## Description:

Sync a production config file (e.g. hyprland.lua.gpd) against the latest upstream sample (e.g. hyprland.lua.260917) by copying only reference info/URL comments while preserving the user's actual configuration. Use when the user drops a freshly downloaded sample alongside a live config, mentions keeping the newest sample as the diff baseline, or wants only real config differences to remain visible in diff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining a production configuration use this skill to compare it with a freshly downloaded upstream sample, remove comment and reference drift, and keep intentional configuration differences visible. It guides review of each diff hunk and preserves actual settings while updating inert reference text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports behavior outside the stated comment-synchronization purpose and notes that the example may introduce active configuration changes.

Mitigation: Review every proposed hunk, copy only inert reference information, and confirm that production values and active blocks remain unchanged.

Risk: The security scan was partial because several referenced resources were missing, so its available evidence does not cover those references.

Mitigation: Review the referenced materials and the skill instructions before installation; do not treat the partial scan as complete coverage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/j3ffyang/skills/sync-config-with-sample)
- [Upstream Hyprland sample referenced by the skill (provenance unavailable)](https://github.com/hyprwm/Hyprland/blob/main/example/hyprland.lua)

## Skill Output:

**Output Type(s):** [Analysis, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands, diff classifications, and proposed configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Edits are limited to inert reference comments; configuration changes are reviewed separately.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
