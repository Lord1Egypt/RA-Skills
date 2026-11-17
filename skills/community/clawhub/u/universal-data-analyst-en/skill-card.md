## Description:

Performs LLM-driven data analysis by loading and validating datasets, selecting methods, generating Python analysis scripts, executing them, and producing reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yamaz49](https://clawhub.ai/user/yamaz49)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to automate exploratory and goal-directed analysis of uploaded datasets, including data loading, quality checks, method selection, script generation, execution, and HTML/Markdown reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Python may run with broad local permissions.

Mitigation: Review generated scripts before execution and run analyses in a sandbox or container.

Risk: Database analysis can expose data through overly broad credentials.

Mitigation: Use read-only, least-privilege database credentials.

Risk: Saved prompts and reports may contain sensitive data.

Mitigation: Delete or secure saved session artifacts after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yamaz49/skills/universal-data-analyst-en)
- [Universal Data Analyst README](artifact/README.md)
- [Universal Data Analyst Skill Guide](artifact/SKILL.md)
- [Quick Reference](artifact/quick_reference.md)
- [Flow Health Monitor Guide](artifact/FLOW_HEALTH_MONITOR_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, HTML reports, JSON validation/session files, Python analysis scripts, charts, and saved LLM prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes session artifacts to analysis output directories; generated Python should be reviewed before execution.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
