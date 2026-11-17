## Description:

Send Web Push notifications from a Node.js backend using the web-push npm library, including VAPID authentication, payload encryption, browser subscriptions, CLI usage, compatibility notes, and common pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add browser push notifications to Node.js backends with the web-push package. It helps with VAPID key setup, browser subscription handling, notification sends, CLI usage, browser compatibility, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: VAPID private keys, GCM keys, and push subscription endpoint or key material can be exposed if copied into commands, logs, or shared examples.

Mitigation: Use environment variables or a secrets manager, avoid pasting real secrets into command-line arguments, and redact credential values before sharing outputs.

Risk: Stored browser push subscriptions may reveal user-linked endpoint data and should be treated as sensitive backend data.

Mitigation: Disclose push subscription storage to users, restrict backend access, and apply normal data protection controls for subscription records.

Risk: Installing the web-push CLI globally or without version pinning can introduce npm supply-chain drift.

Mitigation: Prefer a pinned local project dependency and review package provenance during normal npm dependency management.

## Reference(s):

- [web-push Complete API Reference](artifact/references/webpush.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes placeholder credentials and configuration examples; real push credentials and subscription data should be protected.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
