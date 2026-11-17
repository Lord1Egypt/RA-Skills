## Description:

Connect your agent to Airbnb, Booking.com & VRBO via Vanio AI, with tools for reservations, guests, messaging, smart locks, payments, workflows, and vacation-rental operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivannikolovbg](https://clawhub.ai/user/ivannikolovbg)

### License/Terms of Use:

MIT-0

## Use Case:

Property managers and vacation-rental operators use this skill to connect an OpenClaw agent to Vanio AI for guest communication, reservations, smart locks, payments, listings, tasks, workflows, analytics, and related operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad authority over guest messages, reservations, payments, smart locks, listings, and workflows.

Mitigation: Install only when Vanio is trusted with the connected rental accounts, and require human review for high-impact actions such as charges, cancellations, refunds, lock changes, or workflow changes.

Risk: API keys may be stored locally or exposed through terminal output, shell history, or logs.

Mitigation: Prefer VANIO_API_KEY from a secure environment, avoid pasting keys into shared terminals, protect ~/.config/vanio/config.json, and rotate keys if exposure is suspected.

Risk: A custom VANIO_API_URL or baseUrl can redirect requests and credentials to an unintended service.

Mitigation: Use the default Vanio API endpoint unless you control the alternate endpoint, and verify configuration before authenticating or running operational commands.

## Reference(s):

- [Vanio AI](https://www.vanio.ai)
- [ClawHub Skill Page](https://clawhub.ai/ivannikolovbg/skills/vanio)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Vanio CLI and VANIO_API_KEY; responses may perform or guide sensitive rental-management actions through Vanio AI.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
