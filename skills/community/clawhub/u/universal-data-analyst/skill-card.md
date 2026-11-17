## Description:

Universal Data Analyst loads, profiles, validates, and analyzes supported data files by generating LLM-guided analysis plans, Python scripts, charts, and HTML/Markdown reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamaz49](https://clawhub.ai/user/yamaz49)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to inspect uploaded datasets, select appropriate analysis methods, generate data quality reports and analysis scripts, and produce narrative reports with charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or caller-supplied Python analysis scripts may execute unsafe or unintended behavior.

Mitigation: Review generated scripts before execution and run them in a sandbox or disposable environment.

Risk: Database analysis can expose more data than intended when broad credentials are used.

Mitigation: Use read-only, least-privilege database credentials and restrict access to the specific data needed for the analysis.

Risk: Dataset samples or prompts may be sent to external LLM providers during analysis planning and report generation.

Mitigation: Avoid sending sensitive data samples to external LLMs unless the provider and data handling path are approved.

Risk: Arbitrary local paths used for chart or script inputs can create file access risk.

Mitigation: Use trusted, scoped input and output directories and review paths before running the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yamaz49/skills/universal-data-analyst)
- [README](artifact/README.md)
- [Skill documentation](artifact/SKILL.md)
- [Quick reference](artifact/quick_reference.md)
- [Flow health monitor guide](artifact/FLOW_HEALTH_MONITOR_GUIDE.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, Python code, shell commands, charts, and HTML/Markdown report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates timestamped session directories with prompts, validation reports, generated analysis scripts, charts, and final reports.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
