## Description:

Unusual options activity radar for US stocks and ETFs: end-of-day IV rank, implied volatility, options sentiment, put/call percentile, 25-delta skew, open-interest walls, and max pain, each ranked against the ticker's own trailing history.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesentitrader](https://clawhub.ai/user/thesentitrader)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to review end-of-day options positioning and activity for covered US stocks and ETFs, including how readings compare with each ticker's own history. It provides informational research context, not personalized investment advice or forecasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API provider receives research queries, and the skill requires an API key for requests.

Mitigation: Keep the key in the environment and send it only in the authentication header; avoid including sensitive information in research queries.

Risk: Options analytics can be overread as live order flow, a forecast, or trading advice.

Mitigation: State the session date and percentile context, describe the results as educational information, and do not present them as personalized buy or sell recommendations.

## Reference(s):

- [SentiSense API documentation](https://sentisense.ai/docs/api/)
- [SentiSense](https://sentisense.ai)
- [SentiSense API key](https://app.sentisense.ai/get-api-key)
- [ClawHub skill release](https://clawhub.ai/thesentitrader/skills/unusual-options-activity)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Concise sourced Markdown analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Informational end-of-day options analytics; not a forecast or personalized recommendation.]

## Skill Version(s):

1.8.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
