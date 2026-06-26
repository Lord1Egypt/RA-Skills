## Description: <br>
A local context-management skill for adaptive model context limits, layered memory, dynamic memory injection, and SQLite-backed storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[q012315](https://clawhub.ai/user/q012315) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep reusable context in a local SQLite memory store, inspect memory statistics, and adapt context-management behavior for different model context limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores user-provided memory content in a local SQLite database, so sensitive or regulated data could persist on disk. <br>
Mitigation: Avoid adding secrets, credentials, or regulated personal data, and verify the database location printed by --init. <br>
Risk: Some documented commands are not implemented in the bundled script, so relying on them may fail or produce incomplete workflows. <br>
Mitigation: Use the implemented commands or review the script before automation; treat unimplemented documented commands as unavailable until the publisher updates the release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/q012315/q012315-context-manager) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and plain-text CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database under the user's OpenClaw workspace when the script is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
