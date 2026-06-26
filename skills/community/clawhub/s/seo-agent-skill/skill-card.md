## Description: <br>
Distribb is an SEO platform that handles keyword research, original data research, content publishing to WordPress/Webflow/Shopify, high-DR backlink exchange network, internal linking, and social media repurposing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bomx](https://clawhub.ai/user/bomx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing teams, founders, SEO operators, and agents use this skill to research keywords, create SEO-focused articles, add internal and exchange-network links, manage an article calendar, and publish approved content to connected CMS platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent create, update, schedule, or publish public business content through the user's Distribb account. <br>
Mitigation: Require explicit user approval before create, update, Planned scheduling, or publish calls, with the final article, project, CMS destination, status, schedule, and backlink targets shown first. <br>
Risk: The Distribb API key and submitted drafts may contain sensitive business data. <br>
Mitigation: Treat DISTRIBB_API_KEY, drafts, business context, competitor data, and publishing destinations as sensitive information and avoid exposing them in logs or shared outputs. <br>
Risk: Backlink exchange behavior can affect public SEO content and external linking choices. <br>
Mitigation: Review backlink targets for relevance and accuracy before submission, and include only natural references that the user has approved. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bomx/seo-agent-skill) <br>
- [Distribb homepage](https://distribb.io) <br>
- [Distribb agent signup](https://distribb.io/agentic) <br>
- [Distribb API base](https://distribb.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash curl commands, JSON request and response examples, and HTML article content for Distribb submission.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DISTRIBB_API_KEY environment variable and uses curl and jq to call the Distribb API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
