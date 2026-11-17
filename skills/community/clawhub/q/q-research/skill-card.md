## Description:

6-step structured research skill that searches arXiv, reads five papers via markitdown, has Claude select the best two, runs targeted web searches, and writes a concise citation-backed research summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goog](https://clawhub.ai/user/goog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users use this skill to combine arXiv paper discovery, paper triage, targeted web search, and LLM synthesis into a short cited research summary for a topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad web retrieval with weak boundaries.

Mitigation: Use it only with public, non-sensitive topics unless fetch scope, redirect behavior, cache location, and dependency versions are tightened.

Risk: Fetched paper and page text is sent to OpenRouter for paper selection and synthesis.

Mitigation: Do not use private topics, internal URLs, proprietary documents, or sensitive data unless external LLM processing is approved.

Risk: Research summaries can be incomplete or misleading if PDF conversion, web search, or LLM selection fails.

Mitigation: Review the run checklist, selected source list, and inline citations before relying on the output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/goog/skills/q-research)
- [Publisher Profile](https://clawhub.ai/user/goog)
- [arXiv API Query Endpoint](https://export.arxiv.org/api/query)
- [arXiv Abstract Pages](https://arxiv.org/abs)
- [arXiv PDF Pages](https://arxiv.org/pdf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown research summary with selected papers, five cited bullets, and web sources; may be printed to terminal or saved to a file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses arXiv paper metadata and PDFs, fetched web page text, Serper search results, and OpenRouter-hosted LLM synthesis.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
