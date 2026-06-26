## Description: <br>
Creates draft-only WeChat Official Account image-first sticker posts by uploading local images as permanent materials and creating `newspic` drafts through the official API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hzlawliet](https://clawhub.ai/user/hzlawliet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create WeChat Official Account image-message drafts from local image files and short caption text. It supports draft-box preparation only; final publication remains a manual action in the WeChat backend. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses WeChat Official Account credentials and can upload selected images and caption text to WeChat. <br>
Mitigation: Install and run it only for intended WeChat draft creation, and provide credentials through environment variables or a secure secret manager. <br>
Risk: Local credential files and output JSON records may contain sensitive app details, media IDs, remote asset references, or private filenames. <br>
Mitigation: Keep `wechat.env` and generated `outputs/` records out of version control, and review or delete output records before sharing the skill directory. <br>


## Reference(s): <br>
- [API Notes](references/api-notes.md) <br>
- [ClawHub skill page](https://clawhub.ai/hzlawliet/wechat-sticker-publisher) <br>
- [Publisher profile](https://clawhub.ai/user/hzlawliet) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; execution writes JSON run records.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat Official Account credentials and absolute local image paths; supports up to 20 images per draft.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
