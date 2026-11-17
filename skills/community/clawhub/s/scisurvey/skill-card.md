## Description:

SciSurvey helps agents generate systematic academic surveys and reviews using Sciverse literature search, citation tracing, reference checks, and multi-format export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liweixiaogui10](https://clawhub.ai/user/liweixiaogui10)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and developers use this skill to plan and draft structured academic literature surveys or reviews from a topic. It supports review-type selection, bilingual keyword planning, Sciverse retrieval, evidence mapping, citation integrity checks, and Markdown-first delivery with optional LaTeX, DOCX, or PDF export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The document export path may run local shell commands with unsanitized user-derived filenames.

Mitigation: Prefer Markdown output, use simple safe filenames, review generated commands, and require explicit approval before any file conversion runs.

Risk: The skill may create local review files during normal use.

Mitigation: Run the skill in an appropriate workspace and review generated files before sharing or publishing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liweixiaogui10/skills/scisurvey)
- [Project homepage](https://github.com/liweixiaogui10/Systematic_Survey_skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional LaTeX, DOCX, or PDF files and citation lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local review files; non-Markdown export may invoke local document-conversion tools.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
