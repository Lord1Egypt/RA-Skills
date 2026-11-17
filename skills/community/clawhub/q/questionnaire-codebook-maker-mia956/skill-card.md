## Description:

Turn questionnaire items into clean research codebooks, scoring rules, reverse-scoring checks, variable names, and analysis-ready TSV/Markdown tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mia956](https://clawhub.ai/user/mia956)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and analysts use this skill to turn questionnaire items into codebooks, scoring rules, reverse-scoring checks, variable names, and analysis-ready tables for psychology, education, public-health, and social-science projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet-oriented TSV output can preserve questionnaire text that begins with formula characters when opened in Excel or similar tools.

Mitigation: Review or sanitize untrusted CSV fields before opening generated TSV files in spreadsheet software.

Risk: Questionnaire scoring can be misleading if item wording, reverse-scoring status, or clinical cutoffs are uncertain.

Mitigation: Use the source questionnaire or scale manual, mark uncertain reverse-scoring decisions, and avoid clinical cutoffs unless the user provides or requests verified source material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mia956/skills/questionnaire-codebook-maker-mia956)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TSV tables and optional generated Markdown/TSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional helper script reads CSV files and writes codebook.md and variable_map.tsv using Python standard-library modules.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
