## Description:

Submit articles, shorts, and videos to ZARZOOM for multi-platform social posting; check submission status, pull analytics, and see which platforms each post will land on using customer-managed zarz_live_* API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neildarrenltd](https://clawhub.ai/user/neildarrenltd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and teams use this skill through OpenClaw to submit social content to ZARZOOM, monitor compliance review and publishing status, discover platform eligibility, and review analytics for connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ZARZOOM API key grants access to external posting APIs and may be exposed if stored or shared carelessly.

Mitigation: Treat the key like a password, use the narrowest scopes needed, protect the OpenClaw config file, and rotate the key if exposure is suspected.

Risk: The skill can change real external posting state by submitting content, targeting platforms, cancelling posts, or editing calendar items.

Mitigation: Review content, target platforms, schedules, cancellations, and calendar edits carefully before approving actions.

## Reference(s):

- [ZARZOOM API endpoint reference](reference/api-endpoints.md)
- [ZARZOOM API error codes](reference/error-codes.md)
- [Worked examples - ZARZOOM Skill conversations](reference/examples.md)
- [ZARZOOM API key dashboard](https://zarzoom.com/dashboard/api-keys)
- [ClawHub ZARZOOM skill page](https://clawhub.ai/neildarrenltd/skills/zarzoom)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and concise plain-language status summaries with JSON, HTTP, or shell command snippets when useful.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include submission IDs, status URLs, platform eligibility, analytics summaries, and recovery guidance for API errors.]

## Skill Version(s):

1.0.0 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
