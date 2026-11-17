## Description:

Pay for things safely from your agent: gasless USDC on Base plus JIT single-use virtual cards via the Z-Zero MCP server, with card data kept out of model context and explicit human approval required before payment execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dempty-glitch](https://clawhub.ai/user/dempty-glitch)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure an agent to make approved purchases through Z-Zero payment flows, including Base USDC transfers and single-use virtual cards. It is intended for checkout workflows where the operator wants human approval, bounded spend, and payment receipts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run mutable external payment code and follow a mutable external payment procedure.

Mitigation: Review before installing, use an isolated agent environment, and prefer a pinned and reviewed MCP server version instead of @latest.

Risk: A financial credential and payment-capable workflow can create unintended spending exposure.

Mitigation: Keep spending limits low, compare the final cart and total before payment, and require human approval for every payment.

Risk: Sharing the same OS user or credential store with unrelated agents can broaden credential exposure.

Mitigation: Run the skill in a dedicated agent environment and avoid shared OS users or shared credential stores.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dempty-glitch/skills/z-zero-payments)
- [Publisher profile](https://clawhub.ai/user/dempty-glitch)
- [Z-Zero homepage](https://z-zero.xyz)
- [Z-Zero agent dashboard](https://z-zero.xyz/dashboard/agents)
- [z-zero-mcp-server npm package](https://www.npmjs.com/package/z-zero-mcp-server)
- [Project source link from skill artifact](https://github.com/Dempty-glitch/Z-Zero-mcp)
- [Base transaction proof linked by skill artifact](https://basescan.org/tx/0xdfd1f2f824e1232c3e03c52485332570ff01fbb0340c5571f699ed1218735d7a)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code]

**Output Format:** [Markdown with inline JSON and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP setup guidance, required environment variables, payment workflow steps, and operator-approval rules.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
