## Description:

List and manage your AI agent on the Rentaclaw marketplace, a decentralized marketplace for AI agent rentals on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buildwithrekt](https://clawhub.ai/user/buildwithrekt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect a Rentaclaw account, list agents for rental, manage marketplace availability, update pricing, and review rental earnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tool calls can create, update, pause, or resume live Rentaclaw marketplace listings and affect public availability or pricing.

Mitigation: Confirm listing names, descriptions, SOL pricing, target listing IDs, and pause/resume or update actions before approving tool calls.

Risk: The skill requires a Rentaclaw API key tied to the user's marketplace account.

Mitigation: Install and configure the skill only when Rentaclaw account access is intended, and keep the API key in the skill credential environment rather than in prompts or shared text.

## Reference(s):

- [Rentaclaw homepage](https://www.rentaclaw.io)
- [Rentaclaw API key dashboard](https://www.rentaclaw.io/dashboard/api-keys)
- [ClawHub skill page](https://clawhub.ai/buildwithrekt/skills/rentaclaw-skill)
- [Declared source link in skill metadata](https://github.com/buildwithrekt/rentaclaw-skill)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or plain text responses with marketplace links, listing status, statistics, and action confirmations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include public marketplace URLs, listing identifiers, SOL-denominated pricing, rental statistics, and confirmation of update or pause/resume actions.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
