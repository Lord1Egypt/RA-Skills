## Description:

Query UniProt database for protein sequences, metadata, and search by criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hollyya](https://clawhub.ai/user/hollyya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and biomedical researchers use this skill to look up UniProt accessions and search proteins by gene, organism, function, disease, or annotation criteria. It helps agents return protein sequences, metadata, search results, and human-readable protein reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts UniProt over the network when running lookup or search workflows.

Mitigation: Review intended queries and ensure external UniProt API access is acceptable for the deployment environment.

Risk: Example scripts can save generated protein metadata and reports locally, including under ./tmp/uniprot by default.

Mitigation: Choose and review the output directory before execution, and inspect generated files before sharing or retaining them.

## Reference(s):

- [UniProt API Documentation](https://www.uniprot.org/api-documentation)
- [UniProt Query Fields Reference](references/query_fields.md)
- [UniProt Metadata Fields Reference](references/metadata_fields.md)
- [ClawHub Skill Page](https://clawhub.ai/hollyya/skills/uniprot-query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown guidance with Python snippets, UniProt REST query examples, JSON metadata, and text reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Example scripts may save JSON metadata and text report files under a configurable output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
