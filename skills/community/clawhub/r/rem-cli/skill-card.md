## Description: <br>
Manages macOS Reminders from the terminal using the rem CLI, including creating, listing, updating, completing, deleting, searching, importing, exporting, and formatting reminders and lists. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BRO3886](https://clawhub.ai/user/BRO3886) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to manage Apple Reminders through the rem CLI, automate reminder workflows, or produce script-friendly command guidance for macOS Reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on installing and using an external rem CLI that can modify local Reminders data. <br>
Mitigation: Install only if you trust the rem project and its installer source; review or pin the installer when possible. <br>
Risk: Granting Reminders access allows the CLI and agent workflows to read or change reminders. <br>
Mitigation: Grant Reminders access only when that access is intended and appropriate for the user's reminders. <br>
Risk: Deletion, import, force, or broad agent installation commands can have persistent effects. <br>
Mitigation: Use destructive or broad commands only when the user explicitly intends those effects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BRO3886/rem-cli) <br>
- [Complete Command Reference](references/commands.md) <br>
- [Natural Language Date Reference](references/dates.md) <br>
- [go-eventkit docs](https://github.com/BRO3886/go-eventkit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands and command reference text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include table, JSON, or plain-text rem CLI output format recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata.version is 0.7.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
