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
- **Config** → leave untouched, but list it so the user sees what will remain in the diff. Flag one subtype while listing: a line that merely **restates the system default** (e.g. `XCURSOR_THEME` matching what `gsettings` and `/usr/share/icons/default` already resolve to) is a removable hunk — offer to drop it, but it is still a config change, so the user decides.
- **Ambiguous** → pause and investigate (below).

### 3. Ground truth before acting on ambiguous hunks
A diffed line may look like config but really be an upstream rename, deprecation, or fixed typo. Determine the truth before deciding:
- Read the **sample** itself (does it document this part?).
- Ask the **installed binary** first — fastest, and authoritative for the release actually running:
  ```sh
  grep -ao '<key>[a-z]*' "$(command -v Hyprland)" | sort | uniq -c   # which spelling dominates?
  strings "$(command -v Hyprland)" | grep '<canonical example>'      # embedded default config
  ```
  Keys, defaults, and the sample's own example text are compiled in, and parse errors name the expected key (`hl.curve("{}"): damping expects a number`). This settled a rename in one command that PR archaeology had taken a release to explain.
- Check upstream: GitHub PRs/commits/issues for the change (e.g. `hyprwm/Hyprland`), the wiki page behind the reference URL — needed only when the binary is ambiguous.
- Check what the **installed version** on this machine understands: `hyprctl version`, `pacman -Q <pkg>`. If the rename landed *after* the installed release, keep the old name — it works now and the compat shim usually accepts it after upgrade too. Record that decision as **version-bound**, not permanent: it flips when the package upgrades (see the example below).
- Present findings + recommendation, get the user's decision, apply.

### 4. Apply reference edits
Use `edit` with exact unique `oldString` matches. Take wording **verbatim** from the sample (whitespace included). Only touch reference lines — if an edit's `oldString` overlaps config code, split the edit or re-classify.

### 5. Verify with the user, step by step
- Re-run `diff hyprland.lua.<device> hyprland.lua.<date>`.
- Confirm: (a) sample unmodified, (b) every remaining hunk is real config, (c) no reference URL hunk left, (d) no config line changed.
- Show the user the final diff and the survival list of their config before finishing.
- Record the resulting **hunk count and per-hunk reason** in the project's own KB doc, never in the config file: a "keep until version X" comment becomes an extra hunk to re-classify at every sync.

## Example: hyprland.lua (2026-09, updated 2026-11)

Sample source: <https://github.com/hyprwm/Hyprland/blob/main/example/hyprland.lua> (`raw.githubusercontent.com/hyprwm/Hyprland/main/example/hyprland.lua`). Fetch it, then confirm provenance with `md5sum` against a second fetch before diffing — a corrupted download manufactures hunks that upstream never wrote.

Concrete classification from a real run:

- **Reference (applied verbatim from sample)**: wiki URLs restructured from `Configuring/Basics/...` and `Configuring/Advanced-and-Cool/...` to lowercase `configuring/core/...` etc. — 15 comment hunks (monitors, autostart, env-vars, permissions, variables, tearing, animations, workspace-rules, dwindle/master/scrolling layouts, devices, binds, window/workspace-rules).
- **Config (kept, remain in diff)**: `fileManager = "thunar"`, `menu = "wofi --show drun"`, the active `hl.on("hyprland.start")` block (fcitx5, waybar, hypridle, hyprsunset), `hl.env("XCURSOR_THEME", "Adwaita")` (later dropped — see 2026-11), hyprsunset `+500/-500` binds, the SCREENSHOTS block.
- **Ambiguous → ground truth**: `dampening` vs `damping` on a spring `hl.curve`. Upstream PR `hyprwm/Hyprland#15993` is a deliberate breaking rename (merged 2026-08-29) with a compat shim for the old spelling. The **installed release decides**: on `hyprland 0.56.2` (Aug 5 2026) only `dampening` parsed, so it was kept as a legitimate config diff.

### 2026-11 run — the version-bound decision flipped

Two of the 2026-09 rulings were re-decided by newer evidence, which is the point of recording them as version-bound rather than permanent:

- **`dampening` → `damping`**, because `hyprland` had moved to `0.57.1` (Nov 3 2026). The binary's own embedded example now reads `damping`, and its error strings say `"damping expects a number"`; `dampening` survives only as the shim. Hunk removed.
- **`XCURSOR_THEME` dropped as redundant**, because the line only restated the system default: `/usr/share/icons/default/index.theme` → `Inherits=Adwaita` (package `default-cursors`), `gsettings cursor-theme` → `Adwaita`, and only `Adwaita`/`AdwaitaLegacy` are installed. Hunk removed. Worth knowing for the question that always follows: dark mode is a **different layer** (`color-scheme=prefer-dark`, `gtk-theme-name=adw-gtk3-dark`) and was never affected; Adwaita ships no dark cursor variant.
- A sample-added `LAYERS` block was adopted because `hyprctl getoption` showed `set: false` — i.e. the sample's value was already the built-in default, so adopting it was behavior-neutral and removed a hunk. **`set: false` is the tell that a sample block can be copied for free.**

Net: 9 hunks → 5, all deliberate. One caution learned the hard way: when the config is **shared by several hosts**, verify the version-bound item on *every* host, not just the one you are sitting at — a rename that is native on one box breaks the other.
