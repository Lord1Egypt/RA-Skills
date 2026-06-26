## Description: <br>
企业微信聊天文件获取 - 从 ~/.openclaw/media/inbound/ 目录检测和获取通过聊天传递的文件，当用户提到获取文件、发送文件、附件等请求时激活。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chongjie-ran](https://clawhub.ai/user/chongjie-ran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees or agents handling WeCom attachments use this skill to locate recent inbound files, identify common document, image, video, and archive types, read suitable file contents, and archive important files when explicitly approved. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad file requests can cause the agent to scan local WeCom inbound attachments that may include sensitive content. <br>
Mitigation: Use explicit filenames when possible, or have the agent confirm the target file before opening or reading it. <br>
Risk: Copying attachments into persistent work folders can retain sensitive documents longer than intended. <br>
Mitigation: Require clear approval before copying files into companywork/ or otherwise retaining WeCom attachments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chongjie-ran/wecom-file-detect) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/chongjie-ran) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, markdown] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local file paths under ~/.openclaw/media/inbound/ and companywork/.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
