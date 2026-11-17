## Description:

The published artifact primarily provides Billions/Iden3 identity management tools for agents, with a nested package that fetches BTC/USDT prices from the Binance public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web3dropper](https://clawhub.ai/user/web3dropper)

### License/Terms of Use:


## Use Case:

External developers and agents use this release for decentralized identity workflows such as creating DIDs, linking an agent identity to a human owner, signing challenges, and verifying signatures. The artifact also contains a nested lightweight crypto-price package that can fetch BTC/USDT market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill stores long-lived identity credentials under $HOME/.openclaw/billions, including powerful unencrypted keys.

Mitigation: Install only when the host account can be treated as sensitive, restrict local file permissions, and avoid importing valuable private keys through the documented --key command.

Risk: The security review says the artifact includes unrelated nested crypto-price code in addition to the primary identity-management skill.

Mitigation: Review the nested crypto-price package before trusting or executing the published artifact.

Risk: The security verdict is suspicious and indicates review is needed before installation.

Mitigation: Scan and review the release contents before deployment, and execute only the documented scripts needed for the intended workflow.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/web3dropper/skills/web3dropper-crypto-price)
- [Billions Network](https://billions.network/)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)
- [Nested crypto price README](artifact/scripts/my-agent-skill/README.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands; scripts return JSON or plain text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and openclaw for identity workflows; identity credentials are stored under $HOME/.openclaw/billions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
