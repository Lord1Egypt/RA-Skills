## Description:

Build, debug, and extend the Connectify founder network platform, including its React/Vite frontend, Express backend, Redis cache, OpenAI ranking flow, and Apify ingestion stub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deonmenezes](https://clawhub.ai/user/deonmenezes)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run, modify, and troubleshoot the Connectify founder network application, including the query API, chat interface, scoring logic, and connection ingestion flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The included backend can expose contact data without login checks.

Mitigation: Add authentication and tenant-scoped data access before deploying with real network data.

Risk: Detailed contact records may be sent to OpenAI during relevance scoring and action generation.

Mitigation: Disclose this data flow to users and add controls for limiting, redacting, or approving contact data sent to the model provider.

Risk: A public deployment without rate limits or request size limits could be abused.

Mitigation: Add rate limits and request size limits before making the API publicly reachable.

Risk: Dependency and deployment readiness need review before production use.

Mitigation: Update and scan dependencies, then deploy only in a controlled environment until security review is complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deonmenezes/skills/super-personal-search)
- [Artifact README](artifact/README.md)
- [Artifact Skill Guide](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, JSON contracts, and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository edits, local validation commands, API request examples, and configuration changes for the Connectify application.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
