## Description: <br>
Semantic literature discovery and synthesis across arXiv/OpenAlex/PubMed (and optional Google Scholar adapters). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rogerrrr18](https://clawhub.ai/user/Rogerrrr18) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, developers, and technical users use this skill to retrieve, rank, and synthesize reading lists for scientific, medical, AI, engineering, and interdisciplinary research topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries are sent to external literature services, including arXiv, OpenAlex, PubMed, and optional Scholar-capable adapters. <br>
Mitigation: Use queries that are appropriate for external services and avoid confidential or sensitive research topics unless organizational policy allows it. <br>
Risk: Optional HTML export writes report files to a local path chosen by the user or generated from the query. <br>
Mitigation: Review the export path before using `--export-html` and inspect generated reports before sharing them. <br>
Risk: Generated reading lists may combine preprints with peer-reviewed literature and may omit important papers. <br>
Mitigation: Cross-check critical recommendations against source links, DOI or citation metadata, and domain expertise; include the documented preprint caution for biomedical or clinical queries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Rogerrrr18/semantic-paper-radar) <br>
- [arXiv API endpoint](http://export.arxiv.org/api/query) <br>
- [OpenAlex Works API](https://api.openalex.org/works) <br>
- [NCBI Entrez PubMed E-utilities](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, HTML files] <br>
**Output Format:** [JSON search results, Markdown synthesis reports, and optional local HTML export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include paper metadata, links, citation counts where available, ranked reading lists, timelines, thematic threads, and suggested reading order.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
