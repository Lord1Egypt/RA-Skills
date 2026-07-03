## Description: <br>
This skill helps agents use Tencent Cloud SMS APIs to send single or bulk SMS messages, manage SMS signatures and templates, inspect package usage, and check delivery, receipt, and reply status for domestic and international/HK/Macau/Taiwan SMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to guide Tencent Cloud SMS setup and execute the bundled SMS scripts for sending messages, managing signatures and templates, monitoring package usage, and troubleshooting delivery or reply status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal use can handle Tencent Cloud SMS credentials, phone numbers, uploaded Excel sheets, and optional proof images. <br>
Mitigation: Use a least-privilege Tencent Cloud CAM subaccount, keep credentials in environment variables, avoid sharing secrets in chat, and review dry-run previews before continuing. <br>
Risk: Normal use can automatically install unpinned Python packages. <br>
Mitigation: Use a dedicated Python environment and preinstall or pin required dependencies before running the scripts where possible. <br>
Risk: Send, signature, and template actions can affect live SMS resources and may create cost or compliance impact. <br>
Mitigation: Execute write actions only after the bundled dry-run preview and explicit user confirmation, and confirm signatures and templates are approved before sending. <br>


## Reference(s): <br>
- [Tencent Cloud SMS documentation](https://cloud.tencent.com/document/product/382) <br>
- [Domestic SMS quickstart](https://cloud.tencent.com/document/product/382/37745) <br>
- [International/HK/Macau/Taiwan SMS quickstart](https://cloud.tencent.com/document/product/382/37797) <br>
- [Tencent Cloud CAM IP restriction documentation](https://cloud.tencent.com/document/product/598/38037) <br>
- [API limits reference](references/api-limits.md) <br>
- [Error codes reference](references/error-codes.md) <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/tencentcloud-sms-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, JSON, files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON script output, and generated Excel template files for bulk SMS workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts return structured JSON on success or failure; bulk workflows may copy blank Excel templates into the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
