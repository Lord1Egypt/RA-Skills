---
name: sync-config-with-sample
description: Sync a production config file (e.g. hyprland.lua.gpd) against the latest upstream sample (e.g. hyprland.lua.260917) by copying only reference info/URL comments while preserving the user's actual configuration. Use when the user drops a freshly downloaded sample alongside a live config, mentions keeping the newest sample as the diff baseline, or wants only real config differences to remain visible in diff.
---

# Sync config with upstream sample

The user keeps a **production config** (live `~/.config/...` file, archived in this repo with a device suffix like `.gpd`) next to the **latest upstream sample** (freshly re-downloaded from the project's GitHub repo, named with a date, e.g. `.260917`). The sample is the baseline: the only acceptable diff is the user's real configuration — never reference noise, never lost config.

## Rules (immutable)

1. **Never modify the sample file.** It will be re-downloaded as the example. If it must change, copy a fresh one — never edit it in place.
2. **Never change actual configuration** in the production file: values, binds, active blocks, added features. Copy only reference information.
3. **Reference info = anything inert**: comment lines containing wiki/repo URLs, section headers, `-- See https://...` links, wording of explanatory comments that upstream rewrote. These are safe to adopt verbatim from the sample.
4. **The end state is verified by `diff`**: the only remaining hunks must be real config differences (user's values vs sample's), with zero reference/URL noise.
5. **Raise hands when a hunk is ambiguous** (see Ground truth below) before touching anything ambiguous.

## Procedure

### 1. Establish files and intent
- Identify the production file (`*.gpd` = this device's live config) and the sample (dated `*.2609xx`).
- State the two "don't touch" sets explicitly up front: the sample, and the user's config.

### 2. Diff and classify every hunk
```
diff hyprland.lua.<device> hyprland.lua.<date>
```
For each hunk, classify into one of three buckets:
- **Reference** → apply (copy the sample's exact wording into the production file).
- **Config** → leave untouched, but list it so the user sees what will remain in the diff.
- **Ambiguous** → pause and investigate (below).

### 3. Ground truth before acting on ambiguous hunks
A diffed line may look like config but really be an upstream rename, deprecation, or fixed typo. Determine the truth before deciding:
- Read the **sample** itself (does it document this part?).
- Check upstream: GitHub PRs/commits/issues for the change (e.g. `hyprwm/Hyprland`), the wiki page behind the reference URL.
- Check what the **installed version** on this machine understands: `hyprctl version`, `pacman -Q <pkg>`. If the rename landed *after* the installed release, keep the old name — it works now and the compat shim usually accepts it after upgrade too.
- Present findings + recommendation, get the user's decision, apply.

### 4. Apply reference edits
Use `edit` with exact unique `oldString` matches. Take wording **verbatim** from the sample (whitespace included). Only touch reference lines — if an edit's `oldString` overlaps config code, split the edit or re-classify.

### 5. Verify with the user, step by step
- Re-run `diff hyprland.lua.<device> hyprland.lua.<date>`.
- Confirm: (a) sample unmodified, (b) every remaining hunk is real config, (c) no reference URL hunk left, (d) no config line changed.
- Show the user the final diff and the survival list of their config before finishing.

## Example: hyprland.lua (2026-09)

Concrete classification from a real run:

- **Reference (applied verbatim from sample)**: wiki URLs restructured from `Configuring/Basics/...` and `Configuring/Advanced-and-Cool/...` to lowercase `configuring/core/...` etc. — 15 comment hunks (monitors, autostart, env-vars, permissions, variables, tearing, animations, workspace-rules, dwindle/master/scrolling layouts, devices, binds, window/workspace-rules).
- **Config (kept, remain in diff)**: `fileManager = "thunar"`, `menu = "wofi --show drun"`, the active `hl.on("hyprland.start")` block (fcitx5, waybar, hypridle, hyprsunset), `hl.env("XCURSOR_THEME", "Adwaita")`, hyprsunset `+500/-500` binds, the SCREENSHOTS block.
- **Ambiguous → ground truth**: `dampening` vs `damping` on a spring `hl.curve`. Found upstream PR `hyprwm/Hyprland#15993` — a deliberate rename ("It IS a breaking change") merged Aug 29 2026 with a compat shim accepting the old `dampening`. Installed version here was `hyprland 0.56.2` (Aug 5 2026), old enough that `damping` was not yet recognized. Decision: **keep `dampening`** — works on the installed release and remains accepted after upgrade; stays as a legitimate config diff.