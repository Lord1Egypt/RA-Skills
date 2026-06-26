## Description: <br>
Time Calc helps agents answer date and time questions by mapping natural-language time expressions to native shell or PowerShell commands for current time, date metadata, weekday lookup, offsets, differences, timezone conversion, and Unix timestamp conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrlyk](https://clawhub.ai/user/mrlyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, technical users, and agents use this skill to resolve date/time questions, calculate offsets and differences, convert time zones, and translate Unix timestamps using platform-native commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted date, timezone, or timestamp text could be placed into local shell or PowerShell commands. <br>
Mitigation: Keep inputs limited to date/time values, quote command arguments, and review generated commands before execution. <br>
Risk: Platform date commands have different semantics for weekdays, month ends, leap years, and timezone identifiers, which can produce incorrect results. <br>
Mitigation: Use the platform-specific reference commands and safe month/year offset patterns bundled with the skill. <br>


## Reference(s): <br>
- [Linux GNU date command reference](references/linux.md) <br>
- [macOS BSD date command reference](references/macos.md) <br>
- [Windows PowerShell date command reference](references/windows.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text with inline shell and PowerShell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses platform-specific command references for macOS, Linux/WSL/Git Bash, and Windows PowerShell.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
