## Description:

Import documents and perform knowledge retrieval via the WeKnora API for file, URL, Markdown, knowledge-base browsing, and hybrid search workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyingbug](https://clawhub.ai/user/lyingbug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure WeKnora credentials, import documents or web content into knowledge bases, browse knowledge entries, and run single- or cross-knowledge-base retrieval workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide edit and delete calls against WeKnora knowledge entries, which may affect business-critical knowledge-base content.

Mitigation: Require explicit user confirmation of the exact knowledge entry before edit or delete operations.

Risk: WeKnora API credentials and base URL are required for use.

Mitigation: Use least-privilege API keys, require HTTPS for WEKNORA_BASE_URL, and avoid storing keys directly in shell profiles.

## Reference(s):

- [ClawHub WeKnora skill page](https://clawhub.ai/lyingbug/skills/weknora)
- [ClawHub publisher profile: lyingbug](https://clawhub.ai/user/lyingbug)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WEKNORA_API_KEY and WEKNORA_BASE_URL environment variables.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
