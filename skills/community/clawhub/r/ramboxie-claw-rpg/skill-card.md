## Description: <br>
D&D-style RPG system for AI lobsters that auto-generates characters, tracks XP from conversations, manages leveling and prestige, and provides a web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RAMBOXIE](https://clawhub.ai/user/RAMBOXIE) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to add RPG-style character progression, XP tracking, leveling, prestige, and optional conversational flavor text to AI lobster assistants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks to read local SOUL.md and MEMORY.md persona or memory files and write persistent character state. <br>
Mitigation: Install only in workspaces where that local data access is acceptable, and review generated or changed state files before relying on them. <br>
Risk: The suggested after-reply hook can automatically modify assistant responses with RPG flavor text. <br>
Mitigation: Keep response modification opt-in and disable the hook in environments that require strict response control or auditability. <br>
Risk: The evidence reports referenced Node scripts, cron setup, and dashboard behavior that are not present in the submitted artifact for review. <br>
Mitigation: Do not enable commands, cron jobs, or the dashboard unless the missing implementation files are supplied and reviewed separately. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated RPG text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent character state when the referenced local scripts are available and enabled.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
