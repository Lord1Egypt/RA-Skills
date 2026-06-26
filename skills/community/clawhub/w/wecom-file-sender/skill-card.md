## Description: <br>
通过企业微信将本地文件发送给用户，支持文档、图片、视频、语音等常见文件类型和文件大小限制说明。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chongjie-ran](https://clawhub.ai/user/chongjie-ran) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WeCom users and agents use this skill to locate local workspace files and send them to a specified recipient through a MEDIA directive. It is useful when a user needs a document, image, video, or voice file delivered from known workspace folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends local workspace files through WeCom and could expose the wrong or private file. <br>
Mitigation: Use explicit filenames or full paths, verify the recipient, and confirm the selected file before sending any MEDIA directive. <br>
Risk: Broad trigger phrases may cause the agent to act on an imprecise file request. <br>
Mitigation: Ask for clarification when the requested file is ambiguous, especially for companywork or other private folders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chongjie-ran/wecom-file-sender) <br>
- [Publisher profile](https://clawhub.ai/user/chongjie-ran) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with MEDIA directives and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one MEDIA line per selected file path; includes guidance for supported WeCom file size limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
