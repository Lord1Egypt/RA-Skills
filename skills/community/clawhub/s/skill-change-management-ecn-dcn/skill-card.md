## Description:

This skill helps change engineers, project managers, and document control teams manage ECN/DCN changes by guiding impact analysis, review routing, verification planning, implementation cutover, and controlled change-record generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Employees in engineering, quality, project management, and document control use this skill to classify ECN versus DCN changes, gather required inputs, assess impacts, plan reviews and verification, manage cutover, and produce traceable controlled change records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ECN/DCN records may contain confidential product, supplier, customer, or approval information.

Mitigation: Use a dedicated output directory and apply the organization's normal access controls for generated records.

Risk: Generated records may be mistaken for formal approval or a replacement for PLM, ERP, or DCC workflows.

Mitigation: Treat the skill output as a drafting and controlled-record aid, with final authorization handled through the organization's approved change-management systems and approval process.

## Reference(s):

- [Server-resolved source repository](https://github.com/duding-engicool/skill-change-management-ecn-dcn)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-change-management-ecn-dcn)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text and Markdown change-record documents]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ECN/DCN change records for review circulation and archiving; missing required inputs are marked for completion.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
