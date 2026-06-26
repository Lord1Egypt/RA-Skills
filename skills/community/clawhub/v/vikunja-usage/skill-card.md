## Description: <br>
A Vikunja task-management helper that uses REST API v1 with curl and a runtime bearer token to manage projects, tasks, labels, comments, search, filters, and completion state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to operate a local Vikunja task manager through REST API v1, including project and task creation, updates, deletion, labels, comments, search, filtering, and assignee lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a Vikunja bearer token that can grant access to task-management data. <br>
Mitigation: Provide the token at runtime through VIKUNJA_TOKEN or a permission-restricted token file, avoid logging token values, and rotate the token after suspected exposure. <br>
Risk: The included update and delete examples can modify or remove Vikunja projects and tasks. <br>
Mitigation: Review project and task IDs and request payloads before execution, and test destructive operations in a non-production Vikunja instance when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/axelhu/vikunja-usage) <br>
- [Vikunja local API base](http://localhost:3456/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with curl commands and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and a Vikunja bearer token supplied through VIKUNJA_TOKEN or an agent-local token file.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
