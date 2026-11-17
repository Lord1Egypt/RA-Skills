## Description:

Helps agents decide whether a TRPG briefing_package should use standard form-based character creation, guided multi-step character creation, or both.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice26985850](https://clawhub.ai/user/ice26985850)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and TRPG system maintainers use this skill to update briefing_package character_creation settings when rules require simple point allocation, multi-step choices such as race and class, or both.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed edits to character_creation settings or related data files could introduce incomplete or incorrect TRPG character-creation behavior.

Mitigation: Review proposed changes to config.yaml and related data or rules files before applying them.

Risk: Older transition documents can conflict with the current character-creation definition.

Mitigation: Treat config.yaml as the source of truth when it already contains the active character_creation settings, and avoid updating replaced transition files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ice26985850/skills/trpg-guided-char-creation)
- [ClawHub publisher profile](https://clawhub.ai/user/ice26985850)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code]

**Output Format:** [Markdown with YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose edits to config.yaml and related data or rules files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
