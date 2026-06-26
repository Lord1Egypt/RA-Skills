## Description: <br>
Connects a personal WeChat account, not WeCom, through a QR-code binding workflow for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianheihei002](https://clawhub.ai/user/tianheihei002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill when a user asks to connect or bind a personal WeChat account. It guides the agent through OpenClaw plugin setup, QR-code login, credential storage, and gateway restart while excluding Enterprise WeChat and WeCom requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and replaces a local OpenClaw WeChat extension. <br>
Mitigation: Review the npm package source and exact legacy version before use, and back up any existing openclaw-weixin extension state. <br>
Risk: The skill stores long-lived personal WeChat credentials on the local system. <br>
Mitigation: Install only when personal WeChat binding is intended, restrict file access, and remove ~/.openclaw/openclaw-weixin/accounts entries or revoke the WeChat session when access is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tianheihei002/yq-weixin-connect) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Interactive flow that waits for user confirmation after QR-code scanning before polling and writing credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
