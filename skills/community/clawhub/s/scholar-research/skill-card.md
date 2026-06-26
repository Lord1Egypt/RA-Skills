## Description: <br>
Search, analyze, and summarize peer-reviewed academic papers from open access sources with credibility scoring, visualization, timeline generation, and figure extraction for top papers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jcheng67](https://clawhub.ai/user/jcheng67) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, students, and technical users use this skill to find academic papers, rank them with configurable credibility scores, summarize key methods, and review field trends from open access sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries and metadata are sent to external academic APIs. <br>
Mitigation: Avoid confidential research topics unless sharing queries and metadata with those services is acceptable. <br>
Risk: PDF download and figure extraction may process files from unknown sources. <br>
Mitigation: Run PDF processing in a constrained environment and install only from the reviewed artifact or a verified repository. <br>
Risk: Credibility scores are heuristic and may overstate paper quality when metadata is missing or incomplete. <br>
Mitigation: Review source papers, preprint status, citations, and retraction signals before relying on ranked results. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jcheng67/scholar-research) <br>
- [API references](references/apis.md) <br>
- [arXiv API documentation](https://arxiv.org/help/api) <br>
- [NCBI E-utilities documentation](https://www.ncbi.nlm.nih.gov/books/NBK25497/) <br>
- [OpenAlex documentation](https://docs.openalex.org/) <br>
- [Crossref REST API documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, analysis, configuration, shell commands] <br>
**Output Format:** [Markdown-style research summaries with ranked paper lists, score breakdowns, timelines, credibility distributions, and optional extracted figure file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries academic APIs, can use configurable scoring weights and source settings, and may download or process PDFs when figure extraction is enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
