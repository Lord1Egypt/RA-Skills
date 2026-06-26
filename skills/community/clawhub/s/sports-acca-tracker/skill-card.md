## Description: <br>
Track accumulator (acca) betting slips across football, basketball, and tennis by parsing slip photo or text, checking live scores every 15 minutes, and reporting bet status with overall acca health and cash-out context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[svenmedina07-ship-it](https://clawhub.ai/user/svenmedina07-ship-it) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users ask an agent to parse accumulator or parlay betting slips from images or text, confirm the extracted legs, and monitor football, basketball, and tennis results until the slip is resolved. The skill is useful for periodic status reports, not for real-time betting advice or guaranteed bookmaker settlement decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may misread a betting slip image or text and begin tracking the wrong legs. <br>
Mitigation: Review and confirm the parsed slip summary before approving tracking. <br>
Risk: Periodic score checks can continue in the background longer or more frequently than intended. <br>
Mitigation: Confirm the cron schedule and repeat count before starting, and stop tracking when background polling is no longer wanted. <br>
Risk: Score data can be unavailable, delayed, or mismatched to team or player names. <br>
Mitigation: Report missing data explicitly, use fallback search only when needed, and avoid guessing scores or final outcomes. <br>
Risk: Version and install metadata are inconsistent across release evidence and artifact files. <br>
Mitigation: Treat the server release version as the publication version and have the publisher correct package/plugin metadata and include the helper script in install metadata. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/svenmedina07-ship-it/sports-acca-tracker) <br>
- [Bet Type Reference](artifact/references/bet-types.md) <br>
- [Data Source Strategy](artifact/references/data-sources.md) <br>
- [TheSportsDB eventsday API](https://www.thesportsdb.com/api/v1/json/3/eventsday.php) <br>
- [ESPN basketball scoreboard API](https://site.api.espn.com/apis/site/v2/sports/basketball/${path}/scoreboard) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status reports, parsed slip summaries, cron configuration, and inline shell command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pipe-delimited score rows from helper commands and explicit uncertainty notes when score data is unavailable.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata and SKILL.md frontmatter; openclaw.plugin.json and package.json list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
