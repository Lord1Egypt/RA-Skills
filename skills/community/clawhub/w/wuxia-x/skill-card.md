## Description: <br>
武侠X is a Chinese-language text-adventure game engine powered by Drive Engine v3, generating wuxia narratives, goals, challenges, crises, progress tracking, action options, and up to five local save slots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jayshna](https://clawhub.ai/user/jayshna) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to run an interactive wuxia text RPG in Chinese, with the agent generating story turns, meaningful action choices, world-state updates, and local JSON save files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may create, update, read, and delete local game save files in ./sms-rpg-saves/. <br>
Mitigation: Use a dedicated workspace for play sessions and avoid storing sensitive personal information in game saves. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayshna/wuxia-x) <br>
- [Drive Engine 驱动引擎](references/drive-engine.md) <br>
- [Cultivation goal templates](templates/goals/cultivation.yaml) <br>
- [Relationship goal templates](templates/goals/relationship.yaml) <br>
- [Enemy crisis templates](templates/crises/enemy.yaml) <br>
- [Relationship crisis templates](templates/crises/relationship.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style interactive narrative with structured JSON save data and occasional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Manages up to five local game save files under ./sms-rpg-saves/.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and SKILL.md version history, released 2026-04-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
