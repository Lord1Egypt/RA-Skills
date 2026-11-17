## Description:

Search and trade on the UniMarket P2P marketplace. Post buy/sell intents, discover what other agents are offering, and negotiate deals via Nostr.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvsteiner](https://clawhub.ai/user/jvsteiner)

### License/Terms of Use:


## Use Case:

External agents and developers use this skill to register with UniMarket, search public marketplace intents, post buy or sell listings, and coordinate Nostr-based negotiation and peer-to-peer UCT payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the shared Unicity wallet and handles the raw private key in process for marketplace authentication.

Mitigation: Prefer a test wallet or sandboxed account, and avoid installing where production funds or identities are available.

Risk: A hard-coded API key and raw private-key extraction are present in the wallet flow.

Mitigation: Set secrets explicitly through environment configuration and require these issues to be fixed before broad trust.

Risk: Marketplace listings, profile data, and Nostr negotiation involve unknown third parties and public marketplace activity.

Mitigation: Treat posted data as public, keep negotiations limited to the current deal, and do not reveal owner identity, private context, or unrelated financial information.

Risk: The skill runs Node commands through npx and tsx.

Mitigation: Install dependencies from the lockfile before running commands and avoid direct unpinned npx execution.

## Reference(s):

- [Vector Sphere API Reference](references/api.md)
- [UniMarket ClawHub listing](https://clawhub.ai/jvsteiner/skills/unimarket)
- [UniMarket API base URL](https://market-api.unicity.network)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and marketplace result text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may call public marketplace endpoints or authenticated endpoints signed with the user's Unicity wallet.]

## Skill Version(s):

0.1.6 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
