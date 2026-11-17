## Description:

塔机台账与检测报告逐项核对，检查检测有效期覆盖、使用登记证与司机信号工证件、检测结论、同一设备编号重复登记、合计行逐列复核和字段合法性，并为结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External construction safety teams, equipment administrators, tower-crane rental staff, and site supervisors use this skill to check tower-crane ledger text before monthly reviews or safety inspections. It helps identify missing or inconsistent filing, inspection, operator-certificate, conclusion, duplicate-device, and total-row data without replacing professional or regulatory judgment.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Tower-crane ledgers may contain sensitive project and personnel certificate information.

Mitigation: Run the checker in a trusted local environment; server security evidence reports no network, credential, persistence, or hidden execution behavior in the inspected code.

Risk: The free version does not perform cross-table checks for in-use overdue cranes, stopped or dismantled cranes appearing in use records, unlicensed operation, jack-up or attachment acceptance gaps, or grouped remediation summaries.

Mitigation: Treat results as table-consistency triage for the stated six checks and require human review for withheld checks and safety-critical decisions.

Risk: The skill does not verify the authenticity of inspection reports, registration certificates, operator certificates, or original XLSX/PDF documents.

Mitigation: Validate source documents and certificate status through qualified personnel or authoritative regulatory channels before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/tower-crane-inspection-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Human-readable console text or structured JSON with executed checks, withheld checks, findings, source-line references, and missing-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided ledger text; findings are limited to the free-version checks and do not verify document authenticity.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
