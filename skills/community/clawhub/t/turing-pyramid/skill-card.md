## Description:

Prioritized action selection for AI agents with 10 needs, tension scoring, execution-gate tracking, optional continuity scripts, and an opt-in watchdog for local stateful prioritization inside an isolated WORKSPACE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tensusds](https://clawhub.ai/user/tensusds)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to give an agent a local, stateful prioritization loop that turns decaying needs and workspace signals into concrete next-action suggestions. It is intended for isolated workspaces where the operator can review action lists, persistence settings, and optional watchdog behavior before enabling deeper automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default action list can prompt credential or vault audits and external posting, messaging, feed, notification, or service actions.

Mitigation: Review assets/needs-config.json before use and set weight: 0 for those action categories unless they are explicitly approved for the agent.

Risk: The skill reads and writes inside WORKSPACE, so a broad or sensitive WORKSPACE can expose private files to local scans and audit outputs.

Mitigation: Install it only in an isolated WORKSPACE that does not contain credentials, home-directory content, or unrelated sensitive material.

Risk: Heartbeat and cron integration add persistence, and watchdog cleanup or process termination can affect local skill state when opt-in controls are enabled.

Mitigation: Treat heartbeat and cron setup as opt-in persistence; keep allow_kill and allow_cleanup disabled until the watchdog behavior has been reviewed.

## Reference(s):

- [Turing Pyramid ClawHub Page](https://clawhub.ai/tensusds/skills/turing-pyramid)
- [Architecture Reference](references/architecture.md)
- [Tuning Guide](references/TUNING.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text and Markdown with inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs local action suggestions, status summaries, and follow-up commands; state and audit files are written inside WORKSPACE.]

## Skill Version(s):

1.34.10 (source: release evidence, _meta.json, CHANGELOG, and skill footer)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
