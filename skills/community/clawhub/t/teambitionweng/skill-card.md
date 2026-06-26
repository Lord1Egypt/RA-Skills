## Description: <br>
Create and query TeamBition tasks with support for multiple app configurations and automatic token management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wengjianmin19850412](https://clawhub.ai/user/wengjianmin19850412) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to let an agent create TeamBition tasks or retrieve task details through configured TeamBition application credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create TeamBition tasks when supplied with write-capable credentials. <br>
Mitigation: Use least-privilege credentials, configure a narrow default project, and require user confirmation before task creation. <br>
Risk: TeamBition application secrets and access tokens could be exposed if placed in prompts or logs. <br>
Mitigation: Store credentials in the platform's secret storage and avoid echoing credential values in agent-visible messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wengjianmin19850412/teambitionweng) <br>
- [Publisher profile](https://clawhub.ai/user/wengjianmin19850412) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JSON-compatible TeamBition API response objects and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns raw TeamBition API responses for task creation and task lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
