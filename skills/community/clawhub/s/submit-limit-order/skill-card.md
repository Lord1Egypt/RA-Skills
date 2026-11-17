## Description:

Submit a UniswapX Dutch auction limit order for a token pair, with optional price and expiry controls and order-status monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

External users and trading agents use this skill to prepare and submit UniswapX limit orders after collecting token pair, amount, chain, limit price, and expiry details. It is intended for workflows where the user wants a gasless Dutch auction order with status reporting instead of an immediate swap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad prompt could result in live crypto order submission without a separate confirmation step.

Mitigation: Require the agent to show the token pair, amount, chain, limit price, expiry, estimated output, and order target, then wait for explicit user approval before submission.

Risk: Mutable remote install sources can change after review.

Mitigation: Use pinned or immutable install sources where possible and review file hashes before enabling the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wpank/skills/submit-limit-order)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown status summaries with order parameters and order hash when submitted]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform live UniswapX order submission through configured Uniswap tools; require explicit user approval before submission.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
