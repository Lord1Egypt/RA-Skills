## Description: <br>
TPVL (Taiwan Professional Volleyball League) stats, scores, schedules, and standings for Taiwan's pro volleyball. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ichendong](https://clawhub.ai/user/ichendong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Taiwan Professional Volleyball League game results, upcoming schedules, team standings, and available player statistics from TPVL public pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on TPVL public website pages and embedded page data, so results may be incomplete or stale if those pages change or become unavailable. <br>
Mitigation: For important use, compare returned results with TPVL official pages and rerun queries when current data matters. <br>
Risk: Some player-stat queries may return empty results while TPVL player-stat pages are unavailable. <br>
Mitigation: Treat empty player-stat output as source data unavailable rather than as a final ranking. <br>
Risk: The skill runs commands that make outbound requests to TPVL public pages. <br>
Mitigation: Review command arguments before execution and run the skill only where that network access is expected. <br>


## Reference(s): <br>
- [ClawHub Tpvl release page](https://clawhub.ai/ichendong/tpvl) <br>
- [TPVL official website](https://tpvl.tw/) <br>
- [TPVL API discovery notes](references/api-discovery.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON or plain text returned by Python command-line scripts, with Markdown usage guidance in the skill instructions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports filters for team, date, year, result limits, output mode, and player-stat category.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
