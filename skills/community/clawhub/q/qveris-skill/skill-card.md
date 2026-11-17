## Description:

Search and execute dynamic tools via QVeris API. Use when needing to find and call external APIs/tools dynamically (weather, search, data retrieval, stock trading analysis, etc.). Requires QVERIS_API_KEY environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yifeiwang1981](https://clawhub.ai/user/yifeiwang1981)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover QVeris-hosted API tools by capability and execute selected tools for weather, market data, search, currency, and other data retrieval tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool searches and execution parameters are sent to QVeris and may be routed to third-party APIs.

Mitigation: Do not include secrets, private code, internal URLs, sensitive business data, or regulated data in search queries or execution parameters.

Risk: The skill can automatically invoke broad third-party tool execution for stock, trading, analysis, market, weather, search, and data retrieval requests.

Mitigation: Review selected tools, parameters, and destination services before execution, especially for financial, business, or sensitive queries.

Risk: The artifact documents curl-to-shell, PowerShell iex, and unpinned npx installation commands.

Mitigation: Prefer verified package-manager installation methods and review installation scripts before running them.

## Reference(s):

- [QVeris](https://qveris.ai)
- [ClawHub skill page](https://clawhub.ai/yifeiwang1981/skills/qveris-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown and terminal output, with optional raw JSON from QVeris tool search and execution responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QVERIS_API_KEY; execution responses are capped by the max response size argument, defaulting to 20480 bytes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
