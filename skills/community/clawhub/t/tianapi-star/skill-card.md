## Description:

查询十二星座每日运势，包含综合、爱情、工作指数及幸运色等详情。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query daily horoscope details for the twelve zodiac signs through TianAPI. It helps an agent collect overall, love, work, finance, health, lucky color, lucky number, and summary fields, then present them clearly to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The TianAPI key can be exposed if passed on the command line or committed in scripts/.env.

Mitigation: Use a dedicated low-privilege TianAPI key, prefer the TIANAPI_STAR_KEY environment variable, avoid command-line key arguments, and do not commit scripts/.env.

Risk: Using the skill sends horoscope requests to TianAPI over the network.

Mitigation: Confirm that sending the requested zodiac sign and date to TianAPI is acceptable for the intended user and deployment context.

## Reference(s):

- [TianAPI Star Horoscope API documentation](https://www.tianapi.com/apiview/78)
- [ClawHub tianapi-star skill page](https://clawhub.ai/workxin/skills/tianapi-star)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON from the helper script and concise text or Markdown horoscope summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TIANAPI_STAR_KEY; horoscope requests are sent to TianAPI over the network.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
