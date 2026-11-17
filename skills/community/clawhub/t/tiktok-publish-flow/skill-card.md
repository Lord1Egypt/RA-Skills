## Description:

Guides agents through posting TikTok videos and photos with music and managing captions in TikTok Studio using Playwright.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexsax777](https://clawhub.ai/user/alexsax777)

### License/Terms of Use:

MIT-0

## Use Case:

Account owners and their authorized agents use this skill to automate TikTok Studio video and photo publishing, select music for photo posts, and manage captions. Scheduled posting requires checking for existing posts to avoid duplicates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automation keeps a logged-in TikTok session in a persistent browser profile.

Mitigation: Use only with the account owner's authorization, perform QR login locally rather than sharing codes in chat, and restrict access to the profile directory.

Risk: Screenshots may expose account information or unpublished content.

Mitigation: Review and clean screenshot output, and limit access to the screenshot directory.

Risk: Automation can publish posts or save edits immediately and may duplicate manually published content.

Mitigation: Check existing posts first and add a dry-run or confirmation gate before publishing or saving edits.

Risk: The caption-edit script needs fixing, and the advertised delete-post capability is not implemented.

Mitigation: Fix and verify editing and remove or implement deletion before relying on either capability.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/alexsax777/skills/tiktok-publish-flow)
- [Project homepage (listed in ClawHub metadata; import provenance unavailable)](https://github.com/alexsax777/tiktok-publish-flow)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Running the scripts can publish content and save screenshots on the account owner's behalf.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
