## Description:

Guides agents in reorganizing TRPG briefing_package data/ and context_hooks/rules_sections files to reduce token waste.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice26985850](https://clawhub.ai/user/ice26985850)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and TRPG tool maintainers use this skill to audit briefing_package data files, move large occasional-reference content into rules_sections, and update context_hooks keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt file moves, deletions, and context_hooks keyword changes in a TRPG briefing package.

Mitigation: Review proposed file moves, deletions, and config.yaml hook keyword updates before applying them.

Risk: Broad natural-language hook keywords can inject extra context unexpectedly.

Mitigation: Choose specific player-facing keywords and check that common words do not trigger unnecessary rules_sections content.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, configuration]

**Output Format:** [Markdown guidance with YAML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
