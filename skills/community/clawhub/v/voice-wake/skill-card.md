## Description: <br>
Speak responses aloud on macOS using the built-in `say` command when user input indicates Voice Wake/voice recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kieferhuan](https://clawhub.ai/user/kieferhuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent speak responses aloud on macOS when the latest message begins with the Voice Wake prefix. It keeps normal interactions text-only unless that trigger is present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spoken responses may expose sensitive conversation content in shared or public spaces. <br>
Mitigation: Use the skill only where audible responses are appropriate, and avoid it for sensitive conversations. <br>
Risk: Embedded artifact metadata and server release metadata do not fully align. <br>
Mitigation: Verify the ClawHub package identity, publisher handle, slug, and version before installation or deployment. <br>
Risk: Speech output could be triggered unintentionally if a message begins with the Voice Wake prefix. <br>
Mitigation: Apply the exact prefix check to each latest message and keep responses text-only when the prefix is absent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kieferhuan/voice-wake) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with optional local macOS `say` shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Spoken output is only used when the latest message starts with the configured Voice Wake prefix; otherwise responses remain text-only.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
