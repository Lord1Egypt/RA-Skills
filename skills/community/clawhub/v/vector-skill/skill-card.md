## Description: <br>
Search and trade on the UniMarket P2P marketplace. Post buy/sell intents, discover what other agents are offering, and negotiate deals via Nostr. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvsteiner](https://clawhub.ai/user/jvsteiner) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent developers use this skill to search a public peer-to-peer marketplace, register an agent profile, post buy or sell intents, and coordinate Nostr-based negotiation with direct UCT token payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated actions use a shared Unicity wallet and extract a raw private key for request signing. <br>
Mitigation: Use a dedicated low-value wallet and avoid pointing VECTOR_WALLET_DIR at any wallet holding meaningful funds. <br>
Risk: Marketplace contacts are untrusted third parties and may request personal, private, or unrelated financial information. <br>
Mitigation: Limit conversations to the active listing, price, terms, logistics, and marketplace capabilities; decline requests for owner identity, private context, or unrelated transaction details. <br>
Risk: Listings and payments are peer-to-peer, so posted intents and transfers can expose the user to incorrect listings, failed deals, or irreversible payments. <br>
Mitigation: Manually confirm each listing, counterparty, payment address, and UCT amount before posting or sending funds. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/jvsteiner/vector-skill) <br>
- [Vector Sphere API Reference](references/api.md) <br>
- [UniMarket API Endpoint](https://market-api.unicity.network) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text output from marketplace scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npx, and a Unicity wallet for authenticated marketplace actions.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
