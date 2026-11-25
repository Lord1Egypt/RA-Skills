## Description:

Use when the user encounters VolcEngine errors or needs local troubleshooting for OpenAPI, Python SDK, CLI, IAM, billing, compute, networking, storage, database, CDN, media, AI, security, or VKE cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to diagnose VolcEngine errors across local tools, OpenAPI and cloud product areas. It guides evidence gathering and read-only checks, then explains findings and possible next steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database fault-injection actions or permission changes may disrupt services if treated as routine read-only checks.

Mitigation: Keep checks read-only by default; explain the impact and obtain explicit user confirmation before any state-changing database or permission action.

Risk: Redis logs or key names may expose sensitive operational information.

Mitigation: Collect only the minimum information needed for the case and redact sensitive values and identifiers before sharing.

Risk: The security scan had partial coverage, so it does not establish a complete assessment.

Mitigation: Review the relevant skill guidance and security findings before relying on it for a production troubleshooting workflow.

## Reference(s):

- [ClawHub release](https://clawhub.ai/volc-sdk-team/skills/volcengine-troubleshooting)
- [Getting started and scenario routing](references/getting-started.md)
- [OpenAPI quick checks](references/openapi-quick-check.md)
- [Product domain guide index](references/domain-guides/README.md)
- [Storage and database guide](references/domain-guides/storage-database/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Code]

**Output Format:** [Markdown troubleshooting guidance with diagnostic CLI commands and occasional Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured diagnostic summaries; cloud changes require user confirmation.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
