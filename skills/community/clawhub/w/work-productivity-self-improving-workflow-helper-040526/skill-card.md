## Description:

Create self-improving agent or team workflows that capture failures, extract lessons, update instructions, and verify improvements without uncontrolled drift.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent maintainers, prompt engineers, support operations teams, and skill authors use this skill to convert failures, review comments, corrections, or audits into narrow prompt, skill, checklist, test, documentation, or runbook improvements with replay validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit invocation may apply the workflow when the user did not intend durable process or instruction changes.

Mitigation: Use the skill when workflow improvement, prompt or runbook updates, or replay validation are intended, and review any durable update before applying it.

Risk: A proposed improvement could encode the wrong lesson or create uncontrolled behavioral drift.

Mitigation: Tie each update to a specific observed failure or correction, keep the change narrow and testable, and run a replay or focused validation before adoption.

Risk: Documentation-only guidance can be mistaken for a fully validated operational fix.

Mitigation: Require concrete acceptance criteria, a validation note, and an audit-friendly changelog entry for meaningful workflow changes.

## Reference(s):

- [Requirement Plan](artifact/references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-self-improving-workflow-helper-040526)
- [Self-Improving Agent Demand Signal](https://clawhub.ai/skills/self-improving-agent)
- [Proactive Agent Demand Signal](https://clawhub.ai/skills/proactive-agent)
- [Self-Improving Demand Signal](https://clawhub.ai/skills/self-improving)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with structured analysis, checklists, code snippets, configuration updates, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include durable prompt, skill, checklist, test, documentation, or runbook updates when relevant.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
