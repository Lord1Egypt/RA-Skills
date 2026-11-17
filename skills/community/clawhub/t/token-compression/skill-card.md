## Description:

Compress AI Agent tool outputs, logs, and RAG content using Headroom to reduce token usage by 20-95%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonbuilds](https://clawhub.ai/user/johnsonbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they explicitly need to compress large, redundant tool outputs, logs, RAG chunks, or files for agent workflows while managing local cache and configuration risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw prompts, tool outputs, logs, and other uncompressed content may be cached on local disk.

Mitigation: Avoid API keys, passwords, PII, proprietary code, and other sensitive material; use encrypted storage for any approved sensitive workflow and clear ~/.headroom/cache when content should no longer persist.

Risk: The skill asks users to install an unpinned third-party compression tool that can modify agent startup configuration.

Mitigation: Verify the package version and source before installation, prefer explicit per-task use for sensitive work, and confirm how to undo wrapping before enabling it globally.

## Reference(s):

- [Headroom GitHub repository](https://github.com/headroomlabs-ai/headroom)
- [Headroom documentation](https://docs.headroomlabs.ai/docs)
- [Headroom benchmarks](https://docs.headroomlabs.ai/docs/benchmarks)
- [ClawHub skill page](https://clawhub.ai/johnsonbuilds/skills/token-compression)
- [ClawHub publisher profile](https://clawhub.ai/user/johnsonbuilds)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance can include local deployment, agent wrapping, proxy mode, Python library use, MCP server setup, verification commands, and cache handling.]

## Skill Version(s):

1.1.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
