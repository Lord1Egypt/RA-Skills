## Description:

Search, analyze, and summarize peer-reviewed academic papers from open access sources. Provides credibility scoring, visualization, timeline generation, and figure extraction for top papers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcheng67](https://clawhub.ai/user/jcheng67)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and technical users use this skill to search open access academic databases, rank papers with credibility scoring, summarize top results, generate field timelines, and optionally extract figures from PDFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary PDF URLs and write downloaded content locally without clear size or type limits.

Mitigation: Use the skill only with trusted research sources, run downloads in a restricted environment, and enforce PDF type, size, and storage limits before deployment.

Risk: Downloaded PDFs may be processed by local PDF extraction tools.

Mitigation: Process PDFs in a sandbox or container with patched PDF tooling and no access to sensitive local files.

Risk: Research queries and metadata requests may be sent to third-party academic APIs.

Mitigation: Use non-sensitive research queries and review configured API sources before enabling the skill.

Risk: The README includes a placeholder Git install command rather than a verified source repository.

Mitigation: Install only from the validated ClawHub artifact or a verified repository and pinned revision.

## Reference(s):

- [Scholar Research - API References](references/apis.md)
- [ClawHub Skill Page](https://clawhub.ai/jcheng67/skills/scholar-research)
- [arXiv API Documentation](https://arxiv.org/help/api)
- [NCBI E-utilities Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25497/)
- [OpenAlex Documentation](https://docs.openalex.org/)
- [Crossref REST API Documentation](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, configuration, guidance]

**Output Format:** [Markdown-style research reports with optional JSON output and optional downloaded or extracted PDF figure files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked top papers, 0-100 credibility scores, citation counts, summaries, methodology notes, text timeline visualizations, and configurable source and scoring settings.]

## Skill Version(s):

1.0.0 (source: release evidence, pyproject.toml, config.json, _meta.json, and src/scholar_research/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
