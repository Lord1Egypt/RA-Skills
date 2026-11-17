## Description:

The Short News helps agents search theshort.ai's curated news feeds, fetch article details with summaries, and list available topics and tags for recent-news grounding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sssemil](https://clawhub.ai/user/sssemil)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ground answers in recent curated news, retrieve concise article summaries, and cite canonical source URLs. It is suited for topic- or tag-scoped current-events summaries rather than opinion, social media, or arbitrary fact-checking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated requests send a theshort.ai API key from the agent session.

Mitigation: Use API keys only in trusted sessions and avoid exposing key values in prompts, logs, or user-facing output.

Risk: Successful news search and detail calls are billable against the developer account.

Mitigation: Prefer free topic and tag discovery before paid calls, use narrow limits for chat responses, and confirm billing-sensitive actions when cost matters.

Risk: Optional billing or credit-balance checks can expose account metadata to the agent session.

Mitigation: Only request or display billing information when the user explicitly asks and is comfortable sharing that account metadata.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sssemil/skills/theshort-news)
- [theshort.ai external API](https://theshort.ai/api/external)
- [OpenClaw API keys dashboard](https://openclaw.theshort.ai/dashboard/keys)
- [OpenClaw credits panel](https://openclaw.theshort.ai/dashboard/credits)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, guidance]

**Output Format:** [Markdown with cited news summaries and inline HTTP or shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful news search and detail calls require an API key and may spend account credits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
