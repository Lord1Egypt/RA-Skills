## Description:

Shipz helps an AI agent manage a user's dating workflow through the Shipz REST API, including consent-based onboarding, profile setup, discovery, swiping, matching, conversations, account controls, and webhook notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunelabs](https://clawhub.ai/user/dunelabs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to operate a Shipz dating account through API-guided workflows. The skill covers registration, profile and preference management, candidate discovery, swiping, matches, conversations, reporting, blocking, unmatching, key management, account deletion, and webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad control over sensitive dating and account actions, including irreversible account deletion, API key revocation, blocking, unmatching, webhook registration, and sharing contact information.

Mitigation: Ask for explicit user confirmation before account deletion, key revocation, blocking or unblocking, unmatching, webhook registration, or sharing contact information.

Risk: The SHIPZ_API_KEY grants full access to the user's Shipz account.

Mitigation: Keep the API key out of messages, logs, and conversations; rotate it immediately if compromise is suspected.

Risk: Profiles, photos, PINs, and conversations can expose sensitive personal and dating information.

Mitigation: Build profiles only from user-provided facts, avoid fabricating details, do not cache signed photo URLs, and share PINs or contact details only with the intended recipient after consent.

Risk: Webhook registration can send match and message events to external endpoints.

Mitigation: Register only webhook URLs controlled by the user and verify incoming webhook signatures with the one-time secret.

## Reference(s):

- [Shipz homepage](https://shipz.ai)
- [ClawHub skill page](https://clawhub.ai/dunelabs/skills/shipz)
- [Dune Labs publisher profile](https://clawhub.ai/user/dunelabs)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown guidance with REST endpoint descriptions and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SHIPZ_API_KEY for authenticated Shipz API actions.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
