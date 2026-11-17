## Description:

Team Builder deploys a customizable OpenClaw multi-agent SaaS team workspace with role templates, inboxes, dashboards, product knowledge files, scheduled checks, onboarding guidance, and optional Telegram binding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyound87](https://clawhub.ai/user/beyound87)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate and configure a persistent OpenClaw team workspace for SaaS and product work, including role definitions, shared coordination files, product deep-dive templates, and cron-based operating routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated install scripts can modify global OpenClaw settings and create scheduled jobs.

Mitigation: Review generated apply-config.js, create-crons.sh, and create-crons.ps1; back up ~/.openclaw/openclaw.json before applying changes; run the provided verification mode before enabling the workspace.

Risk: Untrusted deployment inputs can affect generated executable scripts and configuration.

Mitigation: Use only trusted team-builder.json files, --team values, role names, model IDs, team names, timezones, and workspace paths; inspect generated files before execution.

Risk: Agent-to-agent communication and scheduled jobs create a persistent operating workspace.

Mitigation: Confirm that persistent coordination and scheduled jobs are intended, test with a small role set first, and enable only the roles and cron jobs needed.

## Reference(s):

- [ClawHub Team Builder release page](https://clawhub.ai/beyound87/skills/team-builder)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Deployment script](scripts/deploy.js)
- [Sample Team Builder configuration](team-builder.json)
- [Shared workspace templates](references/shared-templates.md)
- [Role soul templates](references/soul-templates.md)
- [Coding behavior fallback](references/coding-behavior-fallback.md)
- [Fullstack developer deep-dive protocol](references/agent-refs/fullstack-dev/deep-dive-protocol.md)
- [Product lead methodology](references/agent-refs/product-lead/methodology.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Workspace files, Markdown documentation, JavaScript and shell scripts, configuration snippets, and optional JSON verification reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates files for a persistent OpenClaw workspace; generated configuration and cron scripts require manual review and execution.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
