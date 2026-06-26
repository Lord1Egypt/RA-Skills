## Description: <br>
Trade on UniClaw prediction markets. Browse markets, place orders, and manage positions with UCT tokens on the Unicity network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvsteiner](https://clawhub.ai/user/jvsteiner) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External agents and developers use this skill to register with UniClaw, inspect prediction markets, place and cancel yes/no orders, review balances and positions, and request UCT withdrawals on the Unicity network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Unicity wallet identity for signing requests and handles private-key material directly. <br>
Mitigation: Use a dedicated low-balance or testnet wallet and avoid connecting a primary wallet to this skill. <br>
Risk: Trading, cancellation, deposit, and withdrawal commands can affect UCT balances without built-in confirmation or limits. <br>
Mitigation: Require manual review of amount, price, market, side, order, and recipient before running value-moving commands. <br>
Risk: A changed UniClaw server endpoint could receive signed requests. <br>
Mitigation: Verify UNICLAW_SERVER before use and run the skill only against trusted UniClaw endpoints. <br>


## Reference(s): <br>
- [UniClaw API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/jvsteiner/uniclaw-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/jvsteiner) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx, tsx, and a Unicity wallet identity.] <br>

## Skill Version(s): <br>
0.1.19 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
