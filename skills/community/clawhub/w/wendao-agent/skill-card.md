## Description: <br>
Automates BNB Chain NFA cultivation through an authorized agent wallet, including meditation, leveling, attribute allocation, optional PK, breakthrough actions, and on-chain learning-tree records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bb964305](https://clawhub.ai/user/bb964305) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run an automated on-chain agent for a WenDao NFA on BNB Smart Chain. It is intended for wallet-authorized game automation, including routine progression tasks and optional token-spending PK behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent controls an authorized wallet and can submit signed on-chain transactions. <br>
Mitigation: Use a dedicated low-balance agent wallet, keep only funds you are willing to risk in it, and revoke agent-wallet authorization when you stop using the skill. <br>
Risk: PK and breakthrough behavior can approve and spend $JW even though parts of the documentation describe the agent wallet as gas-only. <br>
Mitigation: Use the defensive strategy or a custom no-PK strategy unless you explicitly want token-spending behavior, and avoid funding the agent wallet with more $JW than needed. <br>
Risk: Passing a private key on the command line can expose it through shell history or process inspection. <br>
Mitigation: Prefer the AGENT_PRIVATE_KEY environment variable and avoid using the --key option on shared or monitored systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bb964305/wendao-agent) <br>
- [Publisher profile](https://clawhub.ai/user/bb964305) <br>
- [WenDao website](https://wendaobsc.xyz) <br>
- [README](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, TypeScript API examples, and CLI command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance and commands for operating a wallet-backed BNB Chain game automation agent; runtime behavior may submit signed on-chain transactions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; package.json and CLI report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
