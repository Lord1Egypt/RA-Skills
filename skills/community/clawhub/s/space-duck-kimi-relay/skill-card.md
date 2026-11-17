## Description:

This optional Space Duck add-on signs users in to Kimi locally and provides a localhost proxy for inference through their Kimi membership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[askegor](https://clawhub.ai/user/askegor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers running self-hosted Space Duck installations use this skill to sign in to Kimi with a browser-approved device flow and connect their runtime to a local inference proxy.

### Deployment Geography for Use:

Global, except for workloads requiring Western data residency; Kimi inference is processed in China.

## Known Risks and Mitigations:

Risk: Overridden endpoints can receive authentication credentials.

Mitigation: Keep the default HTTPS endpoints and bearer authentication enabled; change endpoints only when you trust the destination.

Risk: Concurrent paid fallback requests can exceed the advertised local daily cap.

Mitigation: Enable OpenRouter fallback only if you accept paid requests, and set provider-side spending limits because the local cap is not reliable under concurrency.

Risk: Kimi inference is processed in China, without Western data residency.

Mitigation: Do not route conversations through this skill when Western data residency is required.

Risk: Printed credentials or an always-on background service can expose secrets or run when unwanted.

Mitigation: Protect printed secrets and install the background service only when wanted.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/askegor/skills/space-duck-kimi-relay)
- [Kimi authentication service](https://auth.kimi.com)
- [OpenRouter API (optional paid fallback)](https://openrouter.ai/api/v1)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Text and Markdown with shell commands and endpoint configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May print a short-lived access token when the token command is explicitly requested; protect printed secrets.]

## Skill Version(s):

0.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
