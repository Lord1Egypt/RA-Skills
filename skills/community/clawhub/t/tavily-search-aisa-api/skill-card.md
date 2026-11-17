## Description:

Advanced web search via Tavily through the AIsa API with search depth, topic and time filtering, content extraction, and optional LLM-generated answer summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to run AIsa-backed Tavily searches, filter search results by depth, topic, and time range, extract supplied URLs, and request answer summaries with source snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, supplied URLs, prompts, and retrieved result data may be sent to AIsa under the user's API key.

Mitigation: Use only with data approved for that external service, and avoid secrets, private URLs, regulated data, and URLs containing tokens.

Risk: The package exposes broader web, scholar, extraction, Perplexity, and synthesis modes than the Tavily-focused description suggests.

Mitigation: Review the available subcommands before deployment and restrict use to approved modes until the documentation and exposed commands are aligned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/tavily-search-aisa-api)
- [AIsa homepage](https://aisa.one)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Structured terminal text with titles, URLs, excerpts, dates when available, optional answer summaries, citations, and usage/cost metadata when returned by the API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; count and filtering options affect returned result volume.]

## Skill Version(s):

1.0.1 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
