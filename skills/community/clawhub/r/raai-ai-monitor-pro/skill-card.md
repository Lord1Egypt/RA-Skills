## Description: <br>
AI monitoring for construction sites and IT infrastructure: dashboards, alerts, incident playbooks, photo reports, SLA and capacity control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raaipro](https://clawhub.ai/user/raaipro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, CTOs, SREs, DevOps leads, and construction managers use this skill to turn infrastructure or site status inputs into dashboards, alerts, incident response playbooks, SLA reporting, capacity planning, photo reports, and executive summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident playbooks include production-impacting diagnostic and remediation commands. <br>
Mitigation: Require explicit human confirmation before executing commands, verify host and service targets, and begin with read-only diagnostics. <br>
Risk: Operational reports and notifications may contain sensitive customer, incident, revenue, infrastructure, or site information. <br>
Mitigation: Redact sensitive data before sharing reports or sending Slack and Telegram notifications. <br>
Risk: The server security verdict is suspicious because broad prompts can create unclear confirmation boundaries for production response. <br>
Mitigation: Review outputs before use in production, keep an accountable incident commander in the loop, and validate unsupported marketplace capability tags before enabling integrations. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/raaipro/raai-ai-monitor-pro) <br>
- [Publisher profile](https://clawhub.ai/user/raaipro) <br>
- [README](README.md) <br>
- [Onboarding guide](docs/onboarding.md) <br>
- [ROI guide](docs/roi.md) <br>
- [Limits and anti-fail guide](docs/anti-fail.md) <br>
- [Quick start examples](examples/quick-start.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, tables, checklists, YAML configuration examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided infrastructure, incident, SLA, business-impact, and site-photo context; optional Slack, Telegram, Prometheus, Grafana, and PagerDuty integrations require explicit configuration.] <br>

## Skill Version(s): <br>
3.5.3 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
