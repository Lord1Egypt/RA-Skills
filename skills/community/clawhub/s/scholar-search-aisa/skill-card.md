## Description:

Searches academic papers and scholarly sources through the AISA scholar endpoint for paper, author, citation, and year-filtered research queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, developers, and analysts use this skill to retrieve scholarly search results, author evidence, citations, and date-filtered academic sources through AISA-backed search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged client can send broader query types, arbitrary URLs, and aggregated results to AISA services beyond scholar-only use.

Mitigation: Use it only with non-sensitive scholarly queries unless the publisher narrows or clearly documents the broader data flows.

Risk: The skill requires an AISA API key for runtime access.

Mitigation: Provide a scoped key where possible, avoid sharing it in prompts or logs, and rotate it if exposure is suspected.

Risk: Private URLs, presigned links, internal research systems, or sensitive queries may be disclosed to external AISA services.

Mitigation: Do not use those inputs with this skill unless the deployment has approved that data flow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/scholar-search-aisa)
- [AISA API service](https://aisa.one)
- [AISA API endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with search result snippets, URLs, dates, citations, and summaries when returned by AISA.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; sends requests to AISA services.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
