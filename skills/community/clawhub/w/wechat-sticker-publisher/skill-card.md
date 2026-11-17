## Description:

Publishes WeChat Official Account image-first sticker posts into the draft box by uploading local images as permanent materials and creating draft-only `newspic` posts through the official API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzlawliet](https://clawhub.ai/user/hzlawliet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and content teams use this skill to create image-first WeChat Official Account draft posts from local image files and short supporting text. It is intended for draft creation only; final publication remains a manual WeChat backend action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads selected local images and draft text to a WeChat Official Account.

Mitigation: Use it only with intended images and copy, then review the generated draft manually in WeChat before publishing.

Risk: WeChat credentials and output records can expose account secrets, media IDs, remote asset URLs, or private local paths.

Mitigation: Keep WECHAT_APP_SECRET private and do not commit local credential files or output records.

## Reference(s):

- [API Notes](artifact/references/api-notes.md)
- [ClawHub Skill Page](https://clawhub.ai/hzlawliet/skills/wechat-sticker-publisher)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON run records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates draft-only WeChat records in an outputs directory; supports up to 20 absolute local image paths per run.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
