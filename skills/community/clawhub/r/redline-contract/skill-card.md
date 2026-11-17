## Description:

Review and redline DOCX contracts paragraph by paragraph with tracked changes, clause-level risk analysis, and draft comment responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipmunkrpa](https://clawhub.ai/user/chipmunkrpa)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, procurement, and contract-review users can use this skill to create paragraph-level review data, proposed replacement language, tracked-change amendments, and risk reports for DOCX contracts. It is especially relevant for privacy, security, data-processing, liability, AI, and other negotiated legal terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted DOCX files may expose unsafe XML or ZIP handling in the bundled parser.

Mitigation: Review contracts only from trusted sources or run the skill in a constrained workspace; harden XML parsing and reject suspicious DOCX archives before broad use.

Risk: Contract redlines and risk reports can affect legal positions if accepted without review.

Mitigation: Have qualified reviewers verify the generated review JSON, tracked changes, and risk report before relying on them.

## Reference(s):

- [Contract Review JSON Schema](references/review-json-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; generated review JSON and DOCX outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a tracked-changes amended DOCX, a risk-report DOCX, and a review JSON dataset when materialized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
