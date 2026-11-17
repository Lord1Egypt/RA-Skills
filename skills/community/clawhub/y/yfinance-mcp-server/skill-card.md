## Description:

Access Yahoo Finance data for stock prices, history, financials, options, dividends, news, and market screeners.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rizkydwicmt](https://clawhub.ai/user/rizkydwicmt)

### License/Terms of Use:


## Use Case:

Developers and external users can connect an agent to Yahoo Finance-backed market data for investment research, portfolio monitoring, and market discovery. The skill exposes tools for ticker lookup, prices, fundamentals, historical data, options, dividends, recommendations, movers, screeners, and news.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can run mutable remote code and make persistent local configuration changes.

Mitigation: Review and pin the exact MCP server source, replace remote shell installation with a verified uv installation method, and confirm mcporter or OpenClaw writes before installation.

Risk: Repository, path, and auto-accept overrides can redirect installation targets or update configuration without further prompts.

Mitigation: Run as an unprivileged user, set target paths explicitly, and avoid YFINANCE_YES=true unless the paths are known and backed up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rizkydwicmt/skills/yfinance-mcp-server)
- [Publisher profile](https://clawhub.ai/user/rizkydwicmt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool names, arguments, examples, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces MCP tool usage guidance and installation/configuration steps for a Yahoo Finance data server.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
