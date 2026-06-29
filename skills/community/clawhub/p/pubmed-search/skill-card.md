## Description: <br>
Search PubMed for article abstracts and metadata, with automatic PMC open-access full-text retrieval when available and no API key requirement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steve33-doc](https://clawhub.ai/user/steve33-doc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinicians, and developers use this skill to search biomedical literature, retrieve PubMed metadata and abstracts, and fetch PMC open-access full text when available for literature review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and PMIDs are sent to public NCBI/PMC services. <br>
Mitigation: Avoid sensitive or confidential queries and follow organizational data-handling rules before using the skill. <br>
Risk: Full text is available only for PMC open-access articles; other records provide abstracts and metadata only. <br>
Mitigation: Verify whether publisher or institutional access is needed for non-open-access articles. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/steve33-doc/skills/pubmed-search) <br>
- [Server-resolved source repository](https://github.com/Steve33-doc/pubmed-search) <br>
- [NCBI E-utilities documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/) <br>
- [NCBI E-utilities API](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [NCBI PMID-PMCID Converter](https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/) <br>
- [PMC OAI-PMH GetRecord API](https://pmc.ncbi.nlm.nih.gov/api/oai/v1/mh/GetRecord) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, terminal text output, and JavaScript API objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and network access to public NCBI/PMC services.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
