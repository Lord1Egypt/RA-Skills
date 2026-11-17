## Description:

Live web search, page retrieval, news, sitemap discovery, and trending topics through Search1API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fatwang2](https://clawhub.ai/user/fatwang2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Search1API to perform live web search, retrieve and summarize pages, check current news, discover site links, explore trending topics, and synthesize cited research through MCP tools or the s1 CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance includes curl-to-bash and unpinned global npm commands.

Mitigation: Review before installing and prefer a connected MCP tool or verified, pinned CLI installation.

Risk: Search queries and URLs may be sent to Search1API and selected search providers.

Mitigation: Do not submit secrets, signed URLs, private or internal links, regulated data, confidential research terms, or other sensitive material unless that sharing is acceptable.

Risk: API keys can be exposed through chat, logs, or shell history.

Mitigation: Use browser login where possible and keep keys out of chat, logs, and shell history.

## Reference(s):

- [Search1API skill page](https://clawhub.ai/fatwang2/skills/s1)
- [Usage examples](artifact/reference/examples.md)
- [Search1API CLI installer](https://cli.search1api.com/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and cited source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Search1API MCP tools or the s1 CLI; server metadata declares s1 as a required binary for CLI fallback.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
