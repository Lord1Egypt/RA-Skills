## Description: <br>
Real-time Solana data monitoring with token prices, alerts via Telegram/email, whale transfers, liquidity pools, and new token discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, DeFi/NFT traders, and project teams use this skill to monitor Solana market and on-chain activity, configure price alerts, and generate guidance or commands for running the included monitors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens, chat IDs, SMTP credentials, or email app passwords may be exposed if stored carelessly. <br>
Mitigation: Use dedicated notification credentials, keep .env and config files out of source control, and restrict local file permissions. <br>
Risk: Unpinned Python dependencies may change behavior over time. <br>
Mitigation: Pin and review dependency versions before deployment. <br>
Risk: Alerts and monitoring requests pass through third-party APIs and notification services. <br>
Mitigation: Use deployment-approved service accounts and endpoints, and avoid including sensitive information in alert messages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chungvic/solana-monitor-vic) <br>
- [Publisher profile](https://clawhub.ai/user/chungvic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime scripts emit console text and Telegram/email alert messages.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call public price, Solana RPC, Telegram, and SMTP services when configured and executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
