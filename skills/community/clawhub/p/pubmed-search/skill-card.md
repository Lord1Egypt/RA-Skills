## Description:

Search PubMed for abstracts, with automatic full-text retrieval for PMC open-access articles, covering both open-access and non-open-access biomedical literature without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[steve33-doc](https://clawhub.ai/user/steve33-doc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to search PubMed, retrieve article metadata and abstracts, and fetch available PMC open-access full text for literature review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, PMIDs, and related parameters are sent to external NCBI and PMC services.

Mitigation: Avoid submitting confidential patient information, proprietary drug targets, or sensitive unpublished research topics unless that disclosure is acceptable.

Risk: Non-open-access articles return abstracts and metadata only, which can make literature review output incomplete if treated as full text.

Mitigation: Check the open-access/full-text status in the skill output and use publisher or institutional access when full text is unavailable.

Risk: Large query batches can run into public NCBI service rate limits or recommended usage windows.

Mitigation: Keep batching conservative and rely on the skill's built-in delay when querying public NCBI endpoints.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/Steve33-doc/pubmed-search)
- [ClawHub skill page](https://clawhub.ai/steve33-doc/skills/pubmed-search)
- [NCBI E-utilities documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- [NCBI E-utilities API base](https://eutils.ncbi.nlm.nih.gov/entrez/eutils)
- [NCBI PMC ID Converter](https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/)
- [PMC OAI-PMH GetRecord API](https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/GetRecord)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown and terminal text containing PubMed query results, article metadata, abstracts, open-access full-text availability, and JavaScript API usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include PMIDs, DOI values, author lists, journal metadata, abstracts, and PMC open-access full-text status.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
