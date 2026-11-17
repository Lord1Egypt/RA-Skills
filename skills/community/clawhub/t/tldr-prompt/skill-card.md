## Description:

Create tldr summaries for GitHub Copilot files (prompts, agents, instructions, collections), MCP servers, or documentation from URLs and queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jhauga](https://clawhub.ai/user/jhauga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to turn GitHub Copilot customization files, MCP server documentation, and Copilot documentation into concise tldr-style Markdown summaries with actionable examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read provided local files and fetched documentation or user-provided URLs to summarize their contents.

Mitigation: Avoid providing sensitive private files or URLs unless their contents should be summarized in the current chat.

Risk: Generated tldr summaries may omit details from source documentation or produce guidance that needs domain review.

Mitigation: Review summaries against the source material before relying on them for workflow, setup, or configuration decisions.

## Reference(s):

- [TLDR Prompt on ClawHub](https://clawhub.ai/jhauga/skills/tldr-prompt)
- [GitHub awesome-copilot](https://github.com/github/awesome-copilot)
- [Model Context Protocol documentation](https://modelcontextprotocol.io/)
- [VS Code MCP servers documentation](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [VS Code inline chat documentation](https://code.visualstudio.com/docs/copilot/inline-chat)
- [VS Code Copilot documentation](https://code.visualstudio.com/docs/copilot/)
- [VS Code Copilot chat documentation](https://code.visualstudio.com/docs/copilot/chat/)
- [GitHub Copilot documentation](https://docs.github.com/en/copilot/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown tldr summary with usage examples and inline command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chat-only output; does not create files.]

## Skill Version(s):

1.0.0 (source: release metadata and user-provided changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
