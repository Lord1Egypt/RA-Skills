## Description: <br>
中国农历查询 helps agents convert Gregorian dates to Chinese lunar dates and look up lunar year, month, day, zodiac, and ganzhi details through an external Huangli API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leocdchina](https://clawhub.ai/user/leocdchina) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they need focused Gregorian-to-Chinese-lunar date conversion, lunar date fields, zodiac, or ganzhi lookup. For broader almanac suitability, auspiciousness, or date-selection workflows, the skill directs users to a separate unified Huangli skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends queried dates or keywords to an external lunar-calendar API and requires an API token for quota or authentication. <br>
Mitigation: Install only if the API provider is trusted for the queried data, use a dedicated revocable HUANGLI_TOKEN, and avoid exposing the token in chats or logs. <br>
Risk: Changing HUANGLI_BASE can redirect requests and credentials to a different endpoint. <br>
Mitigation: Keep HUANGLI_BASE on the official HTTPS API unless the replacement endpoint is explicitly trusted. <br>
Risk: The toolkit includes broader search and filter behavior beyond direct date conversion. <br>
Mitigation: Use this skill for focused date conversion and route Huangli suitability, auspiciousness, or date-selection tasks to the intended unified Huangli skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leocdchina/zhongguo-nongli-query) <br>
- [中国农历查询 Homepage](https://nongli.skill.4glz.com) <br>
- [Huangli Toolkit Reference](references/reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results from the toolkit] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a dedicated HUANGLI_TOKEN and outbound HTTPS access to the configured Huangli API endpoint.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
