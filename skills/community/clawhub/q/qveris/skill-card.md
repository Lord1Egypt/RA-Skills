## Description:

Search and execute dynamic tools via QVeris API. Use when needing to find and call external APIs/tools dynamically (weather, search, data retrieval, stock trading analysis, etc.). Requires QVERIS_API_KEY environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hqman](https://clawhub.ai/user/hqman)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to discover and execute QVeris-hosted API tools for tasks such as weather lookup, market data retrieval, web search, currency data, and other dynamic API-backed workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and execution parameters are sent to QVeris and may be relayed to downstream tools.

Mitigation: Avoid using the skill with secrets, regulated data, or sensitive account details unless QVeris and the selected downstream tool are explicitly trusted.

Risk: Discovered tools may perform broad third-party API actions, including actions that could mutate accounts.

Mitigation: Review each selected tool, its parameters, and the intended action before execution, especially for account-changing or trading-related workflows.

Risk: The documentation includes remote installer commands for uv.

Mitigation: Prefer safer uv installation methods or verify installer integrity before running remote installation commands.

## Reference(s):

- [QVeris](https://qveris.ai)
- [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)
- [ClawHub Skill Page](https://clawhub.ai/hqman/skills/qveris)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QVERIS_API_KEY and can limit execution responses with --max-size.]

## Skill Version(s):

0.1.0 (source: pyproject.toml and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
