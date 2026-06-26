## Description: <br>
Query a Yahoo Fantasy Baseball league to view rosters, standings, matchups, free agents, draft results, transactions, injuries, and read-only daily roster optimization suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khaney64](https://clawhub.ai/user/khaney64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Yahoo Fantasy Baseball users use this skill to inspect league data and get read-only lineup, bench, pitcher rotation, and injured-list suggestions before making their own roster decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores Yahoo OAuth material locally. <br>
Mitigation: Install and run it only on a trusted machine, keep credential files private, and revoke the Yahoo app or token and remove ~/.openclaw/credentials/yahoo-fantasy when access is no longer needed. <br>
Risk: The setup flow installs a pinned Python dependency. <br>
Mitigation: Review yahoo_fantasy_api==2.12.2 before running --setup and avoid setup on untrusted systems. <br>
Risk: Roster suggestions depend on current Yahoo and MLB data and may become stale near game lock times. <br>
Mitigation: Review recommendations against current league and lineup information before making roster changes in Yahoo. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/khaney64/yahoo-fantasy-baseball) <br>
- [Publisher Profile](https://clawhub.ai/user/khaney64) <br>
- [Yahoo Developer Apps](https://developer.yahoo.com/apps/) <br>
- [yahoo-fantasy-api](https://github.com/spilchen/yahoo_fantasy_api) <br>
- [MLB Stats API](https://statsapi.mlb.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text, JSON, or Discord-formatted markdown depending on command flags.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only outputs may include roster tables, standings, matchup summaries, player lists, transaction reports, injury reports, and lineup optimization suggestions.] <br>

## Skill Version(s): <br>
0.1.27 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
