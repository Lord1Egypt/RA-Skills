## Description: <br>
Sends selected local files to Feishu and automatically handles large files by splitting video or audio at 20 MB and compressing other files as ZIP archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jingrongx](https://clawhub.ai/user/jingrongx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send an explicitly chosen local file to a Feishu user or group, with automatic handling for files larger than Feishu's upload limit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads the selected local file to Feishu. <br>
Mitigation: Verify the exact file path and recipient before running the command. <br>
Risk: Feishu app credentials are required and include a sensitive app secret. <br>
Mitigation: Protect FEISHU_APP_SECRET and any .env file, and use a least-privileged Feishu app. <br>
Risk: The script may try to install the Python requests dependency at runtime. <br>
Mitigation: Prefer preinstalling and pinning dependencies in the execution environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jingrongx/sendfiles-to-feishu) <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, Guidance] <br>
**Output Format:** [Markdown usage guidance and plain-text execution status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads the selected file or generated split/compressed parts to Feishu and reports per-file success or failure.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
