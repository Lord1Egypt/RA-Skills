## Description:

Token Layer provides censorship resistant crosschain public token infrastructure for launching once and trading everywhere.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisciszak](https://clawhub.ai/user/chrisciszak)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to guide agents through Token Layer wallet checks, token creation, price quotes, trades, reward claims, and blockchain transaction submission through Token Layer APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create tokens, trade tokens, claim rewards, and submit blockchain transactions with a funded Token Layer agent wallet.

Mitigation: Require explicit user approval for every create, buy, sell, claim, and send-transaction action, and verify wallet balances before use.

Risk: Broad phrases may delegate financial decisions to the agent.

Mitigation: Confirm token details, chain, amount, trade direction, and transaction submission unless the user explicitly authorizes autonomy for that specific action.

Risk: The skill may store email, user IDs, or referral state across sessions.

Mitigation: Store only intentional, minimal account or referral state in private agent memory, and avoid shared memory or TOOLS.md unless the user accepts that tracking.

## Reference(s):

- [Token Layer homepage](https://tokenlayer.network)
- [Token Layer API base](https://api.tokenlayer.network/functions/v1)
- [Token Layer agent wallets](https://app.tokenlayer.network/agent-wallets)
- [ClawHub skill page](https://clawhub.ai/chrisciszak/skills/token-layer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with bash curl examples and JSON request payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires jq, curl, and TOKENLAYER_API_KEY; actions can produce blockchain transaction payloads for explicit user-approved execution.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
