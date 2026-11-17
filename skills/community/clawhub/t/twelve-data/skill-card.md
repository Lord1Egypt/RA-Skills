## Description:

Use Twelve Data REST and WebSocket APIs for market quotes, latest prices, historical time series, symbol discovery, and technical indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[softtrymee](https://clawhub.ai/user/softtrymee)

### License/Terms of Use:


## Use Case:

Developers and market-data users use this skill to configure Twelve Data access, construct REST and WebSocket requests, retrieve live and historical multi-asset data, and add technical or fundamentals endpoints when appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be exposed when copied into request URLs, logs, browser history, or shared command output.

Mitigation: Prefer the Authorization header pattern, avoid logging URLs containing apikey values, and protect any environment or configuration file storing TWELVEDATA_API_KEY.

## Reference(s):

- [Twelve Data Documentation](https://twelvedata.com/docs)
- [Twelve Data Request Guide](https://support.twelvedata.com/en/articles/5620512-how-to-create-a-request)
- [Twelve Data Trial Information](https://support.twelvedata.com/en/articles/5335783-trial)
- [ClawHub Skill Page](https://clawhub.ai/softtrymee/skills/twelve-data)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Twelve Data API key for normal API use.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
