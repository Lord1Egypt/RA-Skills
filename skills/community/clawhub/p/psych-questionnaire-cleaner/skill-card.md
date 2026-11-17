## Description:

Clean, score, and audit psychology questionnaire or survey datasets with reproducible rules, participant-level quality flags, privacy protection, Chinese-language outputs, and traceable reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adecimall](https://clawhub.ai/user/adecimall)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and data-cleaning developers use this skill to audit, clean, score, and document psychology questionnaire or survey datasets while preserving raw inputs, privacy boundaries, and traceable decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill applies default response-time and declared attention-check exclusion rules to derived analysis data.

Mitigation: Compare the exclusion log against the study protocol or preregistration before relying on the cleaned analytical dataset.

Risk: Questionnaire data may contain sensitive participant identifiers or responses.

Mitigation: Minimize identifiers in reports, avoid row-level sensitive answers in narrative output, and confirm participant identifiers are reduced as intended.

Risk: Incorrect scoring keys, item ranges, or reverse-scored items can produce misleading scale scores.

Mitigation: Score only from an authoritative codebook, protocol, manual, item dictionary, or user-approved cleaning plan.

## Reference(s):

- [Cleaning plan template](references/cleaning-plan-template.md)
- [Output contract](references/output-contract.md)
- [Response-quality indicators](references/quality-indicators.md)
- [ClawHub skill page](https://clawhub.ai/adecimall/skills/psych-questionnaire-cleaner)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, files]

**Output Format:** [Markdown guidance plus structured analytical datasets, exclusion records, audit logs, quality reports, and YAML or JSON cleaning plans.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [User-facing outputs are in Simplified Chinese, preserve the raw source file unchanged, and keep renamed fields reversible.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
