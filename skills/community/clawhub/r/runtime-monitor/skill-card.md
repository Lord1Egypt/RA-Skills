## Description:

Runtime Monitor checks AI agent runtime input, tool arguments, and tool output for prompt injection, data leakage, and dangerous command patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liwiw](https://clawhub.ai/user/liwiw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to inspect AI agent inputs, tool calls, and tool outputs for prompt injection, data exfiltration, and dangerous command patterns before auditing or blocking risky activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring reports may contain raw user input, tool arguments, tool output, or secrets.

Mitigation: Restrict report access, avoid broad logging, and prefer credential redaction before storing or serializing detection results.

Risk: The server security verdict is suspicious because retained monitored text can expose sensitive data.

Mitigation: Review the skill before installation or integration and deploy it only where security report handling is controlled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liwiw/skills/runtime-monitor)
- [Publisher profile](https://clawhub.ai/user/liwiw)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Python monitoring reports with JSON-serializable dictionaries and blocking guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include detection type, risk level, risk score, matched patterns, timestamp, blocked status, and truncated raw input.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
