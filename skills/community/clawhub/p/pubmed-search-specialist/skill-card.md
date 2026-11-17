## Description:

Build complex Boolean query strings for precise PubMed/MEDLINE literature retrieval, including MeSH term mapping, Boolean query construction, advanced PubMed filters, citation searching, systematic review search strategy, and clinical query optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, librarians, and clinical evidence teams use this skill to turn biomedical research questions into reproducible PubMed/MEDLINE Boolean searches with MeSH terms, field tags, filters, and line-by-line strategy output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned or unnecessary Python dependencies can make local installation less reproducible.

Mitigation: Install in an isolated virtual environment and pin or remove requirements before deployment, following the security guidance in evidence.json.

Risk: Generated language, date, and study filters can encode protocol choices that may be inappropriate for a given review question.

Mitigation: Treat filters as user-directed choices, document the rationale, and confirm them against the review protocol before using the search.

Risk: MeSH terms and simplified static mappings may become outdated or incomplete.

Mitigation: Verify terms against the current MeSH Browser or NCBI MeSH reference before relying on the query for clinical or systematic review work.

## Reference(s):

- [MeSH Structure Guide](references/mesh-structure.md)
- [Boolean Query Examples](references/boolean-examples.md)
- [MeSH Browser](https://meshb.nlm.nih.gov/)
- [NCBI MeSH](https://www.ncbi.nlm.nih.gov/mesh)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with PubMed query strings, optional JSON output, and inline shell commands when running the packaged script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces copy-paste-ready PubMed searches, line-by-line search strategies, syntax validation notes, and assumptions or caveats when inputs are incomplete.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
