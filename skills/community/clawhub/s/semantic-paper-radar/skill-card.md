## Description:

Semantic literature discovery and synthesis across arXiv/OpenAlex/PubMed (and optional Google Scholar adapters). Use when users ask for domain must-read papers, research trend mapping, paper recommendations, reading lists, or academic lineage/context for a topic in natural science, AI, engineering, medicine, or interdisciplinary research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rogerrrr18](https://clawhub.ai/user/rogerrrr18)

### License/Terms of Use:


## Use Case:

Researchers, developers, and technical readers use this skill to retrieve papers across arXiv, OpenAlex, and PubMed, then synthesize prioritized reading lists, timelines, theme threads, and next-step recommendations for a research topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries are sent to arXiv, OpenAlex, and PubMed.

Mitigation: Avoid confidential project names, private research plans, or sensitive biomedical details in queries.

Risk: Optional HTML export may include unsafe unescaped content from user queries or retrieved search results.

Mitigation: Avoid HTML export for untrusted topics or results until escaping is fixed; when exporting, write to a safe workspace path and inspect the file before opening it.

Risk: arXiv results can include unreviewed preprints, especially for biomedical or clinical topics.

Mitigation: Label arXiv entries as preprints and cross-check clinical or biomedical claims against peer-reviewed sources before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rogerrrr18/skills/semantic-paper-radar)
- [arXiv API query endpoint](http://export.arxiv.org/api/query)
- [OpenAlex Works API](https://api.openalex.org/works)
- [PubMed E-utilities ESearch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi)
- [PubMed E-utilities EFetch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON search results and Markdown research reports, with optional exported HTML files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are normally presented in Chinese unless the user asks for another language.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
