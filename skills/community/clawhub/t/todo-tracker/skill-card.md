## Description: <br>
TODO Tracker maintains a persistent TODO.md scratch pad for tracking prioritized tasks, completed items, and stale reminders across agent sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdrhyne](https://clawhub.ai/user/jdrhyne) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agent operators use TODO Tracker to maintain a persistent workspace TODO.md, manage priorities, mark tasks done, remove entries, and summarize outstanding work during heartbeat checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill maintains a persistent local TODO.md file and can add, mark done, or remove entries. <br>
Mitigation: Use explicit add, done, and remove commands, and review TODO.md before deleting or changing entries. <br>
Risk: The done and remove commands match partial text patterns, so complex regex-like input can affect unintended TODO lines. <br>
Mitigation: Pass simple literal task text where possible and avoid regex-like characters unless the script has been hardened to treat patterns as plain text. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jdrhyne/todo-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/jdrhyne) <br>
- [Clawdbot](https://clawdbot.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command guidance, with persistent TODO.md file updates from the bundled script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local TODO.md state; done and remove operations use partial text matching.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
