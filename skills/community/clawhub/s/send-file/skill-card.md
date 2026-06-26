## Description: <br>
Sends generated documents, local files, or screenshots to messaging platforms, with Feishu support through bundled upload and send scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wlong800](https://clawhub.ai/user/wlong800) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and developers use this skill to send generated reports, local files, or screenshots from an agent session to a messaging recipient, especially Feishu conversations configured with app credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send local files or screenshots to Feishu using broad triggers and inferred recipients, which may disclose unintended data. <br>
Mitigation: Require explicit confirmation of the exact file path, file size, platform, and recipient before each send. <br>
Risk: Feishu app credentials can authorize file upload and message sending. <br>
Mitigation: Use a dedicated low-permission Feishu app and avoid storing the app secret broadly. <br>
Risk: Platform file size and file type limits can cause send failures. <br>
Mitigation: Check the target platform's file size and type limits before upload, and notify the user before attempting large sends. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wlong800/send-file) <br>
- [Publisher profile](https://clawhub.ai/user/wlong800) <br>
- [Feishu Open Platform app console](https://open.feishu.cn/app) <br>
- [Feishu tenant access token endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload endpoint](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu message send endpoint](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and command output text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a file path and, for Feishu sends, an open_id plus FEISHU_APP_ID and FEISHU_APP_SECRET environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
