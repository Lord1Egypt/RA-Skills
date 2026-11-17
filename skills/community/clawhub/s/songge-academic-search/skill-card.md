## Description:

A Chinese-language academic search assistant that queries OpenAlex, Semantic Scholar, Crossref, arXiv, and PubMed, enriches paper metadata, and exports citations in text, JSON, BibTeX, RIS, or Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingsunzhang2026-oss](https://clawhub.ai/user/kingsunzhang2026-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, researchers, and developers use this skill to search academic literature across OpenAlex, Semantic Scholar, Crossref, arXiv, and PubMed, enrich paper metadata, and export citations or result files for literature review and writing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an optional Semantic Scholar API key in a way that server security guidance flags as unsafe.

Mitigation: Run without the API key for normal use; if a key is required, treat it as a secret and avoid shared shells, shell history, logs, and process listings until credential handling is fixed.

Risk: The skill installs Python dependencies with broad version ranges rather than pinned or locked versions.

Mitigation: Install in an isolated virtual environment and pin or lock dependencies before shared, repeatable, or production use.

Risk: The skill can write citation outputs and download PDFs to user-specified paths.

Mitigation: Use only output files and PDF download directories that are explicitly intended for the run, and review paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingsunzhang2026-oss/skills/songge-academic-search)
- [Publisher profile](https://clawhub.ai/user/kingsunzhang2026-oss)
- [Usage guide](references/readme.md)
- [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- [OpenAlex API](https://api.openalex.org)
- [DOI resolver](https://doi.org/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, BibTeX, RIS, files, shell commands, configuration guidance]

**Output Format:** [CLI output, Markdown, JSON, BibTeX, RIS, and optional written result or PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results can be filtered by source, result count, year, date range, author, citation count, arXiv category, publication type, and output path.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
