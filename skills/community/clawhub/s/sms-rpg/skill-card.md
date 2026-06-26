## Description: <br>
SMS RPG Instruction is a text adventure RPG engine that lets an agent act as the wuxia world creator "Moyan", generate story turns directly, manage local JSON save files, and present meaningful player action choices without requiring an external API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayshna](https://clawhub.ai/user/jayshna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run an interactive wuxia text RPG through an agent, including new-game setup, turn-by-turn narration, action selection, state updates, and local save-slot management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates, updates, overwrites, and deletes RPG save files under ./sms-rpg-saves/. <br>
Mitigation: Install and run it only in workspaces where that directory is dedicated to RPG saves, and keep unrelated sensitive files outside that path. <br>
Risk: The included test script creates, updates, and deletes a test save slot. <br>
Mitigation: Review the test script before running it and execute it only when test save-file changes are acceptable. <br>


## Reference(s): <br>
- [Drive Engine Reference](references/drive-engine.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jayshna/sms-rpg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown and plain-text gameplay responses with JSON save-file content and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local RPG save files under ./sms-rpg-saves/.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release evidence and artifact version history, released 2026-04-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
