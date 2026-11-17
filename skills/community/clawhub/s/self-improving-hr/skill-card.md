## Description:

Captures anonymized HR policy gaps, compliance risks, recruiting process issues, onboarding friction, retention signals, candidate experience problems, and offboarding gaps for continuous HR improvement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

HR, People Ops, and agent users use this skill to capture anonymized learnings, process issues, and feature requests from recruiting, onboarding, compliance, retention, compensation, performance, DEI, and offboarding workflows. It helps teams review recurring patterns and promote broadly applicable learnings into policies, checklists, scorecards, compliance calendars, or agent guidance after human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HR learning logs may contain privacy-sensitive or regulated employment information if users include raw records or PII.

Mitigation: Keep .learnings local or gitignored, log only anonymized and aggregated details, and never store names, SSNs, salary figures, medical details, raw HR records, or identifiable performance information.

Risk: Optional hooks can add reminders during agent workflows and PostToolUse can inspect command output for HR or compliance terms.

Mitigation: Use project-scoped hooks only, avoid enabling PostToolUse unless needed, keep hook matchers narrow, and do not log raw command output, secrets, transcripts, or HR records.

Risk: Promoting logged learnings into policies, agent instructions, hooks, or generated skills could change HR guidance or workflows.

Mitigation: Review proposed diffs before applying them and require explicit human approval for changes to AGENTS.md, policies, hooks, generated skills, or other durable guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jose-compu/skills/self-improving-hr)
- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown entries, inline shell commands, configuration snippets, and reminder text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or appends local .learnings markdown files and can provide optional project-scoped hook reminders.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
