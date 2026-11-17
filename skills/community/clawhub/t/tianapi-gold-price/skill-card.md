## Description:

Queries real-time precious-metal market data, including gold and silver buy prices, sell prices, highs, lows, latest prices, and percent changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve current precious-metal price data from TianAPI and present structured quote details for requested metal codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a TianAPI API key and makes HTTPS requests to TianAPI.

Mitigation: Set TIANAPI_GOLD_KEY in the environment, avoid passing keys on the command line, do not commit scripts/.env, and rotate the key if it appears in shell history, logs, or shared screenshots.

## Reference(s):

- [TianAPI Gold Price API Documentation](https://www.tianapi.com/apiview/146)
- [ClawHub Skill Page](https://clawhub.ai/workxin/skills/tianapi-gold-price)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; helper script returns JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TIANAPI_GOLD_KEY. The helper returns success, data, and error fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
