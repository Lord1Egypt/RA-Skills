## Description: <br>
TickTick task manager integration for listing projects and tasks, creating tasks, completing tasks, and deleting tasks after OAuth setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiofreitas](https://clawhub.ai/user/kaiofreitas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage TickTick tasks from an agent, including listing projects and tasks, adding reminders or due dates, and completing or deleting tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on external `ticktick-setup` and `ticktick` CLI commands that must be trusted before use. <br>
Mitigation: Install only a trusted TickTick CLI and verify the command source before entering OAuth credentials. <br>
Risk: Complete and delete commands can change or remove tasks in the connected TickTick account. <br>
Mitigation: Review project and task identifiers before running account-changing commands, and revoke TickTick authorization if the integration is no longer used. <br>
Risk: OAuth client secrets and authorization callbacks can expose account access if shared or logged carelessly. <br>
Mitigation: Keep OAuth client secrets private and avoid sharing callback URLs or token-bearing setup output. <br>


## Reference(s): <br>
- [TickTick Developer Site](https://developer.ticktick.com) <br>
- [TickTick Open API Base URL](https://api.ticktick.com/open/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an OAuth-configured TickTick CLI before task operations can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
