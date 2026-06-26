## Description: <br>
个股舆情/公告/研报催化分析：基于 news 命令做信息收集、噪音过滤、信源分级与影响评分。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ksky521](https://clawhub.ai/user/ksky521) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to evaluate recent A-share stock news, announcements, and research reports for likely positive or negative catalysts. It helps structure evidence collection, noise filtering, source ranking, event scoring, and a concise investment-information report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the external daxiapi-cli npm package and DaxiAPI service. <br>
Mitigation: Install and use the external CLI only when the package and service are trusted. <br>
Risk: API tokens may be exposed if users paste them into chat or logs. <br>
Mitigation: Configure tokens locally and keep credentials out of prompts, reports, and shared logs. <br>
Risk: Generated stock analysis can be incomplete, stale, or unsuitable as investment advice. <br>
Mitigation: Treat outputs as informational, verify against official announcements and current market data, and keep the included disclaimer. <br>


## Reference(s): <br>
- [Report template](assets/report-template.md) <br>
- [ClawHub skill page](https://clawhub.ai/ksky521/xiapi-news-catalyst-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with tables, scores, risk notes, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces informational stock-news catalyst analysis and requires user review before investment decisions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
