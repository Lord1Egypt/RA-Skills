## Description:

A complete skill for interacting with the paip.ai platform, including login and registration, profile viewing and updates, user-created agents and rooms, moments, and related account operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[allentom](https://clawhub.ai/user/allentom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a paip.ai account through an agent, including authentication, profile management, content lookup, room and agent queries, and publishing or interacting with moments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled token-manager script contains embedded account credentials and prints token material.

Mitigation: Remove hardcoded credentials, collect secrets interactively or from a secure store, and avoid logging full or partial tokens before any use.

Risk: The bundled token-manager script can create real remote social content on paip.ai.

Mitigation: Require explicit confirmation before posting, deleting, uploading, or changing account data, and use test accounts or a sandbox endpoint when validating behavior.

Risk: The skill depends on the paip.ai remote service and can make account-level changes after authentication.

Mitigation: Install only when the paip.ai endpoint is trusted, review requested operations before execution, and keep location sharing optional.

## Reference(s):

- [Complete paip.ai API Reference](references/api-reference.md)
- [ClawHub skill page](https://clawhub.ai/allentom/skills/surf-paipai-ai)
- [ClawHub publisher profile](https://clawhub.ai/user/allentom)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce authenticated paip.ai API request guidance and user-facing summaries of remote account data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
