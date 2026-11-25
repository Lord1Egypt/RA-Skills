## Description:

Give the agent long-term memory that survives restarts — store facts, recall them semantically, and forget them on request — backed by a self-hosted SynapCores database. Use when the user asks you to remember something, asks what you remember, wants to correct or delete a stored fact, or wants persistent memory across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synapcores](https://clawhub.ai/user/synapcores)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to configure a SynapCores gateway and give an agent persistent memory across sessions, storing, semantically recalling, correcting, and deleting facts when asked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Docker image source or version may be untrusted or change unexpectedly.

Mitigation: Verify the image source and pin a trusted version before starting the gateway.

Risk: Queries and the API key are sent to the service configured by SYNAPCORES_URL, and security scan coverage is incomplete.

Mitigation: Use a gateway you trust, use HTTPS for remote connections, and review the installation source before use.

## Reference(s):

- [SynapCores project homepage](https://github.com/SynapCores/synapcores-openclaw-memory)
- [ClawHub skill release](https://clawhub.ai/synapcores/skills/synapcores-memory)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, SQL statements, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples for storing, recalling, and deleting memories through a configured SynapCores gateway.]

## Skill Version(s):

0.8.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
