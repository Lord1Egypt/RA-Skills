## Description:

Guides evidence-based audits of claimed AI identity and output provenance using records, signatures, and platform logs rather than an AI's self-description.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

All Rights Reserved

## Use Case:

Teams and individuals reviewing AI-generated content use this skill to collect and compare traceable records, assess claimed identities, and draft an audit opinion that states when evidence is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can write files while preparing an audit.

Mitigation: Limit writes to new reports and checklists; do not edit original evidence, logs, credentials, or source materials.

Risk: An identity conclusion could be overstated if supporting records are absent.

Mitigation: Base conclusions on verifiable platform records or signatures, and mark unsupported claims as insufficient evidence.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/traceability-audit-team)
- [Audit report template](references/audit-report-template.md)
- [Evidence-chain checklist](references/evidence-chain-checklist.md)
- [Standards reference map](references/standards-map.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown audit reports and evidence checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records evidence sources and uncertainty; uses supported, unsupported, or insufficient-evidence conclusions.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release; bundled files list older versions)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
