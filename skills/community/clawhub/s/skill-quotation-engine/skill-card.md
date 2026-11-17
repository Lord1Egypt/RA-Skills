## Description:

Generates quotation data for live event projects from equipment lists, labor inputs, transportation costs, insurance, management fees, and tax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zimuge-doudou](https://clawhub.ai/user/zimuge-doudou)

### License/Terms of Use:

MIT-0

## Use Case:

Event production teams and agents use this skill to calculate quote components for live show projects and generate reviewable quotation summaries or JSON records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated financial totals may be inaccurate if quantities, rates, durations, or tax assumptions are wrong.

Mitigation: Review quote outputs before using them as business documents and validate all pricing inputs against the project contract or rate card.

Risk: The workflow is documented and implemented primarily in Chinese, which may cause review or operational errors for teams that do not use Chinese-language quotation workflows.

Mitigation: Install only where Chinese-language quotation output is acceptable or add localization and reviewer checks before deployment.

Risk: JSON export writes to a caller-provided filepath, so unsuitable paths could overwrite local files in the execution environment.

Mitigation: Constrain export paths to approved working directories and add filepath validation before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zimuge-doudou/skills/skill-quotation-engine)
- [Publisher Profile](https://clawhub.ai/user/zimuge-doudou)

## Skill Output:

**Output Type(s):** [text, code, JSON]

**Output Format:** [Python dictionary or JSON quotation data, with optional plain-text summary output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Financial totals are generated from supplied equipment, labor, transportation, insurance, management, and tax inputs and should be reviewed before business use.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0 and __init__.py reports 2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
