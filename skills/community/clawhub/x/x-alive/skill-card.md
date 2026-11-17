## Description:

X Alive helps AI agents maintain an authentic X/Twitter presence through organic engagement, trend awareness, deduplication, safety defaults, and human oversight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kitakitsune0x](https://clawhub.ai/user/kitakitsune0x)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use X Alive to configure an AI agent's X/Twitter identity, engagement loop, posting and reply practices, and safety boundaries for public account activity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables recurring public posting, replies, quotes, and other account-affecting X/Twitter actions.

Mitigation: Define explicit operator policies for allowed actions and require human approval for public write actions until the agent is trusted.

Risk: X API keys and bearer tokens can expose the account if stored loosely or shared with unreviewed tools.

Mitigation: Store credentials in a secret manager or restrict environment-file permissions, and pin or audit the x-research dependency before giving it token access.

Risk: Token, ticker, contract-address, money, legal, harassment, impersonation, or viral incidents can create public safety and reputational risk.

Mitigation: Keep the skill's default silence posture for high-risk interactions and route these cases to the human operator before any public response.

## Reference(s):

- [X Developer Platform](https://developer.x.com)
- [xurl CLI](https://github.com/xdevplatform/xurl)
- [x-research skill](https://github.com/rohunvora/x-research-skill)
- [X Alive on ClawHub](https://clawhub.ai/kitakitsune0x/skills/x-alive)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X API credentials and operator-defined policies before public account actions.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
