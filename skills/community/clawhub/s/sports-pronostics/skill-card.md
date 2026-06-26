## Description: <br>
Analyzes European football matches and betting markets using current football data before producing structured predictions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lysandre2007](https://clawhub.ai/user/lysandre2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch football match data and produce French-language betting analyses for European leagues, including form, head-to-head records, standings, lineups, odds, confidence levels, and recommended wagers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes external RapidAPI football-data calls and can consume the user's RapidAPI key or quota. <br>
Mitigation: Use a dedicated limited-scope RapidAPI key and confirm RAPIDAPI_HOST points to the intended football-data provider before enabling the skill. <br>
Risk: Broad football-related triggers may activate the skill during general football or betting conversations. <br>
Mitigation: Install only where football-related prompts are expected to use live football data, and review outputs before acting on betting recommendations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lysandre2007/sports-pronostics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [French Markdown analysis with match summaries, prediction tables, confidence scores, risks, and a recommended bet.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RapidAPI football data when RAPIDAPI_KEY and RAPIDAPI_HOST are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and sports-pronostics.js) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
