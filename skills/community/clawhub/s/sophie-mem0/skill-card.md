## Description:

Sophie Mem0 provides persistent semantic memory for agents using mem0ai, Qdrant, and configurable LLM and embedding providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingdangmaoup](https://clawhub.ai/user/dingdangmaoup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure and run long-term memory add, search, list, delete, and health-check workflows. It can also automatically extract user details, preferences, tasks, corrections, and other conversation facts for long-term memory storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic memory capture can store personal conversation details long term.

Mitigation: Enable it only after explicit user consent, keep review and deletion controls available, and avoid storing unnecessary raw conversation metadata.

Risk: The privacy claim in the artifact conflicts with configured remote LLM and embedding API processing.

Mitigation: Tell users which model and embedding providers process memory content, and use provider and deployment settings that match the intended privacy requirements.

Risk: API-key prefixes may be printed during health checks.

Mitigation: Avoid exposing key prefixes in logs or user-visible output, and prefer secret-managed configuration.

Risk: Unpinned dependencies and container images may change behavior over time.

Mitigation: Pin Python dependencies and Docker image versions before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dingdangmaoup/skills/sophie-mem0)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, Python snippets, and CLI status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Qdrant storage with configured LLM and embedding providers; automatic memory capture can store selected conversation details long term.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
