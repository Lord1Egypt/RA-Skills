## Description: <br>
Interact with Reveal feedback infrastructure to manage products, create review tasks, read AI-analyzed user feedback, get sentiment insights, view submissions, manage notifications, register webhooks, and generate marketing content such as scripts, images, and videos. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tolulopeayo](https://clawhub.ai/user/tolulopeayo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, marketing, and customer feedback teams use this skill to inspect Reveal account data, summarize product review insights, manage review tasks and notifications, register webhooks, and generate marketing assets from feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Reveal API key to read account data and change account state. <br>
Mitigation: Keep REVEAL_API_KEY private and require explicit confirmation before creating or changing review tasks, marking notifications, generating persistent media jobs, or registering webhooks. <br>
Risk: Webhook registration can create persistent callbacks and returns a signing secret. <br>
Mitigation: Use only URLs the user controls, limit subscribed events, store the signing secret securely, and remove unused webhooks. <br>
Risk: The optional REVEAL_BASE_URL override can redirect API traffic to a nonstandard endpoint. <br>
Mitigation: Set REVEAL_BASE_URL only when the endpoint is fully trusted. <br>


## Reference(s): <br>
- [Reveal REST API v1 Reference](references/api-reference.md) <br>
- [Reveal Homepage](https://testreveal.ai) <br>
- [ClawHub Skill Listing](https://clawhub.ai/tolulopeayo/reveal-feedback) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, configuration, guidance] <br>
**Output Format:** [Markdown summaries with API request guidance and returned Reveal URLs or identifiers when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVEAL_API_KEY and may return task IDs, webhook secrets, image URLs, video job IDs, access tokens, or video URLs from the Reveal API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
