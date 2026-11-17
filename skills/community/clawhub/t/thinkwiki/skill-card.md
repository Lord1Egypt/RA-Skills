## Description:

Use this skill when the user wants to create, maintain, query, or visualize a local Markdown knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzdavid](https://clawhub.ai/user/wzdavid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge workers use ThinkWiki to create, maintain, query, and visualize a local Markdown knowledge base. It supports importing documents or webpages, answering from existing wiki pages, saving valuable outputs, and generating static HTML viewer, graph, inbox, and governance artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured remote AI or embedding providers may receive relevant wiki content when optional THINKWIKI_LLM_* or THINKWIKI_EMBED_* variables are set.

Mitigation: Confirm data-sharing policy before enabling remote providers, and override the default embedding endpoint when policy requires a different provider.

## Reference(s):

- [ThinkWiki GitHub repository](https://github.com/wzdavid/ThinkWiki)
- [ThinkWiki ClawHub listing](https://clawhub.ai/wzdavid/skills/thinkwiki)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local Markdown wiki content and static HTML artifacts under the selected wiki output directory.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
