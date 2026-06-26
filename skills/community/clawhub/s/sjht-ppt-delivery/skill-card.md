## Description: <br>
Convert an HTML slide deck to PDF and send the generated file to a Feishu user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aowind](https://clawhub.ai/user/aowind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn generated HTML presentation slides into a multi-page PDF and deliver that file through a configured Feishu bot. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses local Feishu bot credentials and uploads the selected file to Feishu. <br>
Mitigation: Use a least-privileged Feishu bot, verify the recipient open_id, and pass only the intended generated PDF or another trusted file to the send helper. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/aowind/sjht-ppt-delivery) <br>
- [Feishu tenant access token API](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu file upload API](https://open.feishu.cn/open-apis/im/v1/files) <br>
- [Feishu send message API](https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, API Calls, Guidance] <br>
**Output Format:** [PDF file with command-line workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Feishu bot credentials and uploads the selected file to Feishu.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog, released 2026-03-20) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
