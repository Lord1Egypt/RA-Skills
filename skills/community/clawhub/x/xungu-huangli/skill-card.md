## Description: <br>
循古黄历 helps agents retrieve Chinese perpetual-calendar and almanac information, including solar terms, lunar dates, auspicious activities, taboos, and day-quality details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnyouker](https://clawhub.ai/user/cnyouker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Chinese almanac questions by querying xungufa.com for dates, lunar calendar details, solar terms, auspicious activities, taboos, and related traditional calendar fields. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a xungufa.com API token and sends date lookup requests to that third-party service. <br>
Mitigation: Keep HUANGLI_API_TOKEN private, store only the needed token in the relevant .env or agent configuration location, and use the service only when those requests are acceptable. <br>
Risk: Almanac responses are third-party informational content and may be inappropriate for security-sensitive or high-impact decisions. <br>
Mitigation: Treat results as informational calendar guidance and review important decisions against appropriate domain-specific sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cnyouker/xungu-huangli) <br>
- [循古排盘](https://xungufa.com) <br>
- [循古黄历 calendar API](https://xungufa.com/huangli/api/calendar) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Configuration guidance] <br>
**Output Format:** [Markdown text with formatted Chinese almanac fields and setup guidance when configuration is needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided HUANGLI_API_TOKEN for xungufa.com API requests.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
