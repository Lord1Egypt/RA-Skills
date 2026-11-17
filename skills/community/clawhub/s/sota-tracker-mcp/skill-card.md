## Description:

Provides daily updated authoritative data and APIs tracking state-of-the-art AI models across categories from LMArena, Artificial Analysis, and HuggingFace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romancircus](https://clawhub.ai/user/romancircus)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI practitioners use this release to query current model rankings, check whether a model is outdated, compare alternatives, and get hardware-aware recommendations through static data, REST, or MCP interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automation and agent-instruction file updates can steer future agent behavior if accepted without review.

Mitigation: Prefer manual one-shot updates and review diffs to generated CLAUDE.md or agents.md content before enabling cron or systemd automation.

Risk: MCP configuration snippets may overwrite or conflict with an existing local MCP configuration.

Mitigation: Merge MCP configuration manually instead of replacing an existing .mcp.json.

Risk: Runtime dependencies and external data fetchers may change behavior over time.

Mitigation: Run in an isolated environment and pin or lock dependencies before production use.

## Reference(s):

- [LMArena](https://lmarena.ai)
- [Artificial Analysis](https://artificialanalysis.ai)
- [HuggingFace](https://huggingface.co)
- [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text tool responses with JSON, CSV, SQLite, REST, and MCP usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ranked model lists, freshness status, comparisons, hardware-aware recommendations, and setup commands.]

## Skill Version(s):

1.0.0 (source: server release metadata, pyproject.toml, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
