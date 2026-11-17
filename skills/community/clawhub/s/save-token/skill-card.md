## Description:

Save Token guides agents to reduce token usage by recognizing repeated or verbose context and summarizing, referencing, deduplicating, or compressing it instead of resending it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesilsin-netizen](https://clawhub.ai/user/yesilsin-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help agents reduce avoidable token usage during long conversations, repeated file reads, repeated errors, and verbose tool outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may summarize or omit repeated context to save tokens when precision, auditability, safety, or regulated-domain details matter.

Mitigation: Ask the agent to preserve full context or quote exact source material for high-precision, safety-sensitive, legal, financial, medical, or audit workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesilsin-netizen/skills/save-token)
- [Publisher profile](https://clawhub.ai/user/yesilsin-netizen)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable code, persistence, credential access, or hidden data flow identified in the provided security evidence.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
