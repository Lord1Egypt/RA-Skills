## Description:

Helps quality engineers and MRB leaders standardize nonconforming product disposition, distinguish rework, repair, concession, downgrade, and scrap decisions, and generate nonconformance disposition forms and MRB records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers and MRB facilitators use this skill to classify nonconforming materials, select a disposition path, document approvals and reinspections, and produce practical text or Markdown records for review and audit evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill text references running scripts/build_report.py, but that script is not included in the artifact.

Mitigation: Review the installed workspace before allowing command execution, and only run scripts/build_report.py after verifying the file exists and is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-nonconformance-handling)
- [Server-resolved GitHub provenance](https://github.com/duding-engicool/skill-nonconformance-handling)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text and Markdown documents with concise process guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates nonconformance disposition forms and MRB records; referenced local shell commands should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
