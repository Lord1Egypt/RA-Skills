## Description:

WalletChan helps agents drive the WalletChan browser extension as a human-in-the-loop co-pilot for web3 dapps, navigating dapp UIs and surfacing decoded transaction or signature requests for user review through the extension.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apoorvlathey](https://clawhub.ai/user/apoorvlathey)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use WalletChan to let an agent operate web3 dapp interfaces while the user reviews decoded wallet transaction or signature requests and approves or rejects them in WalletChan. Typical tasks include connecting a wallet, swapping tokens, supplying or depositing to DeFi, signing typed data, and checking on-chain balances through a dapp.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide a wallet-related Agent Password in chat and grants broad browser-control access for financial actions.

Mitigation: Use a fresh dedicated Chrome profile, bind the debugging port to localhost, never share the Master Password, and rotate or revoke the Agent Password after each session.

Risk: Browser automation can submit transactions or signatures if the reviewed details do not match the user's intent.

Mitigation: Keep the WalletChan tab visible, have the user review decoded details before approval, and reject unexpected contracts, recipients, chains, unlimited allowances, predicted reverts, or any request the agent cannot fully explain.

Risk: Exposing Chrome remote debugging beyond localhost can allow unwanted browser control.

Mitigation: Keep the debugging port bound to localhost only and close the debugging session immediately after use.

## Reference(s):

- [WalletChan homepage](https://walletchan.com/)
- [WalletChan ClawHub skill page](https://clawhub.ai/apoorvlathey/skills/walletchan)
- [WalletChan source repository listed by the skill](https://github.com/apoorvlathey/walletchan-skill)
- [WalletChan Chrome Web Store listing](https://chromewebstore.google.com/detail/walletchan/kofbkhbkfhiollbhjkbebajngppmpbgc)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and human-readable wallet action summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent controlling an existing local Chrome session through CDP and summarizing wallet requests for user confirmation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
