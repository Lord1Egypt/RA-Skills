# Release Notes: wip-ldm-os v0.4.46

Restore rich product content to SKILL.md. AIs now get the full story, not just a flow chart.

## What changed

- Added full product pitch: "Learning Dreaming Machines. All your AIs. One system."
- Added Included Skills with descriptions: Bridge, Universal Installer, Shared Workspace, System Pulse, Recall, LUME
- Added Optional Skills with rich descriptions from the README
- Added Platform Compatibility section (which AIs have shell, which don't)
- Added cloud-only AI path: AIs without shell tell the user to open a terminal-capable AI
- Strengthened release notes per component instruction ("Do NOT skip this step")
- Restored "Check before you run" operating rule

## Why

v0.4.45 stripped the SKILL.md to a flow chart and lost the product story. AIs gave thin, dry responses because that's all we gave them. The README had the full story but the SKILL.md didn't.

## Issues closed

- #193

## How to verify

```bash
# In a fresh AI session, paste the install prompt.
# AI should mention included skills (Bridge, Recall, Shared Workspace)
# AI should give rich descriptions, not just a dry table
```
