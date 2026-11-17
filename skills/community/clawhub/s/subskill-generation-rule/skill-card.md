## Description:

Define and enforce project organization rules for generating subskills by placing generated artifacts under data/, feature scripts under subskills/<feature>/, and optional per-feature SKILL.md files inside feature folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenera](https://clawhub.ai/user/kenera)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to keep frequently iterated skills organized by separating generated result artifacts, feature scripts, and optional feature-specific instructions into predictable folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The prescribed data/ and subskills/<feature>/ layout may conflict with an existing project's established organization.

Mitigation: Review the convention before applying it and adapt the folder placement when the project already uses a different maintainable layout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kenera/skills/subskill-generation-rule)

## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown instructions with directory layout examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; the skill provides file-placement conventions for future skill work.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
