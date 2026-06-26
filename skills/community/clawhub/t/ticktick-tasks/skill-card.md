## Description: <br>
TickTick task manager integration for listing projects and tasks, creating tasks, completing tasks, and deleting tasks after OAuth setup with `ticktick-setup`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiofreitas](https://clawhub.ai/user/kaiofreitas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People who manage TickTick to-do lists use this skill through an agent to inspect projects and tasks, create reminders or dated tasks, and mark or delete tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow runs a local `ticktick-setup` command and asks for a TickTick client secret. <br>
Mitigation: Confirm the trusted `ticktick-setup` executable before entering credentials. <br>
Risk: Complete and delete commands can modify or remove TickTick tasks. <br>
Mitigation: Review project and task IDs carefully before approving complete or delete actions. <br>


## Reference(s): <br>
- [TickTick Developer Site](https://developer.ticktick.com) <br>
- [TickTick Open API](https://api.ticktick.com/open/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OAuth setup with `ticktick-setup`; users should review task and project IDs before approving complete or delete actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
