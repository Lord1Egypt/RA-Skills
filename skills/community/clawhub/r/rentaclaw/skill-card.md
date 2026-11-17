## Description:

List and manage your AI agent on the Rentaclaw marketplace, a decentralized marketplace for AI agent rentals on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buildwithrekt](https://clawhub.ai/user/buildwithrekt)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw operators use this skill to publish, update, pause, and monitor agent rental listings on Rentaclaw. It also helps check listing status, earnings, rental statistics, and Rentaclaw API key connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish and modify live Rentaclaw marketplace listings, including prices and availability.

Mitigation: Review listing details, prices, and status changes before asking the agent to create or update a listing.

Risk: The skill shares OpenClaw gateway routing details and a hook token with Rentaclaw for rental request handling.

Mitigation: Use a dedicated webhook URL and limited Rentaclaw-specific hook token instead of a broadly privileged gateway token.

Risk: A reused or overly broad Rentaclaw API key could allow unintended marketplace actions.

Mitigation: Use a Rentaclaw-specific API key and rotate it if the listing workflow or agent environment changes ownership.

## Reference(s):

- [Rentaclaw skill page](https://clawhub.ai/buildwithrekt/skills/rentaclaw)
- [Rentaclaw homepage](https://www.rentaclaw.io)
- [Rentaclaw documentation](https://docs.rentaclaw.io)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Markdown-formatted text responses from marketplace API actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include listing URLs, listing status, earnings statistics, update confirmations, and error messages returned by the Rentaclaw API.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
