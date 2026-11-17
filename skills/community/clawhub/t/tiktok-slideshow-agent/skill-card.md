## Description:

Creates six-photo slideshow campaigns for TikTok and other networks, with on-image copy, draft or direct posting, and a daily performance review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perufitlife](https://clawhub.ai/user/perufitlife)

### License/Terms of Use:

MIT-0

## Use Case:

External users who market an app or product use the agent to create photo-based slideshow copy and captions, send TikTok drafts or publish posts, and review performance to refine future hooks and calls to action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preview mode uploads the selected photos and slide text to PostWire even though it skips the posting request, creating a privacy concern.

Mitigation: Use only content approved for PostWire processing, and review the preview wording before relying on it.

Risk: Publishing immediately or sending content to additional networks can distribute a post before the user reviews its final wording and destinations.

Mitigation: Keep draft mode unless immediate publication is intended, and check any additional network targets before sending.

Risk: Hosted retention and account-permission enforcement are unverified, and recurring review schedules may run without clear scope.

Mitigation: Limit recurring reviews to an explicitly chosen scope and avoid sending content whose handling requirements are uncertain.

## Reference(s):

- [PostWire OpenClaw integration](https://postwire.io/mcp/openclaw/)
- [PostWire API documentation](https://postwire.io/docs/)
- [PostWire API errors](https://postwire.io/docs/errors/)
- [ClawHub skill release](https://clawhub.ai/perufitlife/skills/tiktok-slideshow-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, API Calls, Guidance]

**Output Format:** [Slide copy and captions, shell commands, and JSON results and review reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates slideshow media from user-selected photos; drafts are the default, with optional immediate publication and cross-posting. Preview mode uploads photos and slide text to PostWire.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
