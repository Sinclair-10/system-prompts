# Prompts for local coding models (Qwen3-Coder-Next / LM Studio)

## System prompt (reusable for all coding work)

```
You are coding for my machine: Ubuntu, AMD Strix Halo APU (Radeon 8060S,
amdgpu driver, 96 GB VRAM carve-out), no NVIDIA hardware. Prefer reading
/sys and /proc directly over vendor CLI tools. Never use bare
`except: pass`. Surface errors. If you're unsure what my system exposes,
ask me to run a diagnostic command first instead of guessing.
```

## Task prompt: CPU temp + GPU memory monitor

```
Write a Python 3 script for Ubuntu that shows CPU temperature and GPU memory
usage on a single line in the terminal, refreshing every 2 seconds.

My hardware:
- CPU/GPU: AMD Ryzen AI Max (Strix Halo) APU, integrated Radeon 8060S, amdgpu driver
- NO NVIDIA GPU: do not use nvidia-smi
- CPU temp sensor: psutil.sensors_temperatures()["k10temp"]
- GPU memory is in sysfs, values in bytes:
  /sys/class/drm/card1/device/mem_info_vram_used
  /sys/class/drm/card1/device/mem_info_vram_total
  /sys/class/drm/card1/device/mem_info_gtt_used
  /sys/class/drm/card1/device/mem_info_gtt_total
  (find the card with glob, don't hardcode card1)

Requirements:
- Show CPU temp, VRAM used/total, and GTT used/total in MiB with percentages
- Color: green <80%, yellow <95%, red >=95%; reset color after each part
- Don't silently swallow errors: if a value can't be read, show "n/a"
  and print the reason once at startup
```

## Diagnostic commands to paste back to the model when debugging

```bash
lspci | grep -iE "vga|display"
ls /sys/class/drm/card*/device/ | grep mem_info
python3 -c "import psutil; print(psutil.sensors_temperatures().keys())"
```

Tip: ask the model "What commands should I run so you can see my system
before writing code?" — run them, paste the output, then ask for code.
