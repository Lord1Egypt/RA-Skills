## Description: <br>
Integrate OpenClaw with Xerolite - IBKR for querying the Xerolite API, placing orders, searching contracts, and fetching portfolio data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xero-flex](https://clawhub.ai/user/xero-flex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to a Xerolite/IBKR setup for contract lookup, portfolio inspection, and order placement through the Xerolite REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent submit real brokerage orders through a Xerolite/IBKR trading setup without a built-in confirmation or dry-run safeguard. <br>
Mitigation: Prefer paper trading or a least-privileged key, verify XEROLITE_API_URL points to localhost or another trusted host, and require explicit user confirmation before order placement. <br>
Risk: The skill requires a sensitive XEROLITE_AGENTIC_API_KEY for agentic endpoints. <br>
Mitigation: Provide the key through a protected environment variable or explicit secret handling, and avoid exposing it in shared command history or logs. <br>


## Reference(s): <br>
- [Xerolite REST API Reference](references/API.md) <br>
- [Xerolite](https://www.xeroflex.com/xerolite/) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Command-line requests and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and XEROLITE_AGENTIC_API_KEY; XEROLITE_API_URL may be set to choose the Xerolite host.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
