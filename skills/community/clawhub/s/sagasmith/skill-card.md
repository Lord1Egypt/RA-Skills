## Description:

Autonomous D&D 5e AI Dungeon Master — campaign lifecycle management, module generation (5 types × 25 paradigms), rule adjudication, and immersive DM persona (Minthara Baenre).

This skill is ready for commercial/non-commercial use.

## Publisher:

[dajiaohuang](https://clawhub.ai/user/dajiaohuang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use SagaSmith to run D&D 5e campaigns with agent-assisted dungeon mastering, campaign state management, rule adjudication, module import or generation, save/load/undo, and character progression.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package asks for broad, always-active control over agent behavior and local workspace files.

Mitigation: Install only in workspaces intended for D&D campaign play, and review global templates before adding them to a general-purpose assistant.

Risk: Module import workflows can process local files or directories selected by the user.

Mitigation: Review files before importing them as modules and avoid pointing imports at broad home, download, or project directories.

Risk: Memory and heartbeat behavior can retain or refresh campaign context beyond a single interaction.

Mitigation: Keep memory and heartbeat features under explicit user control and scope campaign state by campaign ID.

## Reference(s):

- [SagaSmith ClawHub Listing](https://clawhub.ai/dajiaohuang/skills/sagasmith)
- [SagaSmith README](artifact/README.md)
- [SagaSmith Skill Definition](artifact/SKILL.md)
- [D&D DM Rules](artifact/skills/dnd-dm/references/DM_RULES.md)
- [D&D DM Output Templates](artifact/skills/dnd-dm/references/DM_TEMPLATES.md)
- [Character Creation Reference](artifact/skills/dnd-dm/references/CHAR_CREATION.md)
- [Campaign Database Contract](artifact/skills/dnd-campaign-manager/references/database-contract.md)
- [D&D Module Generator Skill](artifact/skills/dnd-module-gen/SKILL.md)
- [D&D 5e SRD Skill](artifact/skills/dnd-dm/srd/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with command snippets and generated campaign or module files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist campaign state, generated modules, snapshots, and user-role mappings in the configured workspace or database.]

## Skill Version(s):

1.0.2 (source: release metadata; artifact SKILL.md frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
