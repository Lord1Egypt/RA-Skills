## Description:

Extract hazard codes and safety info from chemical safety datasheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Lab safety, compliance, hazard communication, and emergency response users can use this skill to extract GHS H-codes, P-codes, safety summaries, and PPE recommendations from SDS/MSDS-style chemical safety documents. Results should be reviewed against the source datasheet and applicable safety requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chemical safety outputs may be incomplete or inaccurate when the source SDS/MSDS content is missing, malformed, or outside the skill's documented scope.

Mitigation: Review the original datasheet, confirm extracted codes and PPE recommendations, and use professional safety guidance before acting on results.

Risk: The skill can execute a local Python helper and handle workspace files.

Mitigation: Run it in a sandboxed workspace, validate input and output paths, and keep generated outputs within the intended project directory.

Risk: The included scanner is simple and the artifact marks the skill as draft.

Mitigation: Treat results as triage or documentation support, then validate against authoritative SDS/MSDS content and applicable regulatory requirements.

## Reference(s):

- [Audit Reference](references/audit-reference.md)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/sds-msds-risk-scanner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown with extracted hazard codes, precautionary statements, safety summary, PPE recommendations, assumptions, risks, and next checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are a structured aid for reviewing SDS/MSDS content and are not a substitute for the source datasheet or professional safety guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
