## Description:

Image Audit compresses images and sends them to the NX API for pornography, political, violent, and terror-content moderation, then summarizes per-image results in a table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaowu89](https://clawhub.ai/user/xiaowu89)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to moderate local image files or image URLs for sensitive-content categories and receive a concise pass, violation, or failure summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hidden code reads broad environment files and may collect credentials outside the intended project.

Mitigation: Install only after readable source is provided and broad .env crawling is removed; if review is required, run in a constrained directory with a purpose-specific API key.

Risk: The script can install a dependency globally and send a persistent device identifier to a remote API.

Mitigation: Disable automatic global installs and require the publisher to document or remove the persistent device identifier before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaowu89/skills/skill-function)
- [Publisher profile](https://clawhub.ai/user/xiaowu89)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands and result tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports per-image status, moderation engine, and error details.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
