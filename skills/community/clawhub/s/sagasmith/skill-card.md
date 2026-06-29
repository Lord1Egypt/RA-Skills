## Description: <br>
SagaSmith is an autonomous D&D 5e AI Dungeon Master skill pack for campaign lifecycle management, module generation, rule adjudication, combat resolution, and immersive DM narration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dajiaohuang](https://clawhub.ai/user/dajiaohuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and tabletop RPG players use SagaSmith to run D&D 5e campaigns with persistent campaign state, rule lookup, character and combat handling, save/load snapshots, and generated adventure modules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes broad personal-assistant templates that are not clearly disclosed by the D&D skill description. <br>
Mitigation: Review AGENTS.md and templates/agent/identity.md before installation, remove unwanted assistant behavior, and limit calendar, email, social, and messaging tools unless explicitly needed. <br>
Risk: Campaign save, load, restore, delete, and undo actions can make real changes to local campaign data. <br>
Mitigation: Review intended actions before execution, keep verified snapshots, and treat restore or delete operations as state-changing local data operations. <br>


## Reference(s): <br>
- [SagaSmith README](README.md) <br>
- [SagaSmith Skill Definition](SKILL.md) <br>
- [D&D Campaign Manager Skill](skills/dnd-campaign-manager/SKILL.md) <br>
- [D&D DM Skill](skills/dnd-dm/SKILL.md) <br>
- [D&D Module Generator Skill](skills/dnd-module-gen/SKILL.md) <br>
- [DM Rules Reference](skills/dnd-dm/references/DM_RULES.md) <br>
- [DM Output Templates](skills/dnd-dm/references/DM_TEMPLATES.md) <br>
- [Character Creation Reference](skills/dnd-dm/references/CHAR_CREATION.md) <br>
- [Database Contract Reference](skills/dnd-campaign-manager/references/database-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain-text agent responses with inline commands, structured campaign updates, and generated campaign or module content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, verify, restore, or delete local campaign database snapshots and generated module files when the bundled tools are executed.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
