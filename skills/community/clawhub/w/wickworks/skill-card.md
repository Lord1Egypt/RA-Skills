## Description:

Computes technical indicators and Smart-Money-Concepts primitives from OHLC candlestick bars through a stateless REST or MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Wickworks to compute technical indicators and market-structure primitives from OHLC bar data. The service returns data for analysis but does not provide forecasts or buy/sell opinions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Docker setup references a mutable `latest` image, and scanner analysis was partial.

Mitigation: Review the image's provenance and use a reviewed, pinned digest before deployment.

Risk: The service has no built-in authentication, so anyone who can reach its port can submit requests.

Mitigation: Bind it to loopback by default; protect off-host access with an authenticated reverse proxy or VPN.

Risk: OHLC bars are sent to the configured Wickworks instance for computation.

Mitigation: Review the service destination and data sent, and use an instance you or a trusted operator controls.

## Reference(s):

- [Setup guide](references/setup.md)
- [Wickworks repository](https://github.com/psyb0t/docker-wickworks)
- [Wickworks OpenClaw plugin](https://github.com/psyb0t/docker-wickworks/tree/main/.agents/plugins/wickworks)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [Wickworks on ClawHub](https://clawhub.ai/psyb0t/skills/wickworks)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON arrays, time series, and structured objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [camelCase fields; NaN values are serialized as null.]

## Skill Version(s):

0.7.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
