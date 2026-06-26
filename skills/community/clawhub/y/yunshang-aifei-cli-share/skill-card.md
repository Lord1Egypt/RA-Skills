## Description: <br>
API client for the Yunshang Aifei OA system that lets an agent query and update tasks, projects, users, reports, reimbursements, contracts, and business opportunities through encrypted REST calls without browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanxin0911](https://clawhub.ai/user/wanxin0911) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations users can use this skill to automate Yunshang Aifei OA workflows from an agent or terminal, including reading work items and business records and creating tasks or weekly-report comments. It is intended for users with authorized OA credentials and access to the relevant internal network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad authenticated changes to production OA business data. <br>
Mitigation: Use the lowest-privilege OA account possible, prefer the test environment first, and review endpoint paths and payloads before using raw POST or PUT requests. <br>
Risk: Session tokens are cached in local token files. <br>
Mitigation: Restrict filesystem access to the skill directory and delete cached token files when access is no longer needed. <br>
Risk: CAPTCHA images may be sent to DashScope for recognition. <br>
Mitigation: Confirm that use of DashScope and the associated API key handling are acceptable for the organization before installing or running the skill. <br>
Risk: The skill uses HTTP transport to reach internal OA environments. <br>
Mitigation: Run it only from an approved trusted network where this transport is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wanxin0911/yunshang-aifei-cli-share) <br>
- [Publisher Profile](https://clawhub.ai/user/wanxin0911) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [api-catalog.json](artifact/api-catalog.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, Python snippets, terminal text, and JSON for raw API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May make authenticated HTTP requests to test or production OA environments and may cache session tokens locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
