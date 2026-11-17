## Description:

Converts markdown SQL query collections into BI dashboard specifications, chart plans, UI scaffolds, and optional service bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bamboo9805](https://clawhub.ai/user/bamboo9805)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analytics engineers use this skill to convert SQL query collections into BI prototypes, including parsed query catalogs, inferred semantics, chart recommendations, dashboard layouts, UI scaffolds, and service bundles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated dashboards have review-worthy browser security risks before use with untrusted SQL or real BI data.

Mitigation: Review generated web assets before sharing or deployment, and treat untrusted SQL-derived content as unsafe until reviewed.

Risk: The generated service frontend needs patching before use with untrusted content.

Mitigation: Patch or avoid the generated service frontend until HTML injection is fixed.

Risk: Generated frontend assets may rely on externally loaded ECharts.

Mitigation: Pin or vendor ECharts with integrity checking before deployment.

Risk: Generated services may be unsafe to connect directly to real data with permissive defaults.

Mitigation: Restrict CORS before connecting generated services to real datasets.

Risk: Environment setup commands may modify shell configuration or install Python packages.

Mitigation: Review commands that modify ~/.zshrc or install dependencies before running them.

## Reference(s):

- [SQL Style Guide](references/sql_style.md)
- [Chart Rules](references/chart_rules.md)
- [Dashboard Layout Rules](references/layout_rules.md)
- [Install Python 3.11](references/install_python311.md)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with generated JSON artifacts, Python service code, static UI files, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces query catalogs, semantic catalogs, chart plans, dashboard specs, UI scaffolds, and optional backend/frontend service bundles.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
