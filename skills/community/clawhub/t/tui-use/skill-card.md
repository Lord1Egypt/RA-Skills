## Description: <br>
Operate terminal user interface programs through the tui-agent CLI tool, including editors, system monitors, file managers, database clients, and other ncurses/TUI applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zbflcy](https://clawhub.ai/user/zbflcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate, automate, and test terminal-based programs through a capture-act-capture workflow with tui-agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The external tui-agent helper is referenced but not included in the artifact. <br>
Mitigation: Verify the tui-agent source and version before installing or using it. <br>
Risk: The skill enables an agent to view and control terminal sessions, including sessions that may expose secrets or perform high-impact actions. <br>
Mitigation: Use it only with intended terminal sessions, avoid displaying secrets, and confirm before edits, database changes, shell commands, or other high-impact actions. <br>


## Reference(s): <br>
- [tui-agent source](https://github.com/zbflcy/tui-use/tree/main/tui-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides session-management, screen-capture, keyboard, mouse, waiting, and cleanup workflows for TUI automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
