## Description:

Interact with Reveal feedback infrastructure to manage products, create review tasks, read AI-analyzed user feedback, get sentiment insights, view submissions, manage notifications, register webhooks, and generate marketing content such as scripts, images, and videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tolulopeayo](https://clawhub.ai/user/tolulopeayo)

### License/Terms of Use:

MIT-0

## Use Case:

Product, marketing, and customer-feedback teams use this skill to inspect Reveal product feedback, review tasks, submissions, notifications, webhooks, and AI-derived insights. It can also help generate marketing scripts, images, and videos from product feedback through the Reveal API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad Reveal API key can be sent to a configurable network destination.

Mitigation: Install only in environments where REVEAL_BASE_URL is unset or pinned to a trusted Reveal endpoint, and keep REVEAL_API_KEY scoped and rotated according to Reveal account policy.

Risk: The skill can perform account-changing actions such as task updates, webhook changes, notification changes, and media generation.

Mitigation: Require explicit user confirmation before sending update, webhook, notification, or media-generation requests.

Risk: Reveal submissions, transcripts, videos, notes, analyses, webhook secrets, and video access tokens may contain sensitive account data.

Mitigation: Avoid exposing secrets or sensitive submission details in responses, logs, or shared outputs; store webhook secrets and video access tokens securely.

## Reference(s):

- [Reveal REST API v1 Reference](references/api-reference.md)
- [Reveal Homepage](https://testreveal.ai)
- [Reveal Skill on ClawHub](https://clawhub.ai/tolulopeayo/skills/reveal-feedback)
- [Publisher Profile](https://clawhub.ai/user/tolulopeayo)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Code, Configuration, Guidance]

**Output Format:** [Markdown with JSON request and response examples, API guidance, and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVEAL_API_KEY; uses Reveal API responses as source data and may return generated media URLs, job IDs, webhook secrets, and video access tokens.]

## Skill Version(s):

1.0.2 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
