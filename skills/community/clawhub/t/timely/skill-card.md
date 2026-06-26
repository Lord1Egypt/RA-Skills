## Description: <br>
Manage Apple Reminders from the command line with geofencing support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halbotley](https://clawhub.ai/user/halbotley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and macOS users use this skill to manage Apple Reminders from a terminal, including creating time-based reminders and location-based reminders with arrive or depart triggers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party Homebrew tap and binary. <br>
Mitigation: Verify that the halbotley Homebrew tap and the timely binary are trusted before installation. <br>
Risk: The tool can read or create reminders after macOS Reminders access is granted. <br>
Mitigation: Grant Reminders access only when the user is comfortable with the tool handling reminder contents, shared iCloud lists, and location-based reminder details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/halbotley/timely) <br>
- [Publisher profile](https://clawhub.ai/user/halbotley) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS and the timely command-line binary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
