## Description:

Evaluates agent skills with a six-dimension T/C/O/E/M/U quality model and produces structured quality reports with prioritized improvement guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to assess new or existing ClawHub skills before release, version upgrades, or periodic health checks. It applies six-dimensional scoring, summarizes quality signals, and generates prioritized recommendations for improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the local skill directory it is pointed at.

Mitigation: Run it only against intended local skill directories and review the files being assessed.

Risk: The generated scores are heuristic and may not represent definitive security or marketplace approval.

Mitigation: Treat the report as advisory and pair it with human review and any required release checks.

Risk: A generated Markdown report could overwrite an existing report at the selected output path.

Mitigation: Choose the output path deliberately and preserve any existing reports before generating a new one.

## Reference(s):

- [Six Dimensions Criteria](references/six-dimensions-criteria.md)
- [Evaluation Report](skill-quality-assurance-evaluation-report.md)
- [Evaluation Template](assets/evaluation-template.md)
- [ClawHub Skill Listing](https://clawhub.ai/pagoda111king/skills/skill-quality-assurance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with scoring tables, concise findings, prioritized recommendations, and optional command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scores are heuristic quality indicators and should be reviewed before being used for release decisions.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
