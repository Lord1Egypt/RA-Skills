## Description:

Cloud-native persistent memory for OpenClaw agents that auto-captures conversation facts, auto-recalls relevant context before replies, and supports hybrid search, query rewrite, and experience learning behind one API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frf12](https://clawhub.ai/user/frf12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to add long-term, cross-session memory to an agent through the m0 plugin. It guides agents on when to recall, store, forget, and inspect memory-derived experiences.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic cloud-based memory can persist conversation-derived facts more broadly than a user expects.

Mitigation: Enable the skill only with a trusted m0 plugin and configured cloud endpoint, and avoid secrets, credentials, health, financial, legal, or confidential business information unless separate controls are in place.

Risk: The security review found insufficient documented safeguards for user control over automatic storage and recall.

Mitigation: Use deployments that provide consent, redaction, retention, access review, and deletion controls; honor explicit forget requests promptly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frf12/skills/seekdb-memory)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OpenClaw >= 2026.2.2 and the m0 plugin configured with a valid API key.]

## Skill Version(s):

0.2.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
