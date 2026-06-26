## Description: <br>
Access and manage Shortcut.com stories, epics, workflows, comments, dependencies, and backlog searches through the Shortcut REST API v3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[incognos](https://clawhub.ai/user/incognos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, product managers, and delivery teams use this skill to inspect Shortcut work items and prepare or execute story, epic, comment, state-change, and dependency updates from an agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Shortcut token to read and modify Shortcut project data. <br>
Mitigation: Review story, epic, comment, state-change, dependency, and bulk-creation payloads before execution. <br>
Risk: Persisted Shortcut tokens grant member-level access until revoked. <br>
Mitigation: Store the token with restrictive file permissions, avoid persistence when unnecessary, and rotate or delete the token when access is no longer needed. <br>
Risk: Unsafe shell string interpolation could alter JSON request bodies. <br>
Mitigation: Build request bodies with jq using --arg and --argjson so user-provided values are escaped before API calls. <br>


## Reference(s): <br>
- [Shortcut REST API v3](https://developer.shortcut.com/api/rest/v3) <br>
- [Shortcut API base URL](https://api.app.shortcut.com/api/v3) <br>
- [Bulk Epic + Story Creation](references/create-stories.md) <br>
- [ClawHub skill page](https://clawhub.ai/incognos/shortcut-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and jq examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl and jq with a user-provided Shortcut API token.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
