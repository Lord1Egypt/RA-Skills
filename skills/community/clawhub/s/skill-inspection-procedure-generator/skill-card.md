## Description:

Generates Chinese product inspection procedure Word documents from user-provided control plans, test reports, drawings, and product descriptions, with structured data validation and missing-item handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers, supplier quality teams, and manufacturing documentation owners use this skill to draft incoming inspection procedures, IQC inspection specifications, and product quality inspection standards from product evidence. It helps structure inspection data, identify missing required fields, and generate a .docx draft for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated inspection procedures may look authoritative while containing weakly validated or unverified technical defaults.

Mitigation: Treat outputs as drafts and independently confirm product standards, sampling plans, AQL values, environmental conditions, and inspection items before operational use.

Risk: The document-generation script requires python-docx, introducing dependency supply-chain risk if installed casually.

Mitigation: Install python-docx from a trusted, pinned dependency source before running the script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-inspection-procedure-generator)
- [Source repository](https://github.com/duding-engicool/skill-inspection-procedure-generator)
- [Data schema reference](references/data-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with JSON input data and generated Word .docx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review of generated inspection documents before operational use; the document generator depends on python-docx.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
