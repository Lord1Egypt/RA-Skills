## Description:

Search and manage a Qdrant vector knowledge base via local CLI helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhlhlf](https://clawhub.ai/user/zhlhlf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to search, add, manage, and migrate reusable project documentation or operational knowledge in a Qdrant vector knowledge base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Knowledge-base and local agent memory content may be copied to configured Qdrant or embedding services, including plaintext HTTP endpoints.

Mitigation: Use only trusted Qdrant and embedding services, require HTTPS for non-local endpoints, and confirm content is appropriate before upsert, file import, or migration.

Risk: Qdrant and embedding credentials may grant access to external services.

Mitigation: Use narrow, revocable API keys and keep them in environment variables or a permissions-restricted .env file; avoid printing secrets in chat or logs.

Risk: Delete and bulk migration commands can change collection contents or copy OpenClaw memory into Qdrant.

Mitigation: Back up important collections and require explicit confirmation before delete or migrate-sqlite operations.

## Reference(s):

- [ClawHub qdrant-db skill page](https://clawhub.ai/zhlhlf/skills/qdrant-db)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local CLI can search, upsert, delete, inspect collections, and migrate OpenClaw SQLite memory using Qdrant and embedding settings from environment variables or a local .env file.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
