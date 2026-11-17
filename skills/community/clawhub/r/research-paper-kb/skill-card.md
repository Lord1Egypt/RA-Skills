## Description:

Persistent cross-session knowledge base for research papers that ingests arXiv IDs, DOIs, or titles, extracts structured paper intelligence, appends entries to PAPERS.md, and keeps MEMORY.md updated.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ilkhamfy](https://clawhub.ai/user/ilkhamfy)

### License/Terms of Use:


## Use Case:

Developers, researchers, and research-focused agents use this skill to maintain a persistent literature knowledge base, add structured notes for papers, generate BibTeX entries, and review tracked papers across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper identifiers, DOIs, or free-text title searches may be sent to external academic metadata services.

Mitigation: Prefer exact arXiv IDs or DOIs and avoid sensitive free-text title searches when privacy matters.

Risk: Paper notes and research-overlap assessments are persisted in PAPERS.md and MEMORY.md.

Mitigation: Review local notes before sharing the workspace or committing generated knowledge-base files.

Risk: The artifact documents an HTTP arXiv API fallback, which may be unsuitable for sensitive use.

Mitigation: Use HTTPS metadata endpoints before relying on the skill for sensitive paper lookups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ilkhamfy/skills/research-paper-kb)
- [Project homepage from skill metadata](https://github.com/IlkhamFY/stch-botorch)
- [arXiv abstract pages](https://arxiv.org/abs/2310.12345)
- [Semantic Scholar Graph API](https://api.semanticscholar.org/graph/v1/paper/search)
- [DOI resolver](https://doi.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, API Calls, Guidance]

**Output Format:** [Markdown summaries with BibTeX code blocks and local Markdown file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or updates PAPERS.md and MEMORY.md; may call arXiv, Semantic Scholar, or DOI metadata services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
