## Description: <br>
Send images, PDFs, and other local files into an OpenClaw Weixin chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[starlxa](https://clawhub.ai/user/starlxa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to send generated or selected local files into the current OpenClaw Weixin conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A selected local file may be sent to the wrong Weixin chat or recipient. <br>
Mitigation: Verify the absolute file path, caption, account, and current chat recipient before sending. <br>
Risk: Sensitive documents may be shared through the connected Weixin or OpenClaw account. <br>
Mitigation: Confirm that the file is intended for sharing before sending and ask the user to verify receipt afterward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/starlxa/weixin-sender) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses absolute local file paths and optional captions for OpenClaw Weixin media delivery.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
