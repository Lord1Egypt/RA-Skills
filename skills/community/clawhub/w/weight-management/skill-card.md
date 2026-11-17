## Description:

Weight Management 体重管理 helps users record weight, meals, steps, and sleep in local Markdown files, estimate calories, calculate TDEE, check data completeness, and summarize weight-management trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hadais](https://clawhub.ai/user/hadais)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to maintain a local weight-management journal, estimate meal calories, calculate TDEE, and receive completeness checks, trend summaries, and habit suggestions. The skill is for informational weight tracking and includes a medical disclaimer rather than medical diagnosis or treatment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may request broad chat-history access for importing health data.

Mitigation: Grant chat-history access only when historical import is needed, and prefer manual entry when minimizing data exposure is more important.

Risk: The skill stores sensitive weight, meal, step, and sleep records in local files with under-specified path controls.

Mitigation: Use a dedicated storage folder, limit file permissions, and review the target path before allowing the agent to read or write records.

Risk: The documented filename pattern can include a real user name in health-record filenames.

Mitigation: Use a pseudonym or non-identifying handle in filenames until privacy and path-validation rules are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hadais/skills/weight-management)
- [Food calorie reference](artifact/references/food-calories.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write user-authorized local Markdown health records and may run the bundled TDEE calculator.]

## Skill Version(s):

2.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
