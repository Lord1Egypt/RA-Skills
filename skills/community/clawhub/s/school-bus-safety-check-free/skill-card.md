## Description:

Checks copied school-bus daily inspection and safety-log tables locally for six record-consistency issues, with line-cited findings and no conclusion when required material is missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

School safety administrators and school-bus fleet operators use this skill to review monthly school-bus operation and inspection records before filing, audits, incident review, or corrective follow-up. It helps identify table-level gaps, duplicate entries, expired driver qualifications, arithmetic mismatches, and blank or malformed fields without treating the output as an official compliance determination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output may be mistaken for an official school-bus safety or compliance determination.

Mitigation: Treat results as a record-consistency aid only; have qualified staff review source records and applicable regulatory requirements before decisions or filings.

Risk: The free version omits several checks, including overload detection, missing attendant handoff, non-fixed-route operation, and vehicle inspection-validity coverage.

Mitigation: Review the reported withheld checks and perform those checks separately before relying on the record package.

Risk: Incorrect, incomplete, or non-Chinese-header input tables can lead to insufficient-input results or missed issues.

Mitigation: Provide the full table with recognized headers and source rows, then review the line-cited evidence for each finding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/school-bus-safety-check-free)
- [Packaged skill instructions](artifact/SKILL.md)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable text or structured JSON containing findings, summaries, executed checks, withheld checks, and source-line evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally over provided school-bus record text; insufficient input returns missing-material guidance instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
