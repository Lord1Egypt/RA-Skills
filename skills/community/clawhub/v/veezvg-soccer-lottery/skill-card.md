## Description:

Soccer Lottery helps agents fetch football match data, analyze head-to-head history and basic statistics, and produce Markdown pre-match analysis with recommendations and risk notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezvg](https://clawhub.ai/user/veezvg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a football-data API source, retrieve match and head-to-head data, and generate Markdown football match analysis. It should be treated as decision support rather than a complete odds or injury-aware betting model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if users paste credentials into chat while configuring the skill.

Mitigation: Configure keys through a secure secret store, environment variable, or careful local edit instead of sharing them in chat.

Risk: Betting recommendations may be misleading because included behavior is limited and does not fully implement odds or injury-aware prediction.

Mitigation: Treat outputs as limited head-to-head heuristics and verify odds, injuries, and current match context before acting on recommendations.

Risk: Runtime dependencies and live API calls add supply-chain and data-source risk.

Mitigation: Pin and audit dependencies before use, and review live data-source behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veezvg/skills/veezvg-soccer-lottery)
- [veezvg publisher profile](https://clawhub.ai/user/veezvg)
- [Football-Data.org](https://www.football-data.org/)
- [Football-Data matches API endpoint](https://api.football-data.org/v4/matches)
- [Football-Data head-to-head API endpoint](https://api.football-data.org/v4/matches/{match_id}/head2head)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and JSON command output with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured football-data API key for live match data; odds and injury data require additional integration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
