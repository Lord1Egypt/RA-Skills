## Description:

Viking Memory lets an agent search, add, list, and read long-term memories through a local OpenViking API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[forvendettaw](https://clawhub.ai/user/forvendettaw)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill when an agent needs to recall saved preferences, past conversation context, or important user information from a local OpenViking memory service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and later retrieve long-term user information without explicit consent, retention, deletion, or sensitivity controls described in the artifact.

Mitigation: Install with clear rules for when memory may be saved, what content is off-limits, and how stored memories can be reviewed or deleted.

Risk: The skill depends on a local OpenViking service at 127.0.0.1:18790, so outputs depend on that service's availability and stored data.

Mitigation: Verify the local service is trusted and running before use, and review returned memory content before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/forvendettaw/skills/viking-memory)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Text responses with optional JSON details and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns memory search results, saved-memory confirmations, read content, directory listings, or local system status from the OpenViking service.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
