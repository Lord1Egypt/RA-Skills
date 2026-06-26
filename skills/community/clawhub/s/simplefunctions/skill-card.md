## Description: <br>
SimpleFunctions is an AI-native prediction market runtime for Kalshi and Polymarket thesis tracking, edge scanning, position monitoring, trade execution, and Telegram alerts through the sf CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patrickliu0077](https://clawhub.ai/user/patrickliu0077) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to manage prediction-market theses, scan Kalshi and Polymarket markets, monitor positions, inspect account state, and prepare or execute trades through the sf CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-accessible commands may connect to real prediction-market accounts and expose trading, order, balance, position, and settlement workflows. <br>
Mitigation: Use read-only or limited credentials where available, verify whether configured Kalshi keys can place orders, and require manual approval before any trade execution. <br>
Risk: Telegram bot tokens, SimpleFunctions API keys, and market credentials are sensitive and may expose alerts, account data, or trading capability. <br>
Mitigation: Store credentials outside prompts and logs, rotate tokens if exposed, and limit alert content to information appropriate for the configured channel. <br>


## Reference(s): <br>
- [SimpleFunctions homepage](https://simplefunctions.dev) <br>
- [ClawHub skill page](https://clawhub.ai/patrickliu0077/simplefunctions) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/patrickliu0077) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, JSON] <br>
**Output Format:** [Markdown with inline bash command examples and CLI option descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The sf CLI supports --json for scripted agent use; authenticated account functions require SimpleFunctions and market account credentials.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
