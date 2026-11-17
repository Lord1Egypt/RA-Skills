## Description:

Analyzes wearable health CSV exports covering steps, heart rate, sleep, calories, SpO2, exercise, and distance, then produces compact JSON reports for hourly, daily, weekly, monthly, sleep, and cross-temporal alert views.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javiersgjavi](https://clawhub.ai/user/javiersgjavi)

### License/Terms of Use:


## Use Case:

Developers and health-data users use this skill to run local analyses over exported wearable CSV or ZIP data and generate machine-readable reports for activity, sleep, heart-rate, SpO2, and cross-period alert review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive local wearable health exports.

Mitigation: Run it only on trusted, reasonably sized CSV or ZIP inputs, choose output folders deliberately, and handle generated JSON reports as sensitive health data.

Risk: Health alerts for illness, apnea, bradycardia, arrhythmia-like patterns, burnout, or overtraining can be mistaken for diagnoses.

Mitigation: Treat alerts as non-diagnostic review signals and discuss concerning patterns with a qualified professional when relevant.

## Reference(s):

- [Skill Health overview](references/overview.md)
- [Operations and execution](references/operations.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and compact JSON report outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts print JSON to stdout and can optionally write JSON files to a selected output directory.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
