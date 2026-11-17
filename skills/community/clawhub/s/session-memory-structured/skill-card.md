## Description:

Creates a structured four-part summary of the previous OpenClaw session when /new or /reset is triggered and appends it to a dated workspace memory file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thelast0802](https://clawhub.ai/user/thelast0802)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users who frequently start or reset sessions use this skill to preserve a concise handoff summary of the prior conversation. It is useful when an agent should resume work from recent session context without treating the summary as a fully governed long-term memory store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recent session content may be sent to the configured model provider.

Mitigation: Use only trusted provider configurations, redact sensitive session content, or add explicit confirmation before the hook runs.

Risk: Generated memory files may contain unreviewed model output that future agents could rely on.

Mitigation: Review generated memory files before treating them as trusted context, and quarantine or validate summaries in higher-risk workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thelast0802/skills/session-memory-structured)

## Skill Output:

**Output Type(s):** [markdown, files, configuration guidance]

**Output Format:** [Markdown appended to memory/YYYY-MM-DD.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The summary is generated from up to 40 recent session messages and written locally by date.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
