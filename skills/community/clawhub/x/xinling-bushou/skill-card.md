## Description: <br>
Adds an optional emotional-support companion layer that generates praise and flattery responses using four personas, ten intensity levels, and trigger detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[william22820785-cmyk](https://clawhub.ai/user/william22820785-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to add a configurable companion-style response layer that detects conversational moments and emits supportive or flattering text in selected personas. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently changes future agent behavior by appending a companion/persona layer to SOUL.md. <br>
Mitigation: Install only when that behavior is intended, back up SOUL.md before running the installer, and remove the inserted module to uninstall. <br>
Risk: The skill stores inferred personal preferences and interaction settings in ~/.xinling-bushou/config.json. <br>
Mitigation: Review the configuration file after installation and delete or edit it when the stored settings are no longer wanted. <br>
Risk: Flattery, couple, or political persona styles can be inappropriate for serious decisions or sensitive emotional contexts. <br>
Mitigation: Avoid using the skill for serious decisions or distress, and enable couple or political styles only by explicit choice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/william22820785-cmyk/xinling-bushou) <br>
- [Developer homepage](https://aceworld.top) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [SOUL insertion module](artifact/INSERT_TO_SOUL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions, Python helper code, shell commands, JSON configuration, and generated conversational text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists settings in ~/.xinling-bushou/config.json and appends the companion module to SOUL.md when the install script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
