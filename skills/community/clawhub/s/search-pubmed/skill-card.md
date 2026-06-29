## Description: <br>
Search biomedical literature on PubMed via NCBI E-Utilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ki-ngian](https://clawhub.ai/user/ki-ngian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, clinicians, and developers use this skill to search PubMed and other NCBI databases for biomedical papers, PMID records, article metadata, and abstracts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Biomedical search terms, PMIDs, and optional NCBI email or API key values are sent to NCBI. <br>
Mitigation: Avoid sensitive patient, proprietary, or confidential project details in queries and only provide NCBI credentials when appropriate for the search. <br>
Risk: Search output may be incomplete if a query is too narrow, uses the wrong NCBI database, or returns no PubMed results. <br>
Mitigation: Broaden or split searches, try synonyms and field qualifiers, and cross-check relevant external biomedical databases before treating a gap as conclusive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ki-ngian/skills/search-pubmed) <br>
- [Server-resolved GitHub source](https://github.com/Ki-ngian/claude_skills/tree/main/search-pubmed) <br>
- [NCBI Entrez Query Syntax Reference](references/entrez-help.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text search results with optional Markdown guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PMID links, article titles, authors, journal/source, publication dates, DOI values, hit counts, and optional abstracts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
