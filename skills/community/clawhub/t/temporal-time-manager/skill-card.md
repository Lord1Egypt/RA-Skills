## Description: <br>
Temporal Time Manager lets an assistant manage tasks, schedules, and captured ideas through aitimemg.cn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PANGKAIFENG](https://clawhub.ai/user/PANGKAIFENG) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users connect an OpenClaw assistant to their aitimemg.cn account to list, create, update, and delete tasks and schedules, and to capture ideas through conversation. <br>

### Deployment Geography for Use: <br>
Global use; service data is stored in mainland China on Alibaba Cloud. <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an API token to access aitimemg.cn task, schedule, and idea data. <br>
Mitigation: Keep TEMPORAL_API_TOKEN private and configure it only in the agent environment. <br>
Risk: A modified base URL could send requests to an unintended service. <br>
Mitigation: Verify TEMPORAL_BASE_URL before use and prefer the documented default, https://api.aitimemg.cn. <br>
Risk: Task, schedule, or idea text may contain sensitive user information. <br>
Mitigation: Avoid storing secrets in task or idea text and review assistant-generated content before saving it. <br>
Risk: Update and delete operations can change or remove user time-management records. <br>
Mitigation: Require user confirmation before executing updates or deletes. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/PANGKAIFENG/temporal-time-manager) <br>
- [Publisher profile](https://clawhub.ai/user/PANGKAIFENG) <br>
- [aitimemg.cn](https://www.aitimemg.cn) <br>
- [aitimemg.cn settings](https://www.aitimemg.cn/settings) <br>
- [OpenAPI specification](artifact/openapi.yaml) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Natural-language responses backed by JSON API responses and documented mcporter commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TEMPORAL_API_TOKEN and optionally TEMPORAL_BASE_URL; can create, update, and delete user time-management records.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
