## Description:

Searches PubMed and Semantic Scholar for academic literature, then organizes results into bilingual Markdown tables with abstracts, links, citation counts, publication types, variable definitions, and measurement instruments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agjvsxgm](https://clawhub.ai/user/agjvsxgm)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, students, and analysts use this skill to search scholarly literature on a topic, deduplicate and sort results, and produce bilingual literature review tables with variable definitions and APA references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or other credentials could be exposed if users follow insecure configuration guidance.

Mitigation: Use the skill only with non-confidential research topics, provide optional keys through environment variables or a managed secret store, and do not paste API keys into chat or store them in SKILL.md.

Risk: Documentation is inconsistent about whether Web of Science and Springer are supported by the current artifact.

Mitigation: Treat PubMed and Semantic Scholar as the implemented primary sources, and verify any Web of Science or Springer workflow before relying on it.

Risk: Journal metrics and journal-level claims are partially documented and may be stale.

Mitigation: Confirm quartiles, impact factors, and indexing status against JCR, SCImago, or institutional sources before using them for evaluation decisions.

## Reference(s):

- [API Reference](artifact/references/api_reference.md)
- [Output Templates](artifact/references/output_templates.md)
- [PubMed E-utilities esearch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi)
- [PubMed E-utilities efetch](https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi)
- [Semantic Scholar Paper Search API](https://api.semanticscholar.org/graph/v1/paper/search)
- [JCR Journal Browse](https://jcr.clarivate.com/jcr/browse-journals)
- [SCImago Journal Rank](https://www.scimagojr.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and tables, with JSON returned from helper scripts when executed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a Markdown report file on request; helper scripts query external scholarly APIs.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
