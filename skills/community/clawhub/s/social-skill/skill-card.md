## Description:

Manage Farcaster social interactions, casting, and feed monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrxlolcat](https://clawhub.ai/user/mrxlolcat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to draft, monitor, and publish Farcaster social interactions through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish public Farcaster casts or attach generated audio without enough user-control detail.

Mitigation: Require explicit user confirmation before publishing casts or attaching audio to public posts.

Risk: The skill may claim that interactions are verified through Farcaster identity without defining how verification is performed.

Mitigation: Only state that an interaction is verified after the runtime performs a real Farcaster identity check.

## Reference(s):

- [Social Skill on ClawHub](https://clawhub.ai/mrxlolcat/skills/social-skill)
- [Publisher profile: mrxlolcat](https://clawhub.ai/user/mrxlolcat)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or concise text with proposed Farcaster post content and action guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested cast text, channel-aware response guidance, voice-cast attachment suggestions, and Farcaster identity references.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
