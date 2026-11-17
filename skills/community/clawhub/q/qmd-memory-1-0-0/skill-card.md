## Description:

Enables local hybrid memory search for OpenClaw using QMD with optimized collections, automatic indexing, and optional multi-agent sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sieyer](https://clawhub.ai/user/sieyer)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to configure local OpenClaw memory search, index Markdown workspaces, refresh embeddings, estimate API cost savings, and optionally expose shared memory through a local MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can globally install an unpinned npm package.

Mitigation: Review or install a pinned QMD version before running setup in a production or sensitive environment.

Risk: The skill can index sensitive OpenClaw Markdown files into a persistent local QMD cache.

Mitigation: Limit OPENCLAW_WORKSPACE to non-sensitive content, remove secrets before indexing, and review retention under ~/.cache/qmd.

Risk: The optional MCP server exposes shared memory access for local or multi-agent use.

Mitigation: Run the MCP server only when localhost or shared-agent access is acceptable.

## Reference(s):

- [QMD Memory 1.0.0 ClawHub skill page](https://clawhub.ai/sieyer/skills/qmd-memory-1-0-0)
- [QMD project](https://github.com/tobi/qmd)
- [As Above Technologies](https://asabove.tech)
- [Declared support issues page](https://github.com/asabove/qmd-memory-skill/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented guidance with shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local setup instructions, QMD collection configuration, index refresh commands, MCP server commands, and cost-savings estimates.]

## Skill Version(s):

1.0.0 (source: release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
