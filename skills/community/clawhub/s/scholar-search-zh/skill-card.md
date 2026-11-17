## Description:

scholar-search-zh helps agents search academic papers and research materials through the AISA Scholar API when users need papers, authors, recent studies, citation details, or year-filtered evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, analysts, and developers use this skill to retrieve academic evidence, paper metadata, citation-oriented search results, and year-filtered research material. Teams should account for the bundled client's broader web search, URL extraction, and synthesis modes when deciding whether a query is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, prompts, URLs, retrieved content, aggregated results, and the AISA API token are sent to AISA's API.

Mitigation: Use only when that disclosure is acceptable; avoid private URLs, confidential research topics, and internal material.

Risk: The bundled client exposes broader web, extraction, deep research, and synthesis behavior than the academic-search description alone suggests.

Mitigation: Review intended commands and constrain use to academic evidence workflows unless the broader search behavior is explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/scholar-search-zh)
- [AISA service](https://aisa.one)
- [AISA API endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or terminal text with result summaries, citations, URLs, and setup commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and the AISA_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
