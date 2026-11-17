## Description:

Delegates precise, formalizable computations and factual lookups to Wolfram|Alpha's LLM API so agents can request concise computed results with optional disambiguation, localization, units, and response-length controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[firefrog-pepe](https://clawhub.ai/user/firefrog-pepe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when an assistant needs reliable arithmetic, unit conversion, symbolic math, statistics, finance math, or structured factual lookups from Wolfram|Alpha instead of relying on model-only reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive or precise-location query data may be sent to Wolfram|Alpha or stored in the local cache.

Mitigation: Use the skill only for appropriate queries, avoid IP, latitude/longitude, or precise location unless needed, and pass --cache off for sensitive or time-sensitive requests.

Risk: Using query-string authentication can expose the Wolfram AppID in URLs or logs.

Mitigation: Keep the default bearer authentication and avoid --auth query unless the environment requires it.

## Reference(s):

- [Wolfram|Alpha LLM API notes](references/llm-api.md)
- [Full Results API parameter reference notes](references/full-api-params.md)
- [Wolfram|Alpha LLM API documentation](https://products.wolframalpha.com/llm-api/documentation)
- [Wolfram|Alpha API parameter reference](https://products.wolframalpha.com/api/documentation?scrollTo=parameter-reference)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text API responses with Markdown guidance and inline bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WOLFRAM_APP_ID; default response cap is 2500 characters and default local cache TTL is 7 days.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
