## Description:

Observe OpenClaw session usage, token consumption, context pressure, and model/runtime state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qsczseasd](https://clawhub.ai/user/qsczseasd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect session status, summarize token usage and context pressure, and get concise next-step guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session-level metadata may expose usage, budget, model, runtime, or context-pressure details when shared outside the workspace.

Mitigation: Share summaries only with users who are authorized to view session status, and avoid exposing sensitive session details beyond what the user requested.

Risk: The skill could overstate cost, budget, or session health if source fields are missing.

Mitigation: Do not invent cost numbers; report unavailable fields as unavailable and base recommendations on returned session status data.

## Reference(s):

- [Session Observer Checklist](references/checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/qsczseasd/skills/session-observer)
- [Publisher Profile](https://clawhub.ai/user/qsczseasd)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown status summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Current state, What it means, and Recommended next step sections; unavailable fields are reported as unavailable.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
