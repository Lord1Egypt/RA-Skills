## Description: <br>
Preserve conversation continuity across token compaction cycles by extracting and archiving all prompts with date-wise entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[syedateebulislam](https://clawhub.ai/user/syedateebulislam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to preserve local conversation continuity across compaction cycles by exporting recent session history and reloading archived context in a later session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill deliberately saves and reuses full conversation history, which can preserve sensitive chats across sessions. <br>
Mitigation: Avoid using it for sensitive chats unless local transcript retention is acceptable, and regularly inspect or delete the archive under ~/.clawd/memory. <br>
Risk: Automatic setup, heartbeat, or cron usage can enable ongoing archiving without frequent review. <br>
Mitigation: Run setup, heartbeat, or cron steps only when continuous local archiving is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/syedateebulislam/remember-all-prompts-daily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text, local files, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may write and read local memory files under ~/.clawd/memory when run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
