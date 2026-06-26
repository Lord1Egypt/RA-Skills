## Description: <br>
Predict international football match outcomes between national teams, include 2026 World Cup kickoff/result context, answer in the user's language, and keep output as statistical reference only, never betting advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[datatrevor](https://clawhub.ai/user/datatrevor) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to request neutral, multilingual statistical projections for national-team football fixtures, including expected goal difference and World Cup schedule or result context. It is intended for statistical reference only and refuses betting, wagering, bookmaker, stake-sizing, and under-18 use cases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested matchups and API-key traffic are sent to the third-party provider at jiajielitong.com. <br>
Mitigation: Use the skill only when that provider relationship is acceptable, keep API keys private, and review the service's account and quota terms before production use. <br>
Risk: Provider claims about temporary-key quota, repeat-query credit handling, account registration, and retraining are externally controlled. <br>
Mitigation: Verify those claims directly with the provider and treat quota or retraining statements as operational guidance rather than guaranteed behavior. <br>
Risk: Football predictions could be misused as betting advice. <br>
Mitigation: Keep outputs framed as statistical reference only, include the disclaimer, and refuse requests for betting picks, odds, stake sizing, wagering strategy, or under-18 use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/datatrevor/worldcup-analyzer) <br>
- [World Cup Analyzer API Reference](references/api.md) <br>
- [Canonical Team Names](references/team_names.md) <br>
- [2026 World Cup Schedule/Result Reference](references/schedule.md) <br>
- [Extended Compliance Notes](references/compliance.md) <br>
- [SoccerAssess Service](https://www.jiajielitong.com) <br>
- [SoccerAssess API Docs](https://www.jiajielitong.com/docs) <br>
- [SoccerAssess OpenAPI Spec](https://www.jiajielitong.com/openapi.json) <br>
- [2026 FIFA World Cup Schedule](https://en.wikipedia.org/wiki/2026_FIFA_World_Cup) <br>
- [2026 FIFA World Cup Fallback Schedule](https://baike.baidu.com/en/item/2026%20FIFA%20World%20Cup/1497370#9) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown text with structured match analysis, quota notes, schedule or result context, and a mandatory statistical-reference disclaimer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mirrors the user's language where possible and keeps predictions framed as non-betting statistical analysis.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
