## Description:

Documents the tool services in Teamgram Server including idgen (Snowflake ID), status (online TTL), dfs (Minio file storage), and media (metadata/thumbnails).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhihang9978](https://clawhub.ai/user/zhihang9978)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this documentation-only skill as a concise reference for Teamgram Server tool services, including ID generation, online status TTLs, distributed file storage, media metadata, and service dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Development service addresses, database DSN, Redis, Minio, and MiniHttp examples may be copied into production without review.

Mitigation: Review and adapt configuration examples for the target environment, credentials, network exposure, and production security controls before use.

Risk: The skill is reference documentation and may not reflect future Teamgram Server changes.

Mitigation: Verify service paths, ports, dependencies, and storage behavior against the current Teamgram Server source before relying on the guidance.

## Reference(s):

- [Teamgram Server repository](https://github.com/teamgram/teamgram-server)
- [Teamgram Tool Services on ClawHub](https://clawhub.ai/zhihang9978/skills/teamgram-tool-services)
- [Publisher profile](https://clawhub.ai/user/zhihang9978)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown reference text with YAML and text code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only output; no executable actions, network calls, or credential handling.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
