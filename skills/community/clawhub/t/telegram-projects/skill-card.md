## Description: <br>
Telegram Projects helps an OpenClaw agent manage persistent per-group Telegram project notes, instructions, knowledge files, glossaries, and active-project context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to keep Telegram group conversations attached to persistent project memory, including permanent instructions, knowledge entries, generated glossaries, and active-project summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Telegram group context persistently in the local OpenClaw workspace. <br>
Mitigation: Install only when persistent local project memory for Telegram groups is desired, and review what group information is added to project knowledge files. <br>
Risk: The bundled scripts can create project folders and update SOUL.md, which may affect the context an agent loads for Telegram group messages. <br>
Mitigation: Review the scripts before running them and inspect generated or modified workspace files after initialization or synchronization. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/moltbotmolty-del/telegram-projects) <br>
- [Publisher Profile](https://clawhub.ai/user/moltbotmolty-del) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and local workspace file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local OpenClaw project files such as project.md, knowledge.md, glossary.md, PROJECTS.md, and SOUL.md.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
