## Description: <br>
查询旺小美系统中的客户、录音、接访/接诊和租户项目信息，帮助已授权用户快速查看业务数据。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[156554395](https://clawhub.ai/user/156554395) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized sales consultants, managers, and operators use this skill to query Wangxiaomei customer records, recordings, visit data, and tenant/project context without manually opening the app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent access sensitive customer, recording, visit, account, and tenant/project data after authorization. <br>
Mitigation: Install only for trusted Wangxiaomei/Wangxiaobao use, make prompts explicit, and review returned data before sharing it. <br>
Risk: A persisted ~/.wangke-auth-token can continue granting access on the local machine. <br>
Mitigation: Do not expose the raw token, avoid shared machines, and clear ~/.wangke-auth-token when access is no longer needed. <br>
Risk: Queries may run against the wrong tenant or project context. <br>
Mitigation: Verify the active tenant or project before data queries and after any switch operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/156554395/wxm-assistant) <br>
- [Wangxiaobao service](https://www.wangxiaobao.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summaries with optional shell command snippets and API-derived records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authorized Wangxiaomei token stored locally.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
