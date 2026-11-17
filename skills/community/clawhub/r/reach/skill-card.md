## Description:

Agent web interface. Browse websites, fill forms, login to services, sign transactions, send/receive email, solve CAPTCHAs, and interact with the web autonomously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potdealer](https://clawhub.ai/user/potdealer)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use Reach to automate web browsing, form interaction, login sessions, email workflows, screenshots, monitoring, and wallet signing or payment tasks through JavaScript, CLI, or MCP interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive browser sessions and cookies may be stored locally.

Mitigation: Run Reach in an isolated environment with low-privilege service accounts and hardened credential storage.

Risk: Signing and payment actions can use wallet private keys and send funds.

Mitigation: Use a limited wallet, set strict x402 payment limits, and require explicit human review before sign or pay actions.

Risk: Inbound webhook handling may expose email or integration data.

Mitigation: Bind webhook services to localhost or place them behind authenticated ingress before accepting external traffic.

Risk: Outbound email automation can send messages through configured API keys.

Mitigation: Use low-privilege email credentials and require explicit review before email actions.

## Reference(s):

- [Reach ClawHub skill page](https://clawhub.ai/potdealer/skills/reach)
- [Reach README](artifact/README.md)
- [Reach test report](artifact/TEST-REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Configuration]

**Output Format:** [Markdown, JSON, screenshots, local files, shell commands, and tool-call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local browser sessions, cookies, state records, inbox files, webhook logs, screenshots, signatures, and payment receipts.]

## Skill Version(s):

0.2.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
