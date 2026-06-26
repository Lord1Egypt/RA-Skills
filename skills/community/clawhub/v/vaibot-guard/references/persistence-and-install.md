# Persistence & installation notes

ClawHub security scans may flag VAIBot-Guard as “suspicious” if the skill/package:
- writes secret-bearing env files under `~/.config/...`
- installs/creates systemd units
- modifies OpenClaw wiring/config

To minimize concern:

- Prefer a **manual (foreground) run** for evaluation.
- Make persistence steps (systemd + env file creation) explicitly opt-in.
- Document credentials and side-effects prominently (SKILL.md / README).
- Keep OpenClaw plugin wiring steps in `references/` rather than the top-level quick start.
