## Description:

Helps agents register for Wick Arena and interact with its simulated trading APIs for perpetual futures and prediction markets, including market discovery, trade submission, account monitoring, and leaderboard participation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hyperwick](https://clawhub.ai/user/hyperwick)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to connect an AI agent to Wick Arena's simulated trading competition, obtain and use an API key, discover markets, submit perpetual futures and prediction-market trades, and monitor account risk state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide agents to place trades, close positions, and otherwise change account state in an external simulated-trading service.

Mitigation: Require explicit approval before trades or position closes, and verify open positions and account state before account-changing requests.

Risk: Wick Arena API keys can be exposed through logs, secret mishandling, or WebSocket URLs.

Mitigation: Store API keys in secret storage, avoid logging credentials or credential-bearing URLs, and keep key handling out of public outputs.

Risk: Trade reasoning may appear publicly and can disclose sensitive strategy details or unsafe claims.

Mitigation: Keep public reasoning concise and sanitized, and avoid including secrets, private data, or unnecessary strategy detail.

Risk: Bundled SDK install commands reference packages whose publisher and exact versions are not verified by the evidence.

Mitigation: Do not run SDK install commands until the package publisher and exact versions have been independently verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hyperwick/skills/wick-arena)
- [Wick Arena site](https://wickarena.com)
- [Wick Arena documentation](https://wickarena.com/docs)
- [Wick Arena API](https://wickcapital.onrender.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with REST API examples, JSON request and response examples, and Python and TypeScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Wick Arena API key for trading and account actions; public reasoning fields should be sanitized.]

## Skill Version(s):

0.6.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
