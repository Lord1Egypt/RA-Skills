## Description: <br>
Interact with the Kraken cryptocurrency exchange for spot and futures market data, account information, trading, and live WebSocket streams through the tentactl MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[askbeka](https://clawhub.ai/user/askbeka) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and trading operators use this skill to inspect Kraken market data, monitor balances and positions, stream live exchange data, and prepare or execute Kraken spot and futures actions. Authenticated account and trading workflows require Kraken API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent high-impact control over real Kraken crypto funds when authenticated trading or transfer permissions are enabled. <br>
Mitigation: Use read-only API keys for market data, balances, and history; enable trading, transfer, futures, earn, or withdrawal permissions only for deliberate live use. <br>
Risk: Kraken API credentials may be stored in ~/.tentactl.env. <br>
Mitigation: Protect the credentials file, keep permissions restricted, and avoid storing powerful keys unless authenticated workflows are required. <br>
Risk: Automation such as cron-driven trading can repeatedly execute account-impacting actions. <br>
Mitigation: Review automation carefully and require explicit confirmation before any order, cancellation, transfer, allocation, or withdrawal. <br>
Risk: The skill relies on an external tentactl binary to perform MCP calls. <br>
Mitigation: Verify the tentactl binary source before installation or execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/askbeka/tentactl) <br>
- [Publisher Profile](https://clawhub.ai/user/askbeka) <br>
- [tentactl Source](https://github.com/askbeka/tentactl) <br>
- [tentactl Releases](https://github.com/askbeka/tentactl/releases) <br>
- [Kraken](https://www.kraken.com) <br>
- [Kraken API Key Setup](https://www.kraken.com/u/security/api) <br>
- [Tools Reference](references/tools.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-oriented text with JSON tool arguments and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke networked Kraken market, account, trading, and WebSocket endpoints through tentactl; authenticated operations require Kraken API credentials.] <br>

## Skill Version(s): <br>
0.3.2 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
