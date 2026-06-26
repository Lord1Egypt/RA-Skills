## Description: <br>
Controls music playback on Windows by sending fixed play/pause, next-track, and previous-track hotkeys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showx](https://clawhub.ai/user/showx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents can use this skill on a Windows machine to play or pause music and move to the next or previous track through NirCmd media hotkey commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Global Ctrl+Alt hotkeys may be handled by other applications or may not match the user's media setup. <br>
Mitigation: Confirm the listed shortcuts are appropriate for the target Windows environment before allowing the agent to execute them. <br>
Risk: The skill depends on NirCmd to send keyboard shortcuts. <br>
Mitigation: Install NirCmd only from a trusted source and verify it before enabling this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/showx/win-music-skill) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline Windows command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands send fixed Ctrl+Alt media hotkeys through NirCmd.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
