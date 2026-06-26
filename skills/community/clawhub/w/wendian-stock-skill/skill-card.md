## Description: <br>
Wendian Stock helps agents use Wendian Starmap market-data endpoints for real-time quotes, K-line/OHLC bars, heatmaps, sector rotation analytics, concept linking, trading calendars, and stock reference data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wendian-ai](https://clawhub.ai/user/wendian-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to configure authenticated Wendian Starmap API calls and retrieve market intelligence for dashboards, screening, charting, heatmap visualization, and quantitative research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Wendian API key and sends it to Wendian HTTPS endpoints. <br>
Mitigation: Use a dedicated limited API key, keep it in the WENDIAN_MARKETHOT_APIKEY environment variable, and avoid pasting real keys into prompts, examples, or logs. <br>
Risk: The skill depends on a third-party market-data service and account terms. <br>
Mitigation: Verify the Wendian hostname and account terms before use, and monitor requests made to markethot.wendian.net. <br>
Risk: Market analytics and heatmap outputs could be mistaken for financial advice. <br>
Mitigation: Treat outputs as data tooling and require human review before making investment or trading decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wendian-ai/wendian-stock-skill) <br>
- [Wendian Starmap](https://markethot.wendian.net) <br>
- [Wendian Starmap Skill API Base](https://markethot.wendian.net/app-api/member/skill-data) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with API endpoint descriptions, parameter tables, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Wendian Starmap API key in WENDIAN_MARKETHOT_APIKEY; API responses depend on the Wendian service and requested market endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
