## Description:

Runs a local Kimi device-code sign-in and localhost proxy so self-hosted Space Duck instances can use the owner's Kimi membership, with an optional capped OpenRouter fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askegor](https://clawhub.ai/user/askegor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers running Space Duck on their own infrastructure can sign in to a Kimi membership and connect a compatible runtime through a local proxy. They can optionally configure a metered OpenRouter fallback.

### Deployment Geography for Use:

Global (Kimi inference is processed in China).

## Known Risks and Mitigations:

Risk: Changed authentication or API endpoint settings could route tokens and prompts to an unintended host.

Mitigation: Keep endpoint overrides unset unless needed, and confirm the destination hosts are trusted before signing in or sending prompts.

Risk: Concurrent fallback requests may exceed the stated daily cap and increase pay-per-token spend.

Mitigation: Leave OPENROUTER_API_KEY unset unless fallback is needed; when enabled, monitor usage and limit concurrent fallback requests.

Risk: Disabling proxy authentication may allow other local processes or users to use the proxy and spend the account's quota.

Mitigation: Keep bearer authentication enabled except on an isolated single-user machine.

## Reference(s):

- [ClawHub release](https://clawhub.ai/askegor/skills/space-duck-kimi-relay)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Command-line interaction and OpenAI-compatible JSON or SSE responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional pay-per-token fallback; default daily cap is 200 calls.]

## Skill Version(s):

0.10.5 (source: artifact/_meta.json and server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
