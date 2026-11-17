## Description:

Asynchronous reflection and memory integration for genuine AI development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[riley-coyote](https://clawhub.ai/user/riley-coyote)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to reflect on recent sessions, maintain structured memory files, surface pending questions, and inspect continuity state between conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation-derived identity, relationship, question, and reflection data without strong user controls.

Mitigation: Configure the memory directory deliberately, inspect generated files regularly, and avoid using transcripts that contain secrets, credentials, private personal details, or sensitive business information without a cleanup process.

## Reference(s):

- [The Continuity Framework](artifact/references/framework.md)
- [ClawHub skill page](https://clawhub.ai/riley-coyote/skills/vektor-continuity)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text with Markdown memory files and JSON reflection logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local memory, identity, question, and reflection files under the configured memory directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
