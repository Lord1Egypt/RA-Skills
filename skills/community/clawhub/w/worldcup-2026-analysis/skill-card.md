## Description: <br>
Provides quantitative football and 2026 World Cup analysis using Elo ratings, Dixon-Coles Poisson scoring, Monte Carlo simulation, web-sourced calibration, and optional odds-data integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[luciuszhao0101-dot](https://clawhub.ai/user/luciuszhao0101-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Football analysts, developers, and agent users use this skill to generate match predictions, score probabilities, group or knockout advancement estimates, upset analysis, odds-value checks, and calibration workflows for World Cup and other football matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect match results, injury reports, lineup information, or odds can alter local calibration files and affect future predictions. <br>
Mitigation: Review sourced calibration inputs before running calibration or updating local model data, and skip unavailable facts rather than filling gaps. <br>
Risk: The skill can optionally use odds and football-data API credentials. <br>
Mitigation: Provide only the needed environment variables, keep credentials out of prompts and logs, and rotate keys if exposure is suspected. <br>
Risk: Odds-value analysis may be mistaken for betting advice. <br>
Mitigation: Present outputs as statistical analysis, preserve the no-betting-advice disclaimer, and highlight model uncertainty when model and market probabilities diverge. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/luciuszhao0101-dot/worldcup-2026-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/luciuszhao0101-dot) <br>
- [The Odds API](https://the-odds-api.com) <br>
- [football-data.org](https://www.football-data.org) <br>
- [football-data.org API registration](https://www.football-data.org/client/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with JSON inputs, Python command examples, and structured probability outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite calibration sources, show data cutoff time, and include the skill's stated warning that statistical analysis is not betting advice.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
