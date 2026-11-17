## Description:

Use when publishing HTML articles to WeChat Official Account drafts, especially when you need cover upload, automatic cover generation, body image rewriting, CSS-variable compatibility, or draft metadata like author and comment settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhylq](https://clawhub.ai/user/zhylq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content automation users use this skill to save prepared HTML articles as WeChat Official Account drafts, upload required cover or body images, and normalize article HTML for WeChat editor compatibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires WeChat Official Account credentials and can upload article content and images to WeChat.

Mitigation: Use only a dedicated skill-local .env, restrict credential access, and review the target account before running upload commands.

Risk: Article HTML can cause the scripts to fetch remote image URLs or read local image paths before uploading them.

Mitigation: Process only trusted HTML or review all image paths and URLs before execution.

Risk: The image upload helper can write a media ID back to an .env file when --write-env is used.

Mitigation: Avoid --write-env unless you have verified which .env file will be updated.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhylq/skills/zhy-wechat-publish)
- [Publisher profile](https://clawhub.ai/user/zhylq)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local command workflows that read article files, upload article content and images to WeChat, and can update local environment configuration when requested.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
