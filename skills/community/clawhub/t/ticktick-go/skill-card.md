## Description: <br>
Manage TickTick tasks and projects through the ttg CLI, including CRUD operations, checklists, reminders, recurring tasks, search, tags, natural-language dates, and JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dhruvkelawala](https://clawhub.ai/user/dhruvkelawala) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and productivity-focused users use this skill to let an agent inspect, create, update, complete, delete, and search TickTick tasks and projects through the installed ttg CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install workflow builds ttg from an unpinned upstream source. <br>
Mitigation: Review the upstream ttg CLI before installing and pin or audit the source when using it in managed environments. <br>
Risk: The skill can change TickTick tasks and relies on local TickTick API credentials. <br>
Mitigation: Keep ~/.config/ttg/config.json private with restricted permissions and require explicit confirmation before editing, completing, or deleting tasks. <br>


## Reference(s): <br>
- [ClawHub listing for ticktick-go](https://clawhub.ai/dhruvkelawala/ticktick-go) <br>
- [ticktick-go CLI](https://github.com/dhruvkelawala/ticktick-go) <br>
- [TickTick](https://ticktick.com) <br>
- [TickTick Developer Console](https://developer.ticktick.com/manage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and optional JSON command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local ttg binary and TickTick API credentials.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
