## Description:

AI-powered tool for searching and analyzing PubMed biomedical literature.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackkuo666](https://clawhub.ai/user/jackkuo666)

### License/Terms of Use:

MIT

## Use Case:

Researchers and literature reviewers use this skill to search PubMed, retrieve article metadata, generate abstract-based paper analysis, and download open-access PDFs when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recommended install paths include mutable remote code execution or unpinned package execution.

Mitigation: Prefer a reviewed local pip/venv installation path and pin or verify dependencies before use.

Risk: PubMed API keys and email addresses may appear in generated URLs, console output, or agent transcripts.

Mitigation: Avoid setting a PubMed API key unless higher rate limits are needed, and treat logs and transcripts as sensitive when credentials are configured.

Risk: Paper analysis is generated from available article metadata and abstracts, which may omit important study details.

Mitigation: Verify findings, limitations, and citations against the original papers before relying on the analysis.

## Reference(s):

- [PubMed E-utilities documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [NCBI account for PubMed API keys](https://www.ncbi.nlm.nih.gov/account/)
- [PubMed E-utilities API endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)
- [ClawHub skill page](https://clawhub.ai/jackkuo666/skills/pubmed-search-skill)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance, files]

**Output Format:** [Console text, JSON, Markdown, and downloaded PDF files when open access is available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save search results, analysis text, metadata, or PDFs to user-specified paths.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
