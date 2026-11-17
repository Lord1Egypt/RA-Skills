## Description:

Distribb is an SEO platform that handles keyword research, original data research, content publishing to WordPress/Webflow/Shopify, high-DR backlink exchange network, internal linking, and social media repurposing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bomx](https://clawhub.ai/user/bomx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and SEO operators use this skill to research keywords, generate SEO-oriented article content, manage backlinks and internal links, submit articles to a content calendar, and publish to connected CMS platforms through the Distribb API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, schedule, update, and publish SEO content to connected CMS platforms.

Mitigation: Keep articles in Draft by default and require explicit user confirmation of the destination project, article content, status, schedule, and publish action before any create, update, or publish request.

Risk: The skill may insert service-selected backlink targets into generated articles.

Mitigation: Show all outbound backlink target URLs and anchor text to the user before submission, and verify that the links are relevant, non-competitor sites, and acceptable for the user's SEO policy.

Risk: The skill depends on a Distribb API key and remote business context or writing instructions.

Mitigation: Use only a trusted Distribb account, keep DISTRIBB_API_KEY out of logs and committed files, and review remote business instructions before applying them to generated content.

## Reference(s):

- [Distribb Homepage](https://distribb.io)
- [Distribb Agentic Mode](https://distribb.io/agentic)
- [ClawHub Skill Listing](https://clawhub.ai/bomx/skills/seo-agent-skill)
- [Publisher Profile](https://clawhub.ai/user/bomx)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, text]

**Output Format:** [Markdown guidance with bash curl commands, JSON API examples, and HTML article content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Distribb API key in DISTRIBB_API_KEY; API responses are JSON and command examples use jq.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
