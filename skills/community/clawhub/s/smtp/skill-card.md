## Description:

Send, test, and debug SMTP mail flows with safe dry runs, provider-aware auth, and deliverability checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure, test, send, and diagnose outbound SMTP mail while separating drafts, probes, canary sends, live sends, authentication, TLS, relay policy, and deliverability checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved SMTP probes or live sends can disclose message content, recipients, headers, and attachments to the configured SMTP provider and DNS infrastructure.

Mitigation: Use approved canary inboxes first, confirm every live send, and keep recipient scope limited until delivery evidence is verified.

Risk: SMTP credentials, API tokens, private keys, full recipient lists, or full message bodies could be exposed if stored in local notes.

Mitigation: Provide credentials only through a trusted runtime secret source and keep ~/smtp notes free of secrets and unnecessary message or recipient data.

Risk: A successful SMTP acceptance response can be mistaken for final inbox delivery.

Mitigation: Verify final state through inbox, spam-folder, bounce, DSN, or provider-log evidence before reporting delivery success or scaling recipient scope.

## Reference(s):

- [ClawHub SMTP Skill Page](https://clawhub.ai/ivangdavila/skills/smtp)
- [SMTP Skill Homepage](https://clawic.com/skills/smtp)
- [Setup - SMTP](artifact/setup.md)
- [Send Flow - SMTP](artifact/send-flow.md)
- [Diagnostic Playbook - SMTP](artifact/diagnostic-playbook.md)
- [Deliverability - SMTP](artifact/deliverability.md)
- [swaks Recipes - SMTP](artifact/swaks-recipes.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses explicit confirmation gates before live sends and records only minimal, redacted local SMTP evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
