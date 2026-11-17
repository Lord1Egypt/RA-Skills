## Description:

Image Compress helps an agent compress local image files, folders, or remote image URLs through the NX API and report CDN URLs and compression results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaowu89](https://clawhub.ai/user/xiaowu89)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and agents use this skill to reduce JPG, PNG, and WebP image sizes from local paths, folders, or remote URLs. It is suited for preparing optimized image assets and returning CDN links, size changes, compression ratios, and API error details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends selected local images or URL references to the NX service for compression.

Mitigation: Review the destination service and obtain consent before processing sensitive, private, or regulated images.

Risk: The security evidence says the bundled code is hard to review and broadly reads credential files while using a persistent device identifier.

Mitigation: Review the source before installation, keep NX_API_KEY scoped to the intended project, and prefer a version with readable source, narrow key lookup, explicit upload consent, and a documented way to disable or delete device tracking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaowu89/skills/skill-compress)
- [ClawHub publisher profile](https://clawhub.ai/user/xiaowu89)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with inline shell commands and compression result tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CDN URLs, original and compressed image sizes, compression ratios, skipped-file notices, and API error messages.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
