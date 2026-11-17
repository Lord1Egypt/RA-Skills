## Description:

Use when user wants benchmark rankings, pricing, token limits, or IDE compatibility info for top 20 agentic coding models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waiyannyeinnaing](https://clawhub.ai/user/waiyannyeinnaing)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to compare current coding-model benchmark rankings, token pricing, context limits, and IDE compatibility before choosing models for agentic coding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script makes live outbound requests to BenchLM and OpenRouter when run.

Mitigation: Run it only in environments where those network calls are allowed, and document network access requirements for offline or permission-controlled deployments.

## Reference(s):

- [BenchLM Coding Leaderboard API](https://benchlm.ai/api/data/leaderboard?category=coding)
- [BenchLM Coding Leaderboard](https://benchlm.ai/coding)
- [OpenRouter Models API](https://openrouter.ai/api/v1/models)
- [ClawHub Skill Page](https://clawhub.ai/waiyannyeinnaing/skills/top-coding-models)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown tables and concise guidance, with JSON output available for automation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches live benchmark and pricing data at runtime; the top-N row count is configurable.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version table)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
