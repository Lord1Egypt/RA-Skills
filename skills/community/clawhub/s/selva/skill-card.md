## Description:

Shopping platform for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpbonch](https://clawhub.ai/user/jpbonch)

### License/Terms of Use:


## Use Case:

External users and agents use Selva to search, compare, inspect, and buy physical products from Amazon through a CLI workflow. The skill also supports profile setup, hosted payment-card setup, order tracking, and purchase approval flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real product orders and create financial commitments.

Mitigation: Require explicit human approval of the exact item, seller, total price, shipping details, and payment method before any purchase.

Risk: Passing card number, expiry, and CVV on the command line can expose sensitive payment details through shell history or process inspection.

Mitigation: Prefer the hosted settings-page card flow and avoid entering payment-card details directly in CLI arguments.

Risk: The local Selva API key is stored on disk and could be misused if exposed.

Mitigation: Protect or rotate the local API key and use a pinned, vetted CLI version before deployment.

## Reference(s):

- [ClawHub Selva skill page](https://clawhub.ai/jpbonch/skills/selva)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline CLI commands and plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product titles, prices, ratings, review counts, delivery estimates, image URLs, settings links, and order statuses.]

## Skill Version(s):

1.0.0 (source: server release metadata; package.json version is 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
