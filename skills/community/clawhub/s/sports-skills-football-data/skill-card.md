## Description: <br>
Football Data helps agents retrieve football (soccer) standings, schedules, match statistics, xG, transfers, player profiles, and related post-match data across 13 major competitions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonelli182](https://clawhub.ai/user/antonelli182) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill when an agent needs football data for league tables, fixtures, match reports, xG analysis, transfer context, injury notes, or player profiles without API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to install and run the third-party sports-skills Python package. <br>
Mitigation: Install it in an isolated virtual environment and review the package or repository before using it in sensitive environments. <br>
Risk: Some endpoints have limited coverage, including xG only for top-five leagues and player leaders or missing-player data only for Premier League seasons. <br>
Mitigation: Check the coverage references before calling endpoints and use fallback commands when a requested league or data type is unsupported. <br>
Risk: The get_head_to_head command is unavailable and live or real-time scores are outside the intended behavior. <br>
Mitigation: Avoid get_head_to_head, use team schedules to compare past meetings when needed, and present results as post-match or scheduled data rather than live scores. <br>


## Reference(s): <br>
- [Football Data API Reference](artifact/references/api-reference.md) <br>
- [Football Data Commands](artifact/references/commands.md) <br>
- [Football Data Coverage](artifact/references/data-coverage.md) <br>
- [Football Data JSON Schemas](artifact/references/schemas.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/antonelli182/sports-skills-football-data) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, and JSON-shaped data descriptions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should account for league-specific coverage limits and post-match data availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
