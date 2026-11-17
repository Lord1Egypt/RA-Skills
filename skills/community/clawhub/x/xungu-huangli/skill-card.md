## Description:

循古黄历获取中国万年历信息，包括二十四节气、农历日期、宜忌、吉凶和黄道吉日等内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnyouker](https://clawhub.ai/user/cnyouker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Chinese almanac questions about solar terms, lunar dates, auspicious activities, inauspicious activities, lucky hours, ganzhi calendar details, moon phases, Taoist calendar dates, and Buddhist calendar dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The sample runtime code may expose unrelated secrets by loading key-value pairs from .env files into the agent process.

Mitigation: Use a dedicated OpenClaw secret or environment variable for HUANGLI_API_TOKEN, avoid colocating unrelated secrets in the same .env files, and prefer code that loads only HUANGLI_API_TOKEN.

## Reference(s):

- [循古排盘](https://xungufa.com)
- [循古黄历 Calendar API](https://xungufa.com/huangli/api/calendar)
- [ClawHub skill page](https://clawhub.ai/cnyouker/skills/xungu-huangli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, API Calls, Configuration]

**Output Format:** [Formatted Chinese almanac text with supporting Python code and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HUANGLI_API_TOKEN for live API calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
