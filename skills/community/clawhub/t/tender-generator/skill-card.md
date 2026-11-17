## Description:

Tender Generator Pro helps an agent collect project and bidder information, extract tender details from text or Word documents, generate DOCX bid-document packages, validate required fields, and create timestamped ZIP deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mama1234421](https://clawhub.ai/user/mama1234421)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement and proposal teams use this skill to collect bid information, extract project details, generate standardized tender documents, run completeness checks, and package bid materials for human review before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tender inputs and generated archives may contain bank, pricing, company, and representative details.

Mitigation: Process materials in an approved local workspace, restrict access to info.json and output ZIP files, and remove or retain them according to organizational data-handling policy.

Risk: Generated bid documents may contain incorrect extracted values, missing placeholders, or materials that still require signatures, stamps, or formal review.

Mitigation: Run the built-in validation path, review every generated document before submission, verify technical parameters against the tender requirements, and replace required signature or stamp materials manually.

Risk: Document generation depends on local Python and python-docx setup and may need template-generation fixes in some environments.

Mitigation: Confirm python3 and python-docx are installed, generate a small test package first, and inspect the output documents before using the skill on production tender data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mama1234421/skills/tender-generator)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts include JSON input files, DOCX bid documents, validation reports, and ZIP packages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and python-docx for local document generation; outputs may contain tender, pricing, company, banking, and representative details.]

## Skill Version(s):

3.0.0 (source: server release evidence and artifact _meta.json; README/SKILL history released 2026-08-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
