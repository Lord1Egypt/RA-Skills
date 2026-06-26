## Description: <br>
Monitors Solana tokens with DexScreener and reports price, volume, liquidity, market cap, and transaction alerts, with optional Telegram Bot API delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shepdogpack](https://clawhub.ai/user/shepdogpack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and token operators use this skill to set up ongoing monitoring for Solana token contracts, inspect status reports, and receive alerts for market movement, liquidity changes, volume spikes, and market cap milestones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens and chat IDs are stored in local plaintext configuration files. <br>
Mitigation: Use a dedicated Telegram bot token, restrict where the local config is stored, and rotate or revoke the token if the config may have been exposed. <br>
Risk: Enabled monitors can make repeated DexScreener requests and send ongoing alerts without further prompts. <br>
Mitigation: Enable monitoring only for tokens the user explicitly wants watched, review configured monitors periodically, and disable or remove monitors that are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shepdogpack/solana-token-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/shepdogpack) <br>
- [ShepDog project site](https://shepdogcoin.com) <br>
- [DexScreener Solana token API](https://api.dexscreener.com/tokens/v1/solana/{CONTRACT_ADDRESS}) <br>
- [ShepDog X profile](https://x.com/ShepDogCoin) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text status or alert output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local token monitor configuration files and optionally send Telegram messages when credentials are configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
