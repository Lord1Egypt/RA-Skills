## Description:

TACE (Tender Agentic Commerce Engine) runtime contract that provides concrete endpoint payloads and response schemas for authenticated commerce workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tender](https://clawhub.ai/user/tender)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and commerce agents use this skill to authenticate with TACE, discover products, place and monitor orders, manage subscriptions and waitlists, and submit feedback using documented API contracts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect purchases, payment state, subscriptions, waitlist positions, and account status.

Mitigation: Require fresh user confirmation before any order, cancellation, payment update, account deactivation, or deletion.

Risk: Mutable remote /skills.md instructions could expand behavior after installation.

Mitigation: Review remote skill updates before allowing them to change the agent's permitted behavior.

## Reference(s):

- [TACE on ClawHub](https://clawhub.ai/tender/skills/tace)
- [TACE Homepage](https://tender.cash)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request and response examples and optional curl-based API execution steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl for command-line API calls and optional TACE_ENV and TACE_SKILL_VERSION environment variables.]

## Skill Version(s):

1.0.6 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
