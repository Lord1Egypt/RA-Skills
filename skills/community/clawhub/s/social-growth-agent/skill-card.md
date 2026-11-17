## Description:

Plans, drafts, and prepares scheduling handoffs for social media content such as posts, reels, and threads with strict anti-spam and explicit user-confirmation limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[utromaya-code](https://clawhub.ai/user/utromaya-code)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and social media operators use this skill to plan content calendars, draft platform-specific posts, check drafts for spam or duplication risks, and prepare scheduling handoff payloads after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated posts could contain inaccurate, duplicated, or platform-inappropriate content if used without review.

Mitigation: Review generated posts before approval and use the skill's safety-check section to resolve duplicates, unsupported claims, and platform constraints.

Risk: Credentials or account access could be exposed if users paste tokens, cookies, or passwords into the conversation.

Mitigation: Provide credentials only to the user's own scheduling system outside the skill and do not include secrets in prompts or generated handoff payloads.

Risk: Scheduling or posting could happen unintentionally if draft IDs, target platforms, or timing are ambiguous.

Mitigation: Use the explicit CONFIRM SOCIAL POST flow only when the exact platforms, text or draft IDs, and publish timing are correct.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/utromaya-code/skills/social-growth-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown sections with optional JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before scheduling or posting actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
