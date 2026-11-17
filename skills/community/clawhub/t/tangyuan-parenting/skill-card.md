## Description:

This skill helps caregivers create simplified-Chinese daily parenting plans, log feedback, retrieve care history, and generate weekly reports for TangYuan, a 2.5-year-old child in Harbin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[protozoan-yuan](https://clawhub.ai/user/protozoan-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

External family caregivers and parents use this skill to coordinate daily care, record observations, adapt plans based on feedback and weather, and summarize weekly childcare patterns for a toddler.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive information about a specific child and stores care logs in the workspace.

Mitigation: Use the skill only in a private workspace, keep tangyuan-logs out of commits and synchronization targets, and avoid sharing generated reports publicly.

Risk: The logging workflow shows shell command examples that can interpolate caregiver-provided feedback into command arguments.

Mitigation: Review and fix command quoting before using the logging workflow with untrusted text, or pass feedback through a safer structured input path.

Risk: Parenting and health recommendations may be mistaken for professional medical advice.

Mitigation: Treat medical content as general guidance and consult a qualified clinician for fever, persistent cough, refusal to eat, or other health concerns.

## Reference(s):

- [Harbin Seasonal Parenting Guide](references/harbin_seasonal_guide.md)
- [2-3 Year Old Scientific Parenting Guide](references/parenting_guide.md)
- [TangYuan Profile](references/tangyuan_profile.md)
- [Daily Plan Template](assets/daily_plan_template.md)
- [Weekly Report Template](assets/weekly_report_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Simplified-Chinese Markdown with occasional shell command examples and local Markdown log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include daily schedules, weekly reports, caregiver feedback summaries, parenting guidance, and log retrieval results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
