## Description: <br>
Manages Dida365/TickTick projects and tasks through official Dida365 OAuth and Open API commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuperOwenX](https://clawhub.ai/user/SuperOwenX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to authenticate with Dida365/TickTick and manage projects and tasks from a CLI. It supports listing, creating, updating, completing, and deleting task-management records through the official API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Dida365/TickTick OAuth credentials and can access a real task-management account. <br>
Mitigation: Treat ~/.config/ticktick-official/ as secret material and avoid running login in shared or logged terminals. <br>
Risk: The CLI can change, complete, or delete projects and tasks. <br>
Mitigation: Confirm exact project and task identifiers before destructive commands, especially delete operations. <br>
Risk: Task payload files passed with --item-json @path may contain sensitive data. <br>
Mitigation: Do not pass files containing secrets or unrelated private content as task payload input. <br>


## Reference(s): <br>
- [Dida365 Open API](references/dida365-openapi.md) <br>
- [Dida365 Developer Center](https://developer.dida365.com/manage) <br>
- [ClawHub skill page](https://clawhub.ai/SuperOwenX/ticktick-official-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Dida365 OAuth credentials and may write local configuration under ~/.config/ticktick-official.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
