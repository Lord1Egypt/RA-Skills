## Description:

AI-powered GitHub repository analysis that accepts a GitHub repo URL and returns a Claude-generated summary of top open issues, developer requests, pain points, and project direction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to inspect a GitHub repository's open issues and get a short summary of what contributors are requesting, the main pain points, and likely project direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted API path asks users to send a reusable Anthropic API key to a third-party gateway without enough handling or retention detail.

Mitigation: Prefer self-hosting with a limited, revocable Anthropic key; only use the hosted endpoint after accepting the billing and exposure risk.

Risk: GitHub issue text is sent to an LLM and can include untrusted or misleading content.

Mitigation: Treat generated summaries as advisory, review source issues before acting, and avoid using the summary as the sole basis for project decisions.

## Reference(s):

- [Repo Insights ClawHub listing](https://clawhub.ai/albionaiinc-del/skills/repo-insights)
- [MeshCore hosted API endpoint](https://meshcore.ai/gateway/call/d062a753-f46c-4a48-808c-fa27dad82de3)
- [Self-hosted source URL mentioned in artifact](https://github.com/albionaiinc-del/repo-insights)

## Skill Output:

**Output Type(s):** [text, json, api calls, guidance]

**Output Format:** [JSON API response with repository identifier, top issue titles, and a plain-text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to five issue titles and a Claude-generated summary capped by the implementation at 500 output tokens.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
