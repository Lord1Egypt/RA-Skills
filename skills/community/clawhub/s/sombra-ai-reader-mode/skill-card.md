## Description:

Persistent reader mode for AI. Save web pages, organise into collections, distil to dense context, and serve it all through MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dazld](https://clawhub.ai/user/dazld)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to connect agents to a persistent Sombra research library, save web pages and notes, organize collections, search saved material, and retrieve distilled context for follow-on work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup uses an unpinned remote `sombra-mcp` package through `npx`.

Mitigation: Pin and review the MCP package version before installing or updating it.

Risk: The example passes a reusable token in plaintext command arguments and shared configuration.

Mitigation: Prefer OAuth or a secret manager where available, avoid long-lived tokens in shared config, and issue a narrow-scope token.

Risk: The MCP server needs local execution and network access.

Mitigation: Run it with only the local and network access needed for the Sombra service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dazld/skills/sombra-ai-reader-mode)
- [Sombra](https://sombra.so)
- [Sombra MCP setup docs](https://sombra.so/mcp)
- [What is Sombra?](https://sombra.so/blog/what-is-sombra)
- [Why context engineering matters](https://sombra.so/blog/context-failures)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and command examples; MCP tool responses include text and markdown content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx, a Sombra account token or OAuth-capable client, and network access to the Sombra MCP service.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
