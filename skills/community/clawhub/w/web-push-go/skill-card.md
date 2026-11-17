## Description:

Send Web Push notifications from a Go backend using webpush-go (VAPID authentication, payload encryption, subscription storage, and browser subscribe flow). Use when working with Push API subscriptions in Go, Web Push Protocol, VAPID key management, browser push notifications, or migrating a Node web-push implementation to Go. Covers VAPID key generation, encrypting payloads, the aes128gcm encoding, subscription persistence in Postgres, and the browser-side subscribe code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[monaxamo](https://clawhub.ai/user/monaxamo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Go services use this skill to set up browser push subscriptions, send Web Push notifications with VAPID, and manage subscription records and browser-side flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples need correction before production use, including library API details and endpoint safeguards.

Mitigation: Check API usage against the library documentation; validate every endpoint against an allowlist, prevent redirects to other hosts, and set request timeouts.

Risk: VAPID private keys and browser subscription records are sensitive.

Mitigation: Keep private keys in secret storage, restrict access to subscription records, and preserve user-controlled subscribe and unsubscribe actions.

## Reference(s):

- [Go API reference](references/go-api.md)
- [Browser-side guide](references/browser-side.md)
- [webpush-go library](https://github.com/SherClockHolmes/webpush-go)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go, JavaScript, SQL, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
