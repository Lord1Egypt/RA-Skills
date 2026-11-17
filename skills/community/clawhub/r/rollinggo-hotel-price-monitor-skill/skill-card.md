## Description:

RollingGo Hotel Booking helps agents search hotels, compare room options and live prices, guide OAuth login, create confirmed hotel reservations after user approval, and return order or payment status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rollinggo-ai](https://clawhub.ai/user/rollinggo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search and compare hotels, inspect room prices and cancellation policies, and create hotel bookings only after explicit user confirmation.

### Deployment Geography for Use:

China-focused release with global hotel inventory coverage.

## Known Risks and Mitigations:

Risk: Installer and update flows use mutable latest packages or executable downloads.

Mitigation: Install only if RollingGo is trusted, and prefer a pinned, verified release or platform-managed install before sensitive use.

Risk: The skill can create payable hotel reservations and process personal booking data such as name and email.

Mitigation: Review booking details, price, cancellation policy, and contact information carefully, and require explicit user confirmation before order creation.

## Reference(s):

- [CLI command parameter reference](artifact/references/cli-params.md)
- [ClawHub skill page](https://clawhub.ai/rollinggo-ai/skills/rollinggo-hotel-skill-cn-new)
- [RollingGo Hotel CLI release downloads](https://github.com/RollingGo-AI/oauth-hotel-cli/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown hotel cards and order summaries, with shell commands for the agent to execute.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before price locking or creating a payable reservation.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
