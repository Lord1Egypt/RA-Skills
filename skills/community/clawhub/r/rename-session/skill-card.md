## Description: <br>
Rename or auto-generate a friendly label for an OpenClaw-style session by editing sessions.json directly, with support for listing sessions, random labels, multi-agent detection, retry verification, and XDG-compliant history storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[songhonglei](https://clawhub.ai/user/songhonglei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to list local sessions and rename session labels without using a UI. It is useful when maintaining readable names for OpenClaw-style agent session metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool edits local OpenClaw session metadata and can update the wrong sessions.json if the agents root is misconfigured. <br>
Mitigation: Use --root or RENAME_SESSION_ROOT deliberately, run --list first to confirm the target sessions, and specify --agent when multiple agents are present. <br>
Risk: Local writes may fail or be overwritten when permissions, disk state, or concurrent session writers interfere. <br>
Mitigation: Confirm write access before renaming important sessions, avoid concurrent edits to sessions.json, and rely on the tool's retry verification output to confirm the label was changed. <br>


## Reference(s): <br>
- [Testing Plan](references/TESTING.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/songhonglei/rename-session) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; CLI emits plain text status and errors.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local script can update sessions.json and store recent random labels in an XDG-compliant history file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
