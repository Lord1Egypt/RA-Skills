## Description: <br>
Generate a concise copy-paste handoff summary for continuing the current task after /new or /reset. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kisssam6886](https://clawhub.ai/user/kisssam6886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to create a compact handoff when moving an active task into a fresh chat after /new or /reset, preserving current state, blockers, and next actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default Simplified Chinese output may not match every handoff scenario. <br>
Mitigation: Ask for another language when invoking the skill if the next session should continue in that language. <br>
Risk: A handoff summary can carry forward sensitive or stale task details from the current conversation. <br>
Mitigation: Review the generated summary before reusing it and remove details that should not be shared or continued. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown-style bullet or numbered handoff summary in Simplified Chinese by default] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Eight items or fewer; ends with the specified final Chinese line.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
