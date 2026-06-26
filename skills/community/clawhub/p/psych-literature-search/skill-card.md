## Description: <br>
Searches and organizes academic literature on a given topic or research question using PubMed and Semantic Scholar, then produces structured literature tables with abstracts, bilingual keywords, citation information, publication types, and research-variable definitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agjvsxgm](https://clawhub.ai/user/agjvsxgm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, students, and knowledge workers use this skill to search PubMed and Semantic Scholar for literature on a topic and organize results into review-ready Markdown tables. It supports literature reviews by collecting metadata, abstracts, citation counts, publication types, bilingual keywords, variable definitions, operational definitions, and APA-style references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Documentation inconsistently mentions optional Web of Science and Springer credentials even though the current implementation evidence centers on PubMed and Semantic Scholar. <br>
Mitigation: Use the no-key PubMed and Semantic Scholar workflow unless the publisher updates the documentation and scripts to clearly explain how any optional provider credentials are handled. <br>
Risk: Literature queries and retrieved metadata are sent to external public research APIs, and abstracts may be translated or formatted by an AI system. <br>
Mitigation: Avoid sensitive or private search topics when that disclosure is unacceptable, and review translated abstracts and extracted variable definitions against source records before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agjvsxgm/psych-literature-search) <br>
- [API reference](references/api_reference.md) <br>
- [Output templates](references/output_templates.md) <br>
- [PubMed E-utilities esearch endpoint](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi) <br>
- [Semantic Scholar paper search endpoint](https://api.semanticscholar.org/graph/v1/paper/search) <br>
- [JCR journal browser](https://jcr.clarivate.com/jcr/browse-journals) <br>
- [SCImago Journal Rank](https://www.scimagojr.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and narrative report sections; helper scripts return JSON search results for agent processing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include literature metadata, DOI or source links, abstracts, Chinese abstract translations, citation counts, publication types, research-variable definitions, operational definitions, journal-level notes, synthesis bullets, and APA 7 references.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
