## Description: <br>
提供中国农历、黄历宜忌和吉凶择日查询，支持单日查询、区间筛选和关键词检索。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leocdchina](https://clawhub.ai/user/leocdchina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Chinese lunar calendar, Huangli almanac, auspicious-date, and date-conversion questions. It is useful for looking up a specific date, comparing date ranges, or finding dates that match traditional activity keywords. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends authenticated requests using HUANGLI_TOKEN, and changing HUANGLI_BASE controls where those requests are sent. <br>
Mitigation: Use a dedicated token, avoid exposing it in prompts or logs, and only set HUANGLI_BASE to a trusted Huangli API endpoint. <br>
Risk: Calendar lookups depend on the stated external Huangli service and may fail when credentials expire, quota is exceeded, or the service is unavailable. <br>
Mitigation: Check token validity and quota status before relying on results, and treat service errors as lookup failures rather than calendar answers. <br>


## Reference(s): <br>
- [Huangli Toolkit Reference](references/reference.md) <br>
- [Huangli homepage](https://nongli.skill.4glz.com) <br>
- [ClawHub skill listing](https://clawhub.ai/leocdchina/zhongguo-nongli-huangli-jixiong) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON command output with concise setup and usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HUANGLI_TOKEN; optional HUANGLI_BASE changes the API endpoint.] <br>

## Skill Version(s): <br>
1.7.11 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
