## Description: <br>
Conversational shopping list with categories, family sharing, and purchase history for adding, checking off, and organizing items through natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajeenkya](https://clawhub.ai/user/ajeenkya) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Households and personal users use this skill to maintain a shared shopping list, organize items by category, track who added items, check off purchases, and query monthly purchase history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping list data and purchase history can reveal household habits, names, and preferences. <br>
Mitigation: Keep the skill data directory private, review files before sharing or syncing them, and avoid adding sensitive notes unless necessary. <br>
Risk: Malformed or interrupted file updates could corrupt the active list or archive state. <br>
Mitigation: Use the skill's startup checks, corruption backup behavior, and history-before-active archive write order before making list changes. <br>


## Reference(s): <br>
- [Shopping List command reference](skills/shopping-list/references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, files] <br>
**Output Format:** [Conversational text and Markdown summaries backed by JSON data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains active list, configuration, and monthly history JSON files under the skill data directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
