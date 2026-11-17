## Description:

Provides daily updated rankings and metadata for state-of-the-art AI models through static exports, local queries, a REST API, and optional MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romancircus](https://clawhub.ai/user/romancircus)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to check current AI model rankings, freshness, forbidden or outdated models, and hardware-aware recommendations before choosing models for projects or agent guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional automation can persistently change future agent instruction files such as CLAUDE.md or agents.md.

Mitigation: Prefer static JSON/CSV or manual local queries; only enable cron or systemd timers after pinning the code, reviewing diffs, and confirming how to disable the timer.

Risk: Optional MCP configuration can add a local server that influences model recommendations.

Mitigation: Treat MCP results as advisory and review any .mcp.json edits manually before use.

Risk: Aggregated model rankings can become stale or reflect third-party benchmark limitations.

Mitigation: Check source freshness and review recommendations against project requirements before selecting a model.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/romancircus/skills/sota-tracker-claw)
- [README](README.md)
- [Security policy](SECURITY.md)
- [Evaluation report](EVALUATION.md)
- [LMArena leaderboard](https://lmarena.ai/leaderboard)
- [Artificial Analysis](https://artificialanalysis.ai)
- [HuggingFace](https://huggingface.co)
- [Open LLM Leaderboard](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, CSV, SQLite query results, REST API responses, shell commands, and agent instruction snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory model-ranking and freshness guidance derived from aggregated public benchmark and model metadata.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
