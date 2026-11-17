## Description:

Converts Tsinghua thesis Word DOCX documents into thuthesis LaTeX projects and compiled PDFs, with support for chapters, abstracts, figures, tables, references, acknowledgements, resumes, and AI-assisted quality review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chao1208](https://clawhub.ai/user/chao1208)

### License/Terms of Use:

MIT-0

## Use Case:

Students, researchers, and thesis support teams use this skill to normalize Tsinghua thesis DOCX drafts into a thuthesis-compatible LaTeX project and PDF. Developers or agent operators can also use it to extract document structure, build intermediate JSON, render LaTeX, and review conversion quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can fetch or update a mutable remote thuthesis template.

Mitigation: Use a pinned thuthesis release or a reviewed local THUTHESIS_DIR, and review template changes before running conversion workflows.

Risk: LaTeX compilation executes on user-controlled thesis content.

Mitigation: Compile only in a contained workspace with restricted privileges, and avoid processing untrusted DOCX files.

Risk: Packaged thesis samples and generated outputs may contain personal or student information.

Mitigation: Remove private thesis documents, real student data, and generated outputs from public packages; use sanitized samples when examples are needed.

## Reference(s):

- [thu-thesis ClawHub Skill Page](https://clawhub.ai/chao1208/skills/thu-thesis)
- [thuthesis GitHub Project](https://github.com/tuna/thuthesis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands plus generated JSON, LaTeX project files, PDF output, and evaluation reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces intermediate raw, struct, and parsed JSON files; renders a thuthesis LaTeX project; compiles thesis.pdf when TeX tooling is available.]

## Skill Version(s):

1.5.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
