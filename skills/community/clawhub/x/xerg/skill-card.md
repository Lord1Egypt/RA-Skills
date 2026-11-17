## Description:

Audits AI agent runtime spending, attributes costs, and identifies evidence-backed opportunities to reduce waste.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xerg](https://clawhub.ai/user/xerg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Xerg to audit AI agent runtime spend, assess detector and pricing coverage, investigate supported waste findings, and compare costs after changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pinned, non-open-source npm CLI can read approved local AI runtime logs or databases.

Mitigation: Review the selected data sources and package before granting separate permission to fetch the CLI and inspect local evidence.

Risk: Remote collection or a hosted push could expose runtime information outside the local machine.

Mitigation: Approve the exact remote host and evidence paths separately; keep local audit, hosted pairing, and upload as distinct approvals, and preview push data with a dry run.

Risk: Estimated or unpriced runtime spending may be mistaken for an authoritative provider bill.

Mitigation: Report pricing and detector coverage, separate neutral signals from waste findings, and avoid presenting modeled costs as invoice totals.

## Reference(s):

- [Xerg documentation](https://xerg.ai/docs)
- [Xerg skill documentation](https://xerg.ai/skill.md)
- [Xerg CLI package](https://www.npmjs.com/package/@xerg/cli)
- [Hermes analysis guide](https://xerg.ai/docs/hermes-analysis)
- [ClawHub skill listing](https://clawhub.ai/xerg/skills/xerg)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries and CLI commands; JSON audit reports when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spend estimates depend on pricing and detector coverage; findings and neutral signals remain distinct.]

## Skill Version(s):

0.35.5 (source: ClawHub release metadata; reviewed CLI pin: 0.35.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
