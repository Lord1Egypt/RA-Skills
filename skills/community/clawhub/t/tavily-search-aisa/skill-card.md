## Description:

Run Tavily web search through AISA with filters for depth, topic, and time range when the user needs flexible web search with stronger filtering than a plain keyword search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run AISA-backed Tavily-style web searches with controls for search depth, topic, time range, answer inclusion, and result count. It is useful when an agent needs recent or filtered web results rather than a basic keyword search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security evidence reports that the release is presented as Tavily search while the bundled runtime exposes broader search, extraction, model-query, aggregation, and synthesis features.

Mitigation: Review the bundled commands before installing, limit agent use to the intended Tavily search workflow, or remove undocumented commands before deployment.

Risk: Queries, URLs, search results, and the AISA API key are sent to api.aisa.one during use.

Mitigation: Use a dedicated API key, avoid submitting sensitive or private data, and rotate or revoke the key if it may have been exposed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/aisadocs/skills/tavily-search-aisa)
- [AISA homepage](https://aisa.one)
- [AISA API endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown-style CLI output with titles, URLs, snippets, answers, citations, and usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY. Runtime output can include search results, extracted URL content, model answers, citations, usage or cost fields, and confidence summaries depending on the selected command.]

## Skill Version(s):

1.0.0 (source: server release, target metadata, and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
