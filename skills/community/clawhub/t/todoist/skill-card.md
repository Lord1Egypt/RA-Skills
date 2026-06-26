## Description: <br>
Manage tasks and projects in Todoist. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mjrussell](https://clawhub.ai/user/mjrussell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to inspect, create, search, update, complete, reopen, move, and delete Todoist tasks, projects, labels, and comments through the Todoist CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change tasks and projects in a connected Todoist account. <br>
Mitigation: Use a revocable Todoist API token and confirm ambiguous or destructive actions such as delete, move, complete, or reopen before allowing execution. <br>
Risk: The skill depends on the globally installed todoist-ts-cli package. <br>
Mitigation: Trust the package source and installed version before granting it Todoist account access. <br>


## Reference(s): <br>
- [Todoist](https://todoist.com) <br>
- [Todoist developer integrations settings](https://todoist.com/app/settings/integrations/developer) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the todoist CLI and a Todoist API token.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
