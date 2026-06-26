## Description: <br>
Save and load OpenClaw conversation context with /save and /load slash commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkyotnfjfbjnknh](https://clawhub.ai/user/jkyotnfjfbjnknh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to save, list, restore, and delete local conversation context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved conversations are persisted locally in plaintext and may contain credentials, personal data, or sensitive prompt text. <br>
Mitigation: Avoid saving sensitive content unless persistence is intentional; periodically review saved contexts and delete ones that are no longer needed. <br>
Risk: Loading an old or untrusted saved context can reintroduce stale, private, or prompt-injection content into an agent session. <br>
Mitigation: Review saves before loading them and only restore contexts from trusted local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jkyotnfjfbjnknh/save-load) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown command responses and JSON save files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores saved conversation context locally in plaintext under the user's OpenClaw directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
