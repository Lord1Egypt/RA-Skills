## Description:

A POC war-room skill for ToB AI delivery that diagnoses POC status, tracks pass rate, classifies blockers, builds 48-hour closure plans, detects customer silence risk, and produces daily POC reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[william202404](https://clawhub.ai/user/william202404)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, project-management, and technical delivery teams use this skill to turn ToB POC facts into risk triage, blocker ownership, 48-hour action plans, customer follow-up moves, and contract-closing readiness signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI and report language are mostly Chinese, which may reduce usability for teams that require English-only workflows.

Mitigation: Confirm the intended users can review Chinese-language triage output or translate/adapt the report before relying on it operationally.

Risk: The skill provides POC delivery and sales guidance, not automatic customer outreach, contract execution, or authoritative business decisions.

Mitigation: Have responsible sales, project, and technical owners review the recommended actions against current customer facts before acting.

Risk: Industry heuristics and example outcomes could be mistaken for guarantees.

Mitigation: Treat examples and pass-rate patterns as planning signals only, and require concrete acceptance criteria and current blocker evidence for decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/william202404/skills/tob-poc-war-room)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables, checklists, and action items; the CLI prints reports to stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Visible Chinese-language UX and report text; supports interactive prompts and CLI flags for industry, objective, day, problems, pass rate, and silence days.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
