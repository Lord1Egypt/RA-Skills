## Description:

Creates TikTok image carousels with text overlays on photos via the ViralBaby API, including image search, slideshow editing, and TikTok draft upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aryanbhasin](https://clawhub.ai/user/aryanbhasin)

### License/Terms of Use:


## Use Case:

External creators, marketers, and social media operators use this skill to create TikTok photo slideshows: search for background images, assemble slides with text overlays, manage image collections, preview and edit drafts, and upload to TikTok drafts through ViralBaby.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to persist API credentials and generated passwords in environment variables.

Mitigation: Use a dedicated secret manager where available, avoid exposing credentials in chat or logs, and rotate credentials if they may have been revealed.

Risk: The ViralBaby workflow can receive slideshow content, business/style preferences, TikTok connection flow data, and diagnostic or feedback messages.

Mitigation: Confirm the user is comfortable sharing this data before use, and review feedback or error reports before sending them.

Risk: The skill includes destructive actions such as deleting collections or slideshows.

Mitigation: Ask for explicit confirmation before deletion or other irreversible changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aryanbhasin/skills/tiktok-slideshow)
- [ViralBaby API base URL](https://viralbaby.co)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON API request examples, shell command snippets, and returned ViralBaby or TikTok workflow URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce slideshow preview URLs, OAuth connection URLs, checkout URLs, rendered slide URLs, captions, hashtags, and upload status messages.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
