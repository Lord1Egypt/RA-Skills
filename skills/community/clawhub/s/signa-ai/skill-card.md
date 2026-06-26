## Description: <br>
Send payments, messages, escrow, and verifiable outputs between AI agents on the Signum blockchain. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[folkerds13](https://clawhub.ai/user/folkerds13) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use Signaai to let OpenClaw agents check balances, send Signum payments and messages, create or release escrow tasks, and stamp or verify task outputs on-chain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize real mainnet Signum transactions and control wallet funds while its daemon runs. <br>
Mitigation: Use only a small dedicated wallet and confirm the operator understands that the configured passphrase can authorize real transactions. <br>
Risk: The skill requires sensitive credentials, including wallet passphrases and optional OpenClaw or Telegram configuration. <br>
Mitigation: Avoid reusing important API keys or passphrases, restrict stored secrets to the dedicated deployment, and review local configuration before enabling autonomous mode. <br>
Risk: Task and result data may be shared with LLM providers, Telegram, and public blockchain records. <br>
Mitigation: Do not submit confidential task content unless the deployment has approved those data flows and the public on-chain record is acceptable. <br>


## Reference(s): <br>
- [SignaAI live dashboard](https://signaai.io) <br>
- [Signum blockchain](https://signum.network) <br>
- [Signum explorer](https://explorer.signum.network) <br>
- [SignaAI Python SDK](https://pypi.org/project/signaai/) <br>
- [SignaAI SDK repository](https://github.com/folkerds13/signaai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and transaction receipt text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include blockchain transaction IDs, wallet addresses, escrow IDs, and setup instructions.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
