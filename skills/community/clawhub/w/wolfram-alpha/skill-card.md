## Description:

Perform complex mathematical calculations, physics simulations, data analysis, and scientific queries via the Wolfram|Alpha LLM API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robert-janssen](https://clawhub.ai/user/robert-janssen)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to send quantitative, scientific, data, unit-conversion, and factual queries to Wolfram|Alpha and return exact text answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries, including sensitive user input, are sent to Wolfram|Alpha.

Mitigation: Avoid submitting confidential queries unless that external processing is acceptable for the deployment context.

Risk: The WOLFRAM_APP_ID is a credential and may be exposed through verbose URL logging or diagnostics.

Mitigation: Redact appid values in logs and diagnostics, monitor quota use, and rotate the app ID if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robert-janssen/skills/wolfram-alpha)
- [Wolfram|Alpha LLM API endpoint](https://www.wolframalpha.com/api/v1/llm-api)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text returned by the Wolfram|Alpha LLM API, with shell command and environment configuration guidance in documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, the requests package, and a WOLFRAM_APP_ID environment variable.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
