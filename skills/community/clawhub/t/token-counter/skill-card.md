## Description:

Track and analyze OpenClaw token usage across main, cron, and sub-agent sessions with category, client, model, and tool attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkhaytman87](https://clawhub.ai/user/mkhaytman87)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect local OpenClaw token usage, identify high-consumption sessions, and break usage down by category, client, model, and tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session transcripts and cron definitions that may contain sensitive prompts, labels, paths, or derived usage metadata.

Mitigation: Install and run it only in workspaces where that local transcript access is acceptable, and avoid --save or --output on shared or synced storage unless retaining derived reports is intended.

Risk: Category, client, and tool-token attribution are heuristic and may be imprecise.

Mitigation: Use the report for hotspot detection and planning, and inspect source sessions before making billing, compliance, or client-allocation decisions.

## Reference(s):

- [Token Counter Classification Rules](references/classification-rules.md)
- [ClawHub Skill Page](https://clawhub.ai/mkhaytman87/skills/token-counter)

## Skill Output:

**Output Type(s):** [analysis, text, json, shell commands, files, guidance]

**Output Format:** [Plain text or JSON reports, with optional saved JSON snapshot files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can cover a time period, selected breakdowns, or a specific session; saved daily snapshots are written only when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
