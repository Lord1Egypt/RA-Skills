## Description:

Guides Chinese-speaking users through a three-stage workflow to build a RACI responsibility matrix for quality activities without assigning responsibilities on their behalf.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duding-engicool](https://clawhub.ai/user/duding-engicool)

### License/Terms of Use:

MIT-0

## Use Case:

Quality managers, project managers, and process owners use this skill to gather activities, roles, and user-confirmed RACI assignments for quality workflows such as audits, complaints, changes, and CAPA. It helps organize those inputs into a reviewable responsibility matrix with rule checks for accountability gaps and conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may enter sensitive organizational role or responsibility details while building the matrix.

Mitigation: Review data sensitivity before use and avoid entering sensitive organizational details unless they are appropriate for the generated matrix.

Risk: The generated RACI matrix may be mistaken for formal authorization or final organizational approval.

Mitigation: Treat the matrix as a review artifact and confirm responsibilities against enterprise authorization and governance processes before adoption.

Risk: Incomplete or uncertain assignments can reduce accountability traceability.

Mitigation: Keep unresolved cells explicitly marked as pending enterprise input and revisit them before finalizing the matrix.

## Reference(s):

- [Server-resolved GitHub repository](https://github.com/duding-engicool/skill-raci-matrix)
- [ClawHub skill page](https://clawhub.ai/duding-engicool/skills/skill-raci-matrix)
- [ClawHub publisher profile](https://clawhub.ai/user/duding-engicool)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown containing a RACI matrix, validation notes, and usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matrix content is based on user-provided activities, roles, and RACI cell assignments; unresolved items may be marked pending enterprise input.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
