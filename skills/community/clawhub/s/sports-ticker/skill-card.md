## Description: <br>
Live sports alerts for Soccer, NFL, NBA, NHL, MLB, F1 and more. Real-time scoring with FREE ESPN API. Track any team from any major league worldwide. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Sports Ticker to configure team tracking, check live scores, generate match-day alert schedules, and receive concise sports event updates across supported leagues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence rates the release as suspicious because it can create recurring match-alert workflows. <br>
Mitigation: Review generated cron configurations before enabling alerts and keep only the schedules, destinations, and teams the user explicitly wants. <br>
Risk: The security evidence notes optional third-party search calls and possible reuse of a search API key from another skill. <br>
Mitigation: Use explicitly provided BRAVE_SEARCH_API_KEY or SERPER_API_KEY values for this skill, and avoid letting it read another skill's .env credentials. <br>
Risk: The skill can cache sports results locally after ESPN or search lookups. <br>
Mitigation: Review local cache contents and remove stale or unwanted score data when changing tracked teams or sharing the workspace. <br>


## Reference(s): <br>
- [ClawHub Sports Ticker Release Page](https://clawhub.ai/robbyczgw-cla/sports-ticker) <br>
- [OpenClaw](https://openclaw.com) <br>
- [Public ESPN API Documentation](https://github.com/pseudo-r/Public-ESPN-API) <br>
- [ESPN OpenAPI Spec](https://github.com/zuplo/espn-openapi) <br>
- [ESPN API Explorer](https://zudoku.dev/demo?api-url=https://raw.githubusercontent.com/zuplo/espn-openapi/refs/heads/main/espn_openapi_soccer_league_path.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown alert text, command guidance, and JSON cron or configuration objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local configuration, cron configuration JSON, and score-cache files when scripts are run.] <br>

## Skill Version(s): <br>
3.2.0 (source: SKILL.md frontmatter, package.json, CHANGELOG, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
