## Description:

动物园规则怪谈 is a Chinese interactive horror text-adventure skill where an agent runs a rules-based zoo mystery, tracks player state, inventory, items, hidden rules, and resolves choices toward multiple endings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dream-pig](https://clawhub.ai/user/dream-pig)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run a Chinese rules-horror zoo text adventure, manage player inventory and game state, reveal hidden area rules, and narrate choices through survival, discovery, and multiple endings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may maintain a local game_state.md save file during play.

Mitigation: Run it in the intended game workspace and review file changes before reusing or publishing the save state.

Risk: Hidden formatting characters and inconsistent reference names may confuse readers or file lookup during gameplay.

Mitigation: Sanitize hidden formatting characters and align referenced file names before publication.

## Reference(s):

- [Game Start and Initialization](references/ch00_start.md)
- [Managing Inventory System](references/system_inventory.md)
- [Managing Item System](references/system_item.md)
- [Managing Rule System](references/system_role.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown narrative with local game-state file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and update a local game_state.md save file during play.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
