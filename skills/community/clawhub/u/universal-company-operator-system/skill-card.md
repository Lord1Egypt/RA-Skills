## Description:

A complete AI executive team for running, analyzing, or building companies, products, startups, creator brands, nonprofits, and internal initiatives by routing business requests to specialized operator roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwapupward-hub](https://clawhub.ai/user/gwapupward-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, founders, operators, and business teams use this skill to route broad or function-specific company requests into strategy, product, marketing, sales, operations, finance, customer success, analytics, design, legal/compliance, community, or night-shift planning workflows. It produces decision-ready plans, drafts, analyses, briefs, task lists, and recommendations for human review and execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad business-adjacent requests and produce wider routing than the user intended.

Mitigation: Use explicit /run commands or name the desired operator when a narrower response is needed.

Risk: Finance, legal, compliance, contract, and policy outputs may be mistaken for professional advice.

Mitigation: Treat these outputs as planning drafts or risk-spotting aids and review them with qualified professionals before acting.

Risk: Drafts or recommendations could imply irreversible actions such as publishing, spending money, deploying changes, sending messages, signing contracts, deleting data, or exposing secrets.

Mitigation: Keep generated artifacts in draft form, place unsafe or irreversible actions under Decisions Needed, and require explicit human approval and execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwapupward-hub/skills/universal-company-operator-system)
- [README](artifact/README.md)
- [Command console](artifact/COMMAND_CONSOLE.md)
- [Operating system layer](artifact/OPERATING_SYSTEM.md)
- [Multi-agent orchestration system](artifact/orchestration.md)
- [Night shift workflow](artifact/NIGHT_SHIFT.md)
- [Morning brief output contract](artifact/MORNING_BRIEF.md)
- [Night shift safety rules](artifact/SAFETY_RULES.md)
- [Operator manifest](artifact/operator_manifest.json)
- [Night shift manifest](artifact/night_shift_manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with structured plans, briefs, drafts, checklists, scripts, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft labels and Decisions Needed sections are used for actions requiring human approval.]

## Skill Version(s):

1.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
