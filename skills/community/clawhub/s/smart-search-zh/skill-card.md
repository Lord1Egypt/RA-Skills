## Description:

Combines web and academic search into a smart AISA search mode for balanced retrieval across public web coverage and academic depth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they need an agent to combine public web search with academic search for balanced research coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries, URLs, and retrieved result bundles may be sent to AISA's external API under the user's API key.

Mitigation: Avoid secrets, private or internal URLs, regulated data, and prompts that should remain local.

Risk: The included client exposes broader search, URL extraction, and synthesis capabilities than the short skill description discloses.

Mitigation: Prefer explicit subcommands and review the intended API action before invocation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/smart-search-zh)
- [AISA service](https://aisa.one)
- [AISA API base](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and text search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; can return result lists, snippets, answers, citations, usage details, extracted URL content, and synthesized summaries depending on the selected command.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
