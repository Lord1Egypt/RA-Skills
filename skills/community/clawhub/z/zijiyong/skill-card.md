## Description: <br>
Guides an agent through Web of Science literature search, Shenzhen University library access, paper screening, abstract extraction, and Feishu Base writeback using local lark-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samadhifire](https://clawhub.ai/user/samadhifire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, research assistants, and academic users use this skill to run a structured WoS-to-Feishu workflow: confirm search scope, collect and screen literature, extract key fields, and write records into a specified Feishu multidimensional table. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can use authenticated WoS/SZU and Feishu access. <br>
Mitigation: Use only authorized accounts, keep passwords and verification codes runtime-only, and pause for the user at SMS, captcha, or other multi-step authentication. <br>
Risk: Feishu writeback could update the wrong Base, subtable, fields, or records. <br>
Mitigation: Confirm the exact Base link, target subtable, field schema, and append/update/overwrite behavior before any writeback. <br>
Risk: The artifact includes a default SZU username for a local workflow. <br>
Mitigation: Review the default username before use and do not persist passwords, verification codes, or other credentials. <br>


## Reference(s): <br>
- [WOS to Feishu execution playbook](artifact/references/playbook.md) <br>
- [Shenzhen University Web of Science entry](https://www.lib.szu.edu.cn/er?key=web+of+science) <br>
- [ClawHub skill page](https://clawhub.ai/samadhifire/zijiyong) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell and PowerShell commands plus structured Feishu field templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide Feishu Base field definitions, record writeback, and verification steps; credentials and write targets require runtime user confirmation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
