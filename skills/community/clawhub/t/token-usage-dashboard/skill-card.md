## Description:

Token Usage Dashboard helps agents summarize local CodexBar usage and cost data, generate per-model views, detect spikes, and produce local dashboard or report artifacts for Codex and Claude usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bkes994408-cmd](https://clawhub.ai/user/bkes994408-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, FinOps users, and team administrators use this skill to inspect local CodexBar cost logs, identify model usage and spending spikes, and generate local dashboards or scheduled reports for budgeting and governance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose or persist detailed local prompt, user, project, and usage data through dashboard and report outputs.

Mitigation: Avoid feeding logs that contain prompts, secrets, customer data, or sensitive identifiers unless you control the generated files and their storage location.

Risk: Default output examples use temporary paths that may be less private on shared machines.

Mitigation: Use private output directories for HTML, JSON, CSV, and report history files, and restrict operating-system access to those files.

Risk: Viewer and RBAC settings in generated dashboards should not be treated as a strong security boundary.

Mitigation: Apply external access controls before sharing dashboards or reports, and review outputs before distributing them.

Risk: The artifact includes broader dashboard and reporting behavior than a simple model-cost summary.

Mitigation: Install and run it only when the broader local dashboard, reporting, tenant, alert, or cost-control features are intended.

## Reference(s):

- [CodexBar CLI quick ref](references/codexbar-cli.md)
- [Token Usage Dashboard README](README.md)
- [Tenant configuration example](docs/TENANT_CONFIG_EXAMPLE.json)
- [Alert configuration example](docs/ALERT_CONFIG_EXAMPLE.json)
- [Cost control configuration example](docs/COST_CONTROL_CONFIG_EXAMPLE.json)
- [Report scheduler configuration example](docs/REPORT_SCHEDULER_EXAMPLE.json)
- [ClawHub skill page](https://clawhub.ai/bkes994408-cmd/skills/token-usage-dashboard)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts may include HTML dashboards, JSON summaries, and CSV reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports local CodexBar cost input, optional pre-exported JSON, configurable alert and tenant settings, and scheduled report output.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
