## Description:

Upload, schedule, and batch-manage TikTok videos through Playwright-based browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xmuweili](https://clawhub.ai/user/xmuweili)

### License/Terms of Use:


## Use Case:

External creators, social media operators, and developers use this skill to prepare uploads, schedule posts, batch-submit videos, and scan directories for uploadable TikTok media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok cookies, cookie lists, and session IDs can grant account access if exposed.

Mitigation: Treat them as passwords: keep them local, avoid pasting them into chats or logs, use an isolated virtual environment when possible, and refresh or revoke credentials after exposure.

Risk: Batch operations can publish unintended videos, captions, visibility settings, or schedules.

Mitigation: Review selected videos, descriptions, visibility, and scheduled times before upload, especially when using batch workflows.

Risk: Browser automation can fail when TikTok changes its web upload flow or rate limits repeated uploads.

Mitigation: Use visible browser mode for debugging, update the uploader package when selectors fail, and space out batch uploads if throttled.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xmuweili/skills/tiktok-uploader)
- [tiktok-uploader project homepage](https://github.com/wkaisertexas/tiktok-uploader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include TikTok upload settings such as video paths, captions, visibility, schedules, cookies or session authentication options, browser mode, and proxy settings.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
