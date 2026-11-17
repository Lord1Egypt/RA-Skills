## Description:

Requirement Validator validates whether product requirements are worth implementing by analyzing user feedback, behavior data, competitor coverage, alternatives, impact, frequency, and ROI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, founders, and product teams use this skill to score proposed requirements against product feedback data and produce decision guidance before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input CSV or JSON files may contain sensitive customer or user feedback.

Mitigation: Review and minimize the data before running the skill, and keep analysis local unless your own workflow requires sharing the report.

Risk: Generated scores and recommendations can be misleading if keywords, feedback samples, behavior data, or competitor data are incomplete.

Mitigation: Use explicit input paths and requirement keywords, inspect the generated report, and treat the result as decision support rather than an automatic implementation decision.

## Reference(s):

- [Requirement Validator on ClawHub](https://clawhub.ai/lijinhongucl-pixel/skills/requirement-validator)
- [Publisher profile](https://clawhub.ai/user/lijinhongucl-pixel)
- [README](artifact/README.md)
- [Validation rules](artifact/config/validation_rules.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a numeric validity score, per-dimension analysis, and decision recommendations from local CSV or JSON inputs.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
