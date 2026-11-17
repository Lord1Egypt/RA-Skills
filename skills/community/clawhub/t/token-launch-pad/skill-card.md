## Description:

Helps builders evaluate token launch ideas and generate guidance, code patterns, API examples, and fee-management workflows for launching tokens through Clanker, Flaunch, Pump.fun, or the Tator API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azep-ninja](https://clawhub.ai/user/azep-ninja)

### License/Terms of Use:


## Use Case:

External developers and token builders use this skill to compare launch paths, prepare token deployment details, configure creator-fee recipients, claim fees, update recipients, and understand tax, legal, and operational cautions before acting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token launches, fee claims, recipient updates, and hosted API requests can have irreversible financial effects.

Mitigation: Require explicit confirmation that names the chain, wallet, token, recipient, service endpoint, payment amount, and irreversible effect before taking action.

Risk: Wallet keys, contract addresses, dependencies, and funded wallets can expose users to financial loss if handled carelessly.

Mitigation: Use dedicated minimally funded wallets, never share private keys, pin dependencies, and verify contract addresses before signing or submitting transactions.

Risk: The skill provides token launch guidance in an area with tax, legal, and market risk.

Mitigation: Present the guidance as informational, encourage professional review where appropriate, and avoid implying guaranteed returns or legal compliance.

## Reference(s):

- [Token Launcher Direct Mode Reference](REFERENCE.md)
- [Clanker v4 Direct Mode Reference](references/clanker.md)
- [Flaunch Direct Mode Reference](references/flaunch.md)
- [Pump.fun Direct Mode Reference](references/pumpfun.md)
- [Tator documentation](https://docs.tator.bot)
- [x402 protocol](https://www.x402.org)
- [Clanker SDK documentation](https://clanker.gitbook.io/clanker-documentation/sdk/v4.0.0)
- [Flaunch builder documentation](https://docs.flaunch.gg/for-builders)
- [Pump.fun public documentation](https://github.com/pump-fun/pump-public-docs)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code snippets, JSON payloads, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include unsigned transaction patterns and hosted API request examples for token launches, fee claims, recipient updates, and security scans.]

## Skill Version(s):

1.0.15 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
