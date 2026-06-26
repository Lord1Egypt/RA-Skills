## Description: <br>
AI trading memory for MT5 and forex traders that records trades, discovers patterns, and provides AI-powered reflections with strategy-adjustment recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zychenpeng](https://clawhub.ai/user/zychenpeng) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External traders and developers use this skill to give an agent persistent trading memory, recall past trades, analyze strategy performance, and produce reflections over MT5, forex, or API-provided trade data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles trade history and can use MT5 broker credentials for synchronization. <br>
Mitigation: Store credentials only in a private local .env file with restrictive permissions, avoid committing it, and prefer demo or read-only investor credentials where possible. <br>
Risk: A remote TRADEMEMORY_API endpoint can receive trade data if configured. <br>
Mitigation: Keep TRADEMEMORY_API on localhost unless the endpoint is controlled and approved for the trade data being sent. <br>
Risk: Trading reflections and lot-size or strategy recommendations may be incorrect or unsuitable for live trading. <br>
Mitigation: Manually review all trading and risk recommendations before applying them. <br>


## Reference(s): <br>
- [TradeMemory GitHub Repository](https://github.com/mnemox-ai/tradememory-protocol) <br>
- [TradeMemory Protocol PyPI Package](https://pypi.org/project/tradememory-protocol/) <br>
- [MT5 Sync Setup Guide](https://github.com/mnemox-ai/tradememory-protocol/blob/master/docs/MT5_SYNC_SETUP.md) <br>
- [TradeMemory Tutorial](https://github.com/mnemox-ai/tradememory-protocol/blob/master/docs/TUTORIAL.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zychenpeng/tradememory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with natural-language prompts, tables, and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local SQLite trade history, optional MT5 credentials, optional TradeMemory API endpoint, and optional Anthropic API key for LLM reflections.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
