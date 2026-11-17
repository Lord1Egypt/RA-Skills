## Description:

Automate social media posting to Instagram and YouTube. Schedule and publish images, videos, and content automatically. Social media automation tool for content creators, marketers, and businesses. Free alternative to Buffer and Hootsuite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vitja1988](https://clawhub.ai/user/vitja1988)

### License/Terms of Use:


## Use Case:

Content creators, marketers, business owners, and agencies use this skill to prepare commands and configuration for posting Instagram images and YouTube videos through an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived Instagram and YouTube credentials may be stored in local plaintext files.

Mitigation: Use a test account first, keep credential files out of version control, restrict file permissions, and maintain a token rotation or revocation plan.

Risk: Posting examples can publish content to public social channels if the account or visibility settings are wrong.

Mitigation: Verify the target account, media, captions, and visibility before posting; use private or unlisted YouTube uploads and non-production accounts for initial testing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and credential setup instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform-specific posting arguments for Instagram and YouTube.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
