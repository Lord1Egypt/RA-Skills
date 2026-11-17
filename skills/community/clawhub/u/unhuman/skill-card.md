## Description:

Search, register, and manage domain names via unhuman.domains, including DNS records, nameservers, renewals, recovery, and optional bitcoin payment with agent-wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satbot-mdk](https://clawhub.ai/user/satbot-mdk)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search for domains, register or renew domains, manage DNS records, update nameservers, and recover management tokens through the unhuman CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm commands are used for sensitive domain-management and bitcoin-wallet operations.

Mitigation: Review before installing and use pinned, reviewed versions of npm packages.

Risk: Domain-management tokens and wallet data can control domains or funds if exposed.

Mitigation: Keep domain-management tokens and wallet data isolated and protect local token and wallet storage.

Risk: Wallet-enabled registration or renewal can trigger real bitcoin payments.

Mitigation: Require clear user approval before registrations, renewals, DNS or nameserver changes, and any wallet-enabled payment.

## Reference(s):

- [unhuman.domains](https://unhuman.domains)
- [unhuman npm package](https://www.npmjs.com/package/unhuman)
- [ClawHub skill page](https://clawhub.ai/satbot-mdk/skills/unhuman)
- [ClawHub publisher profile](https://clawhub.ai/user/satbot-mdk)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that may affect domain registration, DNS, nameservers, renewals, local management-token storage, and wallet-enabled bitcoin payments.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
