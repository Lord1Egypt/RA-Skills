## Description:

AI monitoring for construction sites and IT infrastructure: dashboards, alerts, incident playbooks, photo reports, SLA and capacity control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raaipro](https://clawhub.ai/user/raaipro)

### License/Terms of Use:

MIT-0

## Use Case:

CTOs, SREs, DevOps leads, operations leads, and construction site managers use this skill to turn supplied infrastructure, incident, SLA, business-impact, and photo context into operational dashboards, alerts, playbooks, reports, post-mortems, and capacity plans.

### Deployment Geography for Use:

Global; artifact defaults and examples are primarily Russian-language and use RUB business-impact examples.

## Known Risks and Mitigations:

Risk: The security review found broad production-changing incident commands without strong approval or scoping controls.

Mitigation: Use the skill as an advisory SRE/reference package and require a human to review the exact target and command before any shell, database, Docker, Kubernetes, firewall, or rollback action.

Risk: The security review says the included install, build, and smoke-test scripts may need repair before use.

Mitigation: Inspect and test the scripts in a disposable environment before installation, and avoid unattended deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raaipro/skills/raai-ai-monitor-pro)
- [README](artifact/README.md)
- [Configuration template](artifact/config.yaml)
- [Onboarding guide](artifact/docs/onboarding.md)
- [ROI guide](artifact/docs/roi.md)
- [Anti-fail guide](artifact/docs/anti-fail.md)
- [Quick-start examples](artifact/examples/quick-start.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text operational reports with tables, checklists, YAML configuration snippets, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory outputs depend on user-supplied infrastructure, SLA, revenue, ownership, and incident context; production-changing commands require human review before execution.]

## Skill Version(s):

3.5.3 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
