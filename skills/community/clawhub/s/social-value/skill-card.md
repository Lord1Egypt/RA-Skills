## Description: <br>
Economic intelligence for AI agents — efficient micropayments via Breez SDK (Liquid or Spark). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vveerrgg](https://clawhub.ai/user/vveerrgg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to give an AI agent wallet-aware payment guidance for receiving, sending, batching, withdrawing, and estimating fees for sats over Liquid or Spark through Breez SDK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a wallet on mainnet and move real funds. <br>
Mitigation: Install only when an agent-controlled wallet is intended, start on testnet, set a low maximum balance, and require explicit confirmation for mainnet transfers, batch payouts, and withdrawals. <br>
Risk: Wallet access depends on a mnemonic that controls funds. <br>
Mitigation: Protect the mnemonic like cash and provide it only through secure environment configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vveerrgg/social-value) <br>
- [OpenClaw homepage](https://github.com/HumanjavaEnterprises/huje.socialvalue.OC-python.src) <br>
- [Breez SDK](https://breez.technology/sdk/) <br>
- [social-alignment](https://clawhub.ai/vveerrgg/social-alignment) <br>
- [sense-memory](https://clawhub.ai/vveerrgg/sense-memory) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell install commands, and environment variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include wallet setup steps, transfer workflows, fee-estimation guidance, and safety reminders] <br>

## Skill Version(s): <br>
0.1.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
