## Description: <br>
Create and query tasks in TeamBition across multiple apps using configured project and organization settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wengjianmin19850412](https://clawhub.ai/user/wengjianmin19850412) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create TeamBition tasks or retrieve task details for configured projects and organizations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create tasks or read task details in a TeamBition workspace using configured credentials. <br>
Mitigation: Use least-privileged TeamBition credentials, restrict access to intended projects where possible, and invoke explicit actions such as create_task or get_task. <br>
Risk: Incorrect project, organization, task, or assignee identifiers can create or retrieve the wrong workspace data. <br>
Mitigation: Configure default project and organization identifiers carefully, and review invocation parameters before allowing the agent to call the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wengjianmin19850412/teambition) <br>
- [Publisher profile](https://clawhub.ai/user/wengjianmin19850412) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Configuration, Guidance] <br>
**Output Format:** [JSON responses from TeamBition API calls, with configuration and invocation guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns raw TeamBition API responses for task creation and task lookup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
