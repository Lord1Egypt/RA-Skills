## Description: <br>
Free stock and crypto momentum scanner with social sentiment analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nomadrex](https://clawhub.ai/user/nomadrex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan stocks and crypto assets for momentum, social sentiment, score changes, and historical signal performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker searches and market-interest patterns may be sent to third-party market, social, and search services. <br>
Mitigation: Review before installing and use the skill only when external market and sentiment lookups are acceptable. <br>
Risk: The skill may use TAVILY_API_KEY if it is present in the environment. <br>
Mitigation: Do not set TAVILY_API_KEY unless Tavily-backed Reddit sentiment search is intentionally desired. <br>
Risk: The skill stores local cache, snapshots, and signal history. <br>
Mitigation: Delete ~/.openclaw/workspace/memory/ripe_scanner and /tmp/ripe_scanner_cache.json when local scan history should not be retained. <br>
Risk: Runtime dependencies and external data retrieval increase the installation and execution surface. <br>
Mitigation: Install dependencies in an isolated Python environment and review the skill before deployment. <br>


## Reference(s): <br>
- [Ripe Scanner ClawHub Page](https://clawhub.ai/nomadrex/ripe-scanner) <br>
- [NomadRex Publisher Profile](https://clawhub.ai/user/nomadrex) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [S&P 500 Companies](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies) <br>
- [Nasdaq-100](https://en.wikipedia.org/wiki/Nasdaq-100) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown and terminal-oriented text with inline shell commands and tabular scan output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read market and social-sentiment data from external services and may write local cache, snapshot, and signal history files.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
