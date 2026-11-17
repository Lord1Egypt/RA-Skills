## Description:

Breaks a technology into first- and second-level branches, prepares keywords and search queries, counts patents, and produces an Excel-compatible breakdown table.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Patent analysts use this skill as an initial step in patent landscape and navigation projects to organize a technology into branches, define search terms, and estimate patent counts for each branch.

### Deployment Geography for Use:

Global; the described patent coverage includes China, the United States, Europe, Japan, South Korea, and WIPO.

## Known Risks and Mitigations:

Risk: Credential handling needs security fixes.

Mitigation: Store keys securely, do not share them in chat, and use a spending-limited key.

Risk: Cache writes need stronger path containment.

Mitigation: Prefer a corrected release that contains cache paths.

Risk: Spreadsheet exports need formula-safe handling.

Mitigation: Import CSV columns as text and review exported data before reuse.

## Reference(s):

- [Search workflow](references/search-workflow.md)
- [Query construction](references/query-construction.md)
- [PatentMax API reference](references/api-reference.md)
- [PatentMax API platform](https://api.ip930.com)

## Skill Output:

**Output Type(s):** [text, guidance, CSV data]

**Output Format:** [Excel-compatible CSV table with a technology branch hierarchy, keywords, search queries, and patent counts.]

**Output Parameters:** [First- and second-level technology branches.]

**Other Properties Related to Output:** [Includes Chinese keywords and, when needed, English keywords and IPC references.]

## Skill Version(s):

1.0.2 (source: skill frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
