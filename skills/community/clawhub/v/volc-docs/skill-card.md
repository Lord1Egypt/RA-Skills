## Description:

Volc Docs helps agents search and fetch official Volcengine documentation for product usage, billing, deployment, troubleshooting, APIs, SDKs, service terms, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinsun-fiver](https://clawhub.ai/user/jinsun-fiver)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support agents use this skill to answer Volcengine product questions by searching official documentation or fetching the full content of a specific Volcengine documentation page.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation queries and fetch URLs are sent to Volcengine's remote documentation API.

Mitigation: Do not include sensitive or confidential information in queries or URLs submitted through the skill.

Risk: The fetch helper can forward arbitrary user-supplied URLs to a remote Volcengine fetch API instead of enforcing an official documentation allowlist.

Mitigation: Use fetch only for trusted Volcengine documentation URLs, preferably HTTPS URLs under www.volcengine.com/docs/.

## Reference(s):

- [ClawHub Volc Docs skill page](https://clawhub.ai/jinsun-fiver/skills/volc-docs)
- [Volcengine document search API](https://docs-api.cn-beijing.volces.com/api/v1/doc/search)
- [Volcengine document fetch API](https://docs-api.cn-beijing.volces.com/api/v1/doc/fetch)
- [Example Volcengine documentation page](https://www.volcengine.com/docs/6349/162514)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown answers with official documentation links; helper commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and fetch results should cite clean Volcengine documentation URLs without query parameters.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
