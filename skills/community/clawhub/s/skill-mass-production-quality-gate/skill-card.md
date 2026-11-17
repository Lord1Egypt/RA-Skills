## Description:

Assists mass-production quality teams with containment and escalation decisions by generating standardized action cards and tracking boards for production exceptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality managers, supplier quality engineers, process quality engineers, and line quality leads use this skill to triage mass-production exceptions, define containment actions, decide escalation levels, and maintain a follow-up board. It is focused on production-stage containment and escalation, not NPI gate reviews, Safe Launch planning, 8D root-cause analysis, or formal approval signoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect or incomplete severity and escalation recommendations could cause missed containment steps or unnecessary production disruption.

Mitigation: Require the responsible quality owner to confirm severity, batch scope, customer exposure, containment status, and escalation level before executing actions or signing off.

Risk: Missing production details can produce an incomplete containment board.

Mitigation: Keep unknown values marked as pending and verify product, defect, batch, inventory, work-in-process, in-transit, and customer-side exposure before closure.

Risk: The package references generated .txt and Markdown report outputs, but the referenced report-rendering script is not included in the package.

Mitigation: Have the agent produce the plain-text and Markdown board directly and review the outputs for completeness before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-mass-production-quality-gate)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-mass-production-quality-gate)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown and plain text containing containment/escalation action cards, decision rationale, and a quality escalation tracking board]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include pending-field markers when production quality inputs are incomplete.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
