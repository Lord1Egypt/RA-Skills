## Description:

Standardized search workflow integrating tavily-search, web_search, web_fetch and other search skills, providing a complete process from query analysis to result output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earthwalking](https://clawhub.ai/user/earthwalking)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run a staged search workflow for academic search, recent information, deep research, and fact checking, then produce a structured Markdown report with summaries, key information, source citations, and links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script includes a fallback Tavily API key.

Mitigation: Remove and rotate the embedded key, require users to provide TAVILY_API_KEY explicitly, and block execution when the variable is missing.

Risk: Search queries may be sent to Tavily and reports may be written to local files.

Mitigation: Disclose the external service and local file-writing behavior before installation and avoid sending sensitive queries.

Risk: Broad trigger keywords could invoke external search behavior during routine search-related prompts.

Mitigation: Narrow trigger keywords or require explicit user confirmation before network search execution.

## Reference(s):

- [Search Workflow ClawHub page](https://clawhub.ai/earthwalking/skills/search-workflow)
- [Tavily Search API endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with search summary, key information, source citations, and related links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes timestamped local Markdown report files when the bundled script is run.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact manifest, and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
