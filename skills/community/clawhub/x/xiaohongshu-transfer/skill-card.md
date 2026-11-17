## Description:

小红书笔记搬运到 Facebook 和 WordPress 的自动化流程。当用户要求搬运小红书笔记、发布小红书内容到 Facebook/WordPress 时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilixiong](https://clawhub.ai/user/weilixiong)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and developers use this skill to move Xiaohongshu note text and images into Facebook Meta Business Suite and WordPress publishing workflows. It provides steps, scripts, and platform-specific handling for image downloads, upload preparation, and WordPress posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish content to real Facebook and WordPress accounts.

Mitigation: Use test or draft publishing first and confirm target accounts before every run.

Risk: Local image and content files are staged in a shared upload directory.

Mitigation: Validate titles and image URLs before invoking scripts, clear only the intended upload directory, and avoid placing sensitive content there.

Risk: WP_TOKEN is a live publishing credential when provided.

Mitigation: Store WP_TOKEN outside the skill files, scope it to the required site, and avoid exposing it in command output or logs.

Risk: The workflow reposts Xiaohongshu material to other platforms.

Mitigation: Install and use it only when authorized to repost the source material to the configured destinations.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/weilixiong/skills/xiaohongshu-transfer)
- [Platform configuration reference](references/platforms.md)
- [Pitfalls reference](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell, Python, AppleScript, and REST API snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local content and image files and publish posts when executed with account access and credentials.]

## Skill Version(s):

1.0.0 (source: package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
