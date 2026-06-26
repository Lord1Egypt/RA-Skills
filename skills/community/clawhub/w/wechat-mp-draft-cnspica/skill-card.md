## Description: <br>
Uploads local Markdown articles to a WeChat Official Account draft box by converting Markdown to WeChat-compatible HTML, uploading or generating a cover image, and creating a draft through WeChat APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnspica](https://clawhub.ai/user/cnspica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to prepare WeChat Official Account draft articles from local Markdown files after supplying account credentials, article metadata, and optional cover art. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports exposed WeChat credentials in the release artifacts. <br>
Mitigation: Rotate or replace any embedded credentials before use, and provide credentials through a controlled secret-handling process instead of relying on packaged examples. <br>
Risk: The security evidence reports under-disclosed behavior that can read and export existing WeChat drafts. <br>
Mitigation: Review the packaged scripts before installation, run only with accounts whose draft access is intended for this workflow, and confirm that draft-reading behavior is acceptable. <br>
Risk: The security guidance warns against running the skill from directories where untrusted files could affect execution. <br>
Mitigation: Run the skill from a controlled working directory and inspect local Markdown and image inputs before executing the upload workflow. <br>


## Reference(s): <br>
- [WeChat Official Account draft API reference](artifact/references/wechat_api.md) <br>
- [ClawHub skill page](https://clawhub.ai/cnspica/wechat-mp-draft-cnspica) <br>
- [WeChat Official Account platform](https://mp.weixin.qq.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat AppID/AppSecret, a local Markdown file path, and optional cover image, author, and digest inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
