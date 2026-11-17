## Description:

Vietnam Education helps agents draft Vietnamese lesson plans, exams, worksheets, and answer checks aligned with CTGDPT 2018 and CV 7991, using web lookup guidance plus SymPy and Matplotlib helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trustydev212](https://clawhub.ai/user/trustydev212)

### License/Terms of Use:

MIT-0

## Use Case:

External educators and agents can use this skill to draft Vietnam-aligned lesson plans, assessment matrices, exams, worksheets, and answer-verification workflows for primary, lower-secondary, and upper-secondary classes.

### Deployment Geography for Use:

Global, for Vietnamese education contexts

## Known Risks and Mitigations:

Risk: Setup commands can affect the local environment through global npm installs or system-level Python package installation.

Mitigation: Install and run the skill in an isolated project environment or container with pinned dependencies and a Python virtual environment.

Risk: Formula and graph-expression workflows may execute unsafe or malformed input if taken directly from untrusted prompts.

Mitigation: Review, sanitize, and constrain expressions before passing them to the helper scripts.

Risk: Web searches may expose private exams, teacher materials, or student-related context.

Mitigation: Confirm before searching sensitive content and redact private or student-identifying details.

Risk: Generated educational content and answers may still be incorrect or mismatched to a required textbook edition or local policy.

Mitigation: Cross-check source curriculum materials, use the documented answer-verification workflow, and require educator review before classroom use.

## Reference(s):

- [CTGDPT 2018 Reference](references/ctgdpt-2018.md)
- [CV 7991 Exam, Lesson Plan, and Worksheet Templates](references/templates.md)
- [OpenClaw Viet Nam Community](https://zalo.me/g/lajsqc334jqc5fezevvo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated .docx, image, and JSON file workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Node.js and Python scripts for document creation, symbolic answer checks, and figure generation.]

## Skill Version(s):

3.0.0 (source: skill frontmatter); ClawHub release 1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
