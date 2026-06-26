## Description: <br>
Send images inline in Feishu chat by uploading them to the Feishu Open API and sending an image message with the returned image_key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamesqin-cn](https://clawhub.ai/user/jamesqin-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to send rendered image messages to Feishu users or chats when the standard message attachment path does not display images inline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes and uses Feishu app credentials in a way users should review before installation. <br>
Mitigation: Do not use embedded Feishu secrets; rotate any real exposed secret, remove hardcoded credentials, and use a managed secret source. <br>
Risk: The skill can send an image through a Feishu account to an unintended recipient or with the wrong file path. <br>
Mitigation: Require explicit confirmation of the Feishu account, recipient, and exact absolute image path before sending. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jamesqin-cn/send-feishu-image) <br>
- [Feishu Upload Image API](https://open.feishu.cn/document/ukTMukTMukTM/ukTM5UjL5ETO14COxkTN/1images-1upload) <br>
- [Feishu Send Message API](https://open.feishu.cn/document/ukTMukTMukTM/ukTM5UjL5ETO14COxkTN/1messages-1create) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown instructions with JavaScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials, a recipient identifier, and an absolute path to a readable image file; supported image files are limited to 30 MB.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
