#!/usr/bin/env python3
"""Fill {{PLACEHOLDERS}} in prompts/ with values from values.local.env.

Writes results to rendered/ (git-ignored). Reports any placeholder that has no
value, so nothing half-filled gets pasted into a model by accident.

Usage:  python3 render.py            (Windows: python render.py)
        python3 render.py other.env  (use a different values file)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROMPTS = ROOT / "prompts"
OUT = ROOT / "rendered"
PATTERN = re.compile(r"\{\{([A-Z0-9_]+)\}\}")


def load_values(path):
    values = {}
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            sys.exit(f"{path.name} line {n}: expected NAME=value")
        key, val = line.split("=", 1)
        values[key.strip()] = val.strip()
    return values


def main():
    values_file = ROOT / (sys.argv[1] if len(sys.argv) > 1 else "values.local.env")
    if not values_file.exists():
        sys.exit(f"Missing {values_file.name}. Copy values.example.env to "
                 f"values.local.env and fill in real values.")
    values = load_values(values_file)

    missing = {}
    count = 0
    for src in sorted(PROMPTS.rglob("*.md")):
        text = src.read_text(encoding="utf-8")
        for name in PATTERN.findall(text):
            if name not in values:
                missing.setdefault(name, set()).add(str(src.relative_to(ROOT)))
        filled = PATTERN.sub(lambda m: values.get(m.group(1), m.group(0)), text)
        dest = OUT / src.relative_to(PROMPTS)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(filled, encoding="utf-8")
        count += 1

    print(f"Rendered {count} prompt(s) to {OUT.relative_to(ROOT)}/")
    if missing:
        print("\nWARNING: placeholders with no value (left as-is):")
        for name, files in sorted(missing.items()):
            print(f"  {{{{{name}}}}}  in  {', '.join(sorted(files))}")
        sys.exit(1)


if __name__ == "__main__":
    main()
