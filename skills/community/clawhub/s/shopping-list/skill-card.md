## Description:

Conversational shopping list with categories, family sharing, and purchase history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajeenkya](https://clawhub.ai/user/ajeenkya)

### License/Terms of Use:


## Use Case:

External users use this skill to maintain a household shopping list through natural-language requests, including adding items, checking off purchases, editing entries, viewing categories, exporting the list, and querying purchase history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps shopping items, purchase history, and a saved name or nickname in local skill data files.

Mitigation: Install only when local persistence of that household data is acceptable, and avoid adding sensitive personal details to item names or notes.

Risk: Natural-language shopping requests can accidentally change the list when casual conversation resembles an add, remove, check, edit, or switch-user command.

Mitigation: Use explicit shopping commands for mutating actions when precision matters, and review confirmations after add, remove, check, edit, clear, or switch-user operations.

## Reference(s):

- [Command Reference](references/commands.md)
- [ClawHub Skill Page](https://clawhub.ai/ajeenkya/skills/shopping-list)
- [Publisher Profile](https://clawhub.ai/user/ajeenkya)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [Markdown and plain text responses with local JSON data updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains active shopping-list, configuration, and monthly history JSON files in the skill data directory.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
