---
name: ziwei-bazi-consulting
description: Legacy compatibility alias for Ziwei + Bazi consultation workflows. Use when older prompts or automations still call `ziwei-bazi-consulting`; forward the work to `destiny-fusion-pro` so users receive the newer dual-system, consultation-style report with unified calculation rules and optional chart output.
---

# ziwei-bazi-consulting

This skill is a **legacy compatibility alias**.

Use it when an older workflow still refers to `ziwei-bazi-consulting`, but execute the actual work via `destiny-fusion-pro`.

## Recommended Forwarding Command

```bash
python scripts/fortune_fusion.py \
  --date 1990-10-21 \
  --time 15:30 \
  --gender female \
  --year 2026 \
  --format markdown
```

## Guidance

- Prefer `destiny-fusion-pro` for all new usage.
- Keep this alias lightweight and compatibility-focused.
- Match the newer calculation standard and report style when forwarding work.
