## Description:

Search biomedical literature on PubMed and other NCBI databases through NCBI E-Utilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ki-ngian](https://clawhub.ai/user/ki-ngian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to search biomedical literature, inspect PubMed IDs, and summarize article metadata from PubMed or related NCBI databases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, optional email address, and optional NCBI API key may be sent to NCBI through Biopython.

Mitigation: Avoid sensitive search terms or credentials unless sharing them with NCBI is acceptable; use a dedicated NCBI API key when needed.

Risk: The skill depends on the external Biopython package.

Mitigation: Install in a virtual environment and prefer a pinned Biopython version.

Risk: Broad trigger language may cause the skill to run for general biomedical or literature-search requests.

Mitigation: Narrow invocation rules if deployment should require explicit PubMed or literature-search intent.

## Reference(s):

- [NCBI Entrez Query Syntax Reference](references/entrez-help.md)
- [PubMed result links](https://pubmed.ncbi.nlm.nih.gov/PMID)
- [Server-resolved GitHub provenance](https://github.com/Ki-ngian/claude_skills/tree/main/search-pubmed)
- [ClawHub skill page](https://clawhub.ai/ki-ngian/skills/search-pubmed)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results include PMID, title, authors, source, publication date, DOI, and optional abstract text.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
