## Description:

Helps agents search free academic APIs for Chinese and English psychology literature, export bibliographic tables, and generate citations in common formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhan599](https://clawhub.ai/user/zhan599)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and academic writing assistants use this skill to find psychology and behavioral science papers, filter recent or highly cited work, export CSV bibliographies, and prepare APA, GB/T 7714, MLA, or Chicago citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and optional email addresses are sent to Semantic Scholar, OpenAlex, and CrossRef.

Mitigation: Use non-sensitive queries when possible, omit email unless needed for polite-pool behavior, and ensure users understand which public academic APIs receive requests.

Risk: Exported CSV files may contain untrusted metadata such as links or formula-like strings from external databases.

Mitigation: Open exports with spreadsheet protections enabled, disable external content and macros, and review suspicious links or formulas before sharing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhan599/skills/psychology-literature-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, files, guidance]

**Output Format:** [Markdown guidance with Python code examples; generated artifacts may be CSV or text citation files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform user-directed network queries to academic APIs and write CSV or text exports.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
