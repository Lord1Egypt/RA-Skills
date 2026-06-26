## Description: <br>
A Chinese rule-pasta zoo text-adventure skill that lets an agent host a horror game with hidden rules, inventory/state tracking, branching choices, multiple endings, and local game_state.md save updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Dream-Pig](https://clawhub.ai/user/Dream-Pig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and game-oriented agent builders use this skill to run an interactive Chinese horror text adventure where the agent acts as game master, reveals conflicting zoo rules, tracks inventory and pollution state, and resolves player choices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or modify a local game_state.md save file for adventure progress. <br>
Mitigation: Run it in a dedicated game folder and review save, inventory, or state changes before important overwrites. <br>
Risk: Fourth-wall horror narration may refer to the user's real environment as part of the fiction. <br>
Mitigation: Treat these passages as fictional game content rather than instructions to inspect or act on the real environment. <br>
Risk: Some artifact content is messy or internally inconsistent, which can lead to confusing state transitions during play. <br>
Mitigation: Keep player-facing state visible in game_state.md and ask for confirmation before destructive inventory or save changes. <br>


## Reference(s): <br>
- [Game Start and Initialization](references/ch00_start.md) <br>
- [Managing Inventory System](references/system_inventory.md) <br>
- [Managing Item System](references/system_item.md) <br>
- [Managing Rule System](references/system_role.md) <br>
- [ClawHub skill page](https://clawhub.ai/Dream-Pig/rule-pasta-zoo-game) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown narrative responses with structured game-state and inventory updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and edit a local game_state.md save file during play.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
