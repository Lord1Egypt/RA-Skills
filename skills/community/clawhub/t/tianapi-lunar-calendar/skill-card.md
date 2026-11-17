## Description:

查询中国老黄历，获取指定日期的宜忌、冲煞、吉时、胎神等传统民俗信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up Chinese lunar-calendar almanac details for a requested date, including suitable and unsuitable activities, zodiac conflict information, auspicious directions, and related traditional calendar fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the configured TianAPI key and requested date to TianAPI.

Mitigation: Use a dedicated, restricted TianAPI key, prefer the TIANAPI_LUNAR_CALENDAR_KEY environment variable, avoid command-line key arguments, and rotate the key if exposure is suspected.

Risk: A local scripts/.env file can contain the TianAPI key.

Mitigation: Do not commit scripts/.env and review local files before publishing or sharing the skill.

Risk: Security evidence notes documentation/runtime bugs in the current script.

Mitigation: Test the script in a controlled environment and fix runtime issues before relying on it in production workflows.

## Reference(s):

- [TianAPI Chinese Lunar Calendar API](https://www.tianapi.com/apiview/45)
- [ClawHub Skill Page](https://clawhub.ai/workxin/skills/tianapi-lunar-calendar)
- [ClawHub Publisher Profile](https://clawhub.ai/user/workxin)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown-oriented text with shell command examples and optional JSON results from the TianAPI lookup script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a TianAPI key, preferably provided through TIANAPI_LUNAR_CALENDAR_KEY.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
