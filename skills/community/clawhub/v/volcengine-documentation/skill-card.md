## Description:

Looks up and retrieves official Volcengine documentation across products, developer tooling, support, best practices, APIs, SDKs, billing, deployment, troubleshooting, and terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer Volcengine product questions by searching official documentation or fetching full document content, then citing the returned official links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search and fetch inputs are sent to an external Volcengine documentation service.

Mitigation: Do not include credentials, internal prompts, private system details, or non-Volcengine private URLs in search or fetch inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volc-sdk-team/skills/volcengine-documentation)
- [Volcengine documentation search API](https://docs-api.cn-beijing.volces.com/api/v1/doc/search)
- [Volcengine documentation fetch API](https://docs-api.cn-beijing.volces.com/api/v1/doc/fetch)
- [Volcengine documentation example](https://www.volcengine.com/docs/6349/162514)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown responses with official documentation links, plus JSON from the helper script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch output includes a clean documentation URL for citation.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
