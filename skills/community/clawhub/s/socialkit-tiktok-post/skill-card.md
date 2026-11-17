## Description:

Sends a video to the user's TikTok as a draft (default) or posts it directly through the official Content Posting API, following TikTok's content sharing rules and the user's explicit choices. Use when the user wants to upload or post a video to TikTok.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and send a video to TikTok, usually as a draft for final publication in the TikTok app. They can choose direct posting after reviewing the creator, visibility, and interaction settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Direct posts from an unaudited personal app may be limited to private visibility.

Mitigation: Use draft mode by default; before direct posting, show the creator and available privacy options and require the user to choose the settings and approve the post.

Risk: Local credentials and TikTok account access can remain after the skill is removed.

Mitigation: Protect the local credential directory and revoke the app's account access when finished.

## Reference(s):

- [TikTok setup](references/setup.md)
- [TikTok Content Sharing Guidelines](https://developers.tiktok.com/doc/content-sharing-guidelines)
- [TikTok Content Posting API: Direct Post](https://developers.tiktok.com/doc/content-posting-api-reference-direct-post)
- [TikTok Login Kit for Desktop](https://developers.tiktok.com/doc/login-kit-desktop)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and JSON post settings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One video upload workflow; draft mode is the default and direct posting requires explicit user choices and approval.]

## Skill Version(s):

0.3.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
