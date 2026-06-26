## Description: <br>
Access Yahoo Finance data, including stock prices, history, financials, options, dividends, news, and market screeners. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rizkydwicmt](https://clawhub.ai/user/rizkydwicmt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users can use this skill to connect an agent to a yfinance MCP server for market research, portfolio monitoring, ticker search, financial statement lookup, options analysis, and finance news retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer makes persistent local setup changes, including Python environment creation, package installation, mcporter configuration, and optional OpenClaw skill registration. <br>
Mitigation: Review install.sh before running it and use SKIP_MCPORTER=true or SKIP_SKILL=true when persistent registration is not desired. <br>
Risk: The installer may install uv by piping a remote shell script from astral.sh into sh. <br>
Mitigation: Install uv through a trusted package manager or otherwise verify the uv installer source before execution. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/rizkydwicmt/yfinance-mcp-server) <br>
- [Repository URL mentioned by artifact](https://github.com/rizkydwicmt/yfinance-mcp-server.git) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API Calls, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline MCP tool examples and shell commands; installed MCP tools return finance data as text or structured responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installer and configuration guidance for registering the yfinance MCP server with mcporter and OpenClaw.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
