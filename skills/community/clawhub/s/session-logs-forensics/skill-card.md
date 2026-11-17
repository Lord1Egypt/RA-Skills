## Description:

Analyze OpenClaw session JSONL history for cost spikes, tool-call anomalies, and behavior regressions with jq + rg.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielsinewe](https://clawhub.ai/user/danielsinewe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to inspect authorized session JSONL history for incident forensics, including cost spikes, tool-call anomalies, and behavior regressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to search broad historical session transcripts that may contain sensitive or unrelated content.

Mitigation: Restrict use to trusted, authorized operators and scope analysis to a specific session, date range, or incident whenever possible.

Risk: Forensic outputs may expose secrets, tokens, personal data, or unrelated transcript excerpts.

Mitigation: Redact sensitive and unrelated content before sharing findings outside the authorized incident response context.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danielsinewe/skills/session-logs-forensics)
- [ClawHub Publisher Profile](https://clawhub.ai/user/danielsinewe)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with jq and rg shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq and rg; outputs should be scoped to authorized OpenClaw session logs.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
