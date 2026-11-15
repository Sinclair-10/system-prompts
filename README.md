# system-prompts

Reusable system prompts for local LLMs (LM Studio, Ollama, llama.cpp).

Public prompts use `{{PLACEHOLDERS}}` instead of real environment details.
Real values live only in `values.local.env` on each machine, which git ignores.
`render.py` fills in the placeholders and writes ready-to-paste prompts to `rendered/` (also ignored).

## Layout

```
prompts/        public prompts with {{PLACEHOLDERS}}
templates/      starting point for new roles
values.example.env   list of every placeholder, with fake values (safe to commit)
values.local.env     your real values (NEVER commit; git-ignored)
rendered/       filled-in prompts for this machine (git-ignored)
render.py       fills placeholders from values.local.env
```

## First-time setup on a machine

```bash
git clone https://github.com/<you>/system-prompts.git
cd system-prompts
cp values.example.env values.local.env     # Windows: copy values.example.env values.local.env
# edit values.local.env with the real values
python3 render.py                          # Windows: python render.py
```

Open the file in `rendered/`, copy it into LM Studio's System Prompt box, and save it as a preset.

## Adding a prompt

1. Copy `templates/role-template.md` into the right folder under `prompts/`.
2. Use `{{NAME}}` for anything environment-specific (domains, hosts, IPs, groups, paths).
3. Add each new placeholder to `values.example.env` with a fake value.
4. Run `python3 render.py` and check the output.

## Before every commit

- `git status` must NOT list `values.local.env` or anything in `rendered/`.
- Search for real values that slipped into a prompt: `git grep -i "<your domain>"`.

## Prompts

| File | Role | Best model |
| --- | --- | --- |
| prompts/it-admin/college-it-analyst.md | Senior systems analyst who runs all college IT | gpt-oss-120b, High reasoning |
| prompts/coding/powershell-reviewer.md | Reviews PowerShell scripts for bugs and environment fit | gpt-oss-120b |
| prompts/it-admin/linux-admin.md | Ubuntu server and workstation administrator | gpt-oss-120b / 20b |
| prompts/writing/email-editor.md | Rewrites emails: clear, polite, firm | gpt-oss-20b |
