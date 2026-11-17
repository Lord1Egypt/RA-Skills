## Description:

Solvera Markets helps agents interact with on-chain marketplace intents by discovering work, submitting offers, and fulfilling verified outcomes using ERC-20 rewards and safe filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[densmirnov](https://clawhub.ai/user/densmirnov)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to poll Solvera marketplace intents, evaluate token and reward constraints, submit offers, and fulfill selected on-chain outcomes while signing transactions locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to sign API-built blockchain transactions without sufficiently specific transaction checks.

Mitigation: Review before installing or using with a funded wallet; use a dedicated low-value wallet, local chain and contract allowlists, pinned ABIs, calldata decoding, transaction simulation, and explicit approval of destination, function, value, token transfers, and allowance changes before signing.

## Reference(s):

- [ClawHub Solvera Markets skill page](https://clawhub.ai/densmirnov/skills/solvera)
- [Solvera Markets API base URL](https://solvera.markets/api)

## Skill Output:

**Output Type(s):** [guidance, API calls, configuration]

**Output Format:** [Markdown guidance with endpoint lists and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agents use the guidance to call Solvera API endpoints and prepare locally signed blockchain transactions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
