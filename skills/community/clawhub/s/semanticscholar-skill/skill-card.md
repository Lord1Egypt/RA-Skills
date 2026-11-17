## Description:

Use when searching academic papers, looking up citations, finding authors, or getting paper recommendations using the Semantic Scholar API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and research users use this skill to search the Semantic Scholar corpus, inspect citations and references, find authors, request related-paper recommendations, and export literature results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paper queries may disclose sensitive or unpublished research interests to Semantic Scholar.

Mitigation: Avoid sensitive unpublished queries and use the skill only when external API submission is acceptable.

Risk: The skill handles the Semantic Scholar API key and raw request helpers broadly.

Mitigation: Review before installing, run in a sandbox, and restrict authenticated requests to official Semantic Scholar hosts.

Risk: Default temporary export paths may be predictable.

Mitigation: Use securely generated temporary file paths or explicit project paths for exported Markdown and JSON results.

## Reference(s):

- [Semantic Scholar API Docs](https://api.semanticscholar.org/api-docs/)
- [Semantic Scholar API Key](https://www.semanticscholar.org/product/api#api-key)
- [Agent Skills Format](https://agentskills.io)
- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/skills/semanticscholar-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries, result tables, Python snippets, shell commands, BibTeX, and JSON or Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use the Semantic Scholar API and optional S2_API_KEY; exports may be written as Markdown or JSON files.]

## Skill Version(s):

0.3.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
