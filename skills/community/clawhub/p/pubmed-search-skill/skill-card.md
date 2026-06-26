## Description: <br>
AI-powered tool for searching and analyzing PubMed biomedical literature. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JackKuo666](https://clawhub.ai/user/JackKuo666) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, clinicians, and biomedical developers use this skill to search PubMed, retrieve article metadata by PMID, prepare literature analysis prompts, and access open-access full text when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A configured PubMed API key may appear in generated search URLs, command output, or logs. <br>
Mitigation: Treat outputs and logs as sensitive when PUBMED_API_KEY is set, and prefer redacting api_key values before sharing command output. <br>
Risk: The skill performs PubMed/NCBI network requests and may write local result or PDF files. <br>
Mitigation: Run it in an environment where outbound NCBI requests and local file writes are expected, and review output paths before saving results or PDFs. <br>


## Reference(s): <br>
- [PubMed E-utilities Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/) <br>
- [NCBI Account](https://www.ncbi.nlm.nih.gov/account/) <br>
- [PubMed E-utilities API Endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils) <br>
- [ClawHub Skill Page](https://clawhub.ai/JackKuo666/pubmed-search-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Console text, JSON, Markdown, saved Markdown or JSON files, and open-access PDF files when available.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Searches and metadata retrieval use PubMed E-utilities network requests; PDF download is limited to open-access articles.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
