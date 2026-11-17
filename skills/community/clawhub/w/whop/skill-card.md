## Description:

Run and grow a Whop business with better offers, checkout flows, promo strategy, affiliates, ads, tracking, analytics, support operations, and advanced API workflows when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, marketers, and developers use this skill to plan and run Whop offers, checkout flows, promo codes, affiliates, ads, analytics, support operations, and optional API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advanced workflows can send Whop business, customer, payment, webhook, and growth data to Whop APIs.

Mitigation: Use API workflows only when they are needed, keep credentials in environment variables, and install only when Whop is trusted with the relevant business data.

Risk: Local memory under ~/whop/ can retain Whop business notes.

Mitigation: Store only non-secret business metadata in local notes and keep API keys, webhook secrets, and other secret values out of memory and project files.

Risk: Payment, trial, or webhook changes tested directly in production can affect real customers or money movement.

Mitigation: Use Whop sandbox with separate keys, webhook configuration, and test cards before moving payment or webhook workflows to production.

Risk: The optional Whop development proxy adds a local package dependency for embedded app testing.

Mitigation: Pin and review @whop-apps/dev-proxy before installation, and use it only when local embedded app behavior needs to be tested.

## Reference(s):

- [ClawHub Whop Skill Release](https://clawhub.ai/ivangdavila/skills/whop)
- [Whop Skill Homepage](https://clawic.com/skills/whop)
- [Whop API](https://api.whop.com/api/v1)
- [Whop Documentation](https://docs.whop.com/)
- [Whop Sandbox](https://sandbox.whop.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with optional code blocks, shell commands, and JSON or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dashboard workflows, local note structures, API calls, webhook checks, sandbox testing steps, and proxy setup guidance; does not require API credentials for dashboard-only use.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
