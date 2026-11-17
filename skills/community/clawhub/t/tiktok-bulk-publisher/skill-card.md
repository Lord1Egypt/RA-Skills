## Description:

Bulk uploads and publishes TikTok videos with OAuth 2.0 authorization and configurable titles, privacy, and interaction settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fly3094](https://clawhub.ai/user/fly3094)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, social media operators, and developers use this skill to automate batch TikTok video publication, including upload commands, scheduling, privacy settings, and interaction controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok API publishing credentials could expose or misuse an account if they are stored, shared, or rotated poorly.

Mitigation: Use a test or low-risk account first, store the client secret securely, and rotate credentials after testing or suspected exposure.

Risk: Bulk publishing can post unintended or excessive content if preview, approval, scheduling, or rate limits are unclear.

Mitigation: Review the configuration and implementation before use, require explicit approval for batches, and confirm scheduling and posting limits before enabling publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fly3094/skills/tiktok-bulk-publisher)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TikTok API client key and client secret configuration.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
