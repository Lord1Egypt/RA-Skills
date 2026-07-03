## Description: <br>
Provides Chinese lunar calendar services including BaZi calculation, calendar conversion, Chinese almanac lookup, daily fortune, solar-term, and five-elements analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cainingnk](https://clawhub.ai/user/cainingnk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for Chinese lunar calendar conversions, almanac details, BaZi and five-elements analysis, daily fortune, and yearly solar terms. It requires a XiaoBenYang API key and sends query inputs to a third-party service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores a XiaoBenYang API key locally in a .env file. <br>
Mitigation: Treat the .env file as a local secret, avoid shared or untrusted workspaces, and prefer a scoped or disposable key. <br>
Risk: Calendar, birth-date, and birth-time queries are sent to xiaobenyang.com or mcp.xiaobenyang.com. <br>
Mitigation: Do not submit sensitive personal data unless the user accepts the third-party service data flow. <br>
Risk: The security evidence marks the release suspicious because it sends calendar and birth-date queries to a third-party API. <br>
Mitigation: Review the skill and the third-party API behavior before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-lunar-calendar) <br>
- [XiaoBenYang service and API key page](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown or text summaries derived from JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided XBY_APIKEY; selected queries may include dates, birth dates, and birth times sent to the XiaoBenYang API.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
