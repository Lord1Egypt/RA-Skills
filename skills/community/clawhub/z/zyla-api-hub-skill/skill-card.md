## Description:

Zyla API Hub Skill connects an OpenClaw agent to Zyla API Hub so it can discover and call production APIs for weather, finance, translation, email validation, geolocation, and related tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alebrega](https://clawhub.ai/user/alebrega)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an OpenClaw agent search Zyla API Hub, configure a Zyla API key, call selected APIs, and review quota or billing status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Zyla API key for authenticated third-party API calls.

Mitigation: Store the key in protected configuration or a secret store, avoid pasting it into chat, and rotate it if it appears in logs or conversation history.

Risk: The hub URL can be configured, which changes the network destination used for catalog and API requests.

Mitigation: Review the configured hub URL before use and keep it pointed at the expected Zyla API Hub endpoint.

Risk: API calls may process sensitive personal or financial data and may incur pay-as-you-go charges.

Mitigation: Send only data needed for the task, confirm the API and endpoint before high-volume use, and monitor quota, rate-limit, and billing status.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alebrega/skills/zyla-api-hub-skill)
- [Zyla OpenClaw Connect](https://zylalabs.com/openclaw/connect)
- [Zyla API Hub](https://zylalabs.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON API results and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API response data and rate-limit or usage fields returned by Zyla.]

## Skill Version(s):

1.0.7 (source: ClawHub release evidence; artifact package.json reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
