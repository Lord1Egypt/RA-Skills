## Description:

Give the agent long-term memory that survives restarts — store facts, recall them semantically, and forget them on request — backed by a self-hosted SynapCores database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synapcores](https://clawhub.ai/user/synapcores)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to store, semantically recall, correct, and delete facts across sessions using a self-hosted SynapCores database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends requests to the configured SynapCores service and relies on its gateway image.

Mitigation: Review the API request and image reference, and configure only a SynapCores service and image you trust.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/synapcores/skills/synapcores-memory)
- [Project homepage](https://github.com/SynapCores/synapcores-openclaw-memory)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands]

**Output Format:** [Natural language with inline shell commands and SQL statements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses curl and jq to issue memory operations through the configured SynapCores gateway.]

## Skill Version(s):

0.8.3 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
