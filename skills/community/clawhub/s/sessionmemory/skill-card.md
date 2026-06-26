## Description: <br>
Session Memory helps OpenClaw agents preserve long-running work context by converting session transcripts into searchable Markdown, building a structured glossary, and suggesting memory-aware cron job prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to preserve OpenClaw session history, build searchable memory indexes, and add memory context to recurring agent automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill broadly persists historical OpenClaw conversations into searchable workspace files. <br>
Mitigation: Use it only when persistent session memory is intended, and review generated memory files before sharing or publishing the workspace. <br>
Risk: Generated memory may contain sensitive conversation details with limited privacy controls. <br>
Mitigation: Add redaction, exclusions, file permission tightening, and cleanup procedures before use in sensitive environments. <br>
Risk: Recurring cron indexing can continue copying new session content into memory files. <br>
Mitigation: Avoid enabling recurring cron indexing in sensitive environments unless retention and review procedures are in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/moltbotmolty-del/sessionmemory) <br>
- [AI Advantage](https://aiadvantage.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files, terminal status text, and setup guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes session transcripts, glossary files, converter state, and cron optimization reports under the user's OpenClaw memory workspace.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
