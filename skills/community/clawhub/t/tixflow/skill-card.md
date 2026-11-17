## Description:

AI-powered event assistant for discovering, booking, and coordinating event tickets. Integrates with KYD Labs protocol and Google Calendar.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seenfinity](https://clawhub.ai/user/seenfinity)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use TixFlow to discover events, compare ticket options, coordinate waitlists, purchase or mint tickets, and create calendar entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticket purchase, cNFT minting, wallet, waitlist, and calendar actions can create transactions or account changes without clear consent and scoping safeguards.

Mitigation: Require explicit user confirmation for each ticket purchase, mint, wallet, waitlist, or calendar-write action, and verify event, quantity, price, destination wallet, and account details before proceeding.

Risk: Calendar, ticketing, mapping, and minting integrations may expose broader access than the user intended when API keys are provided.

Mitigation: Provide only the API keys needed for the intended task, scope credentials narrowly, and prefer demo mode until the CrossMint/KYD, Google Calendar, and Maps behavior has been reviewed.

## Reference(s):

- [TixFlow on ClawHub](https://clawhub.ai/seenfinity/skills/tixflow)
- [seenfinity publisher profile](https://clawhub.ai/user/seenfinity)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Agent-facing text with JavaScript action results and configuration requirements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference Google Calendar, KYD Labs, Google Maps, CrossMint, wallet, waitlist, and ticketing actions depending on available configuration.]

## Skill Version(s):

0.2.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
