## Description: <br>
Taiwan professional basketball stats, scores, schedules, player data, live scores, box scores, notifications, and transactions for PLG and TPBL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ichendong](https://clawhub.ai/user/ichendong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Taiwan professional basketball schedules, standings, live scores, box scores, player statistics, transactions, and team notifications for PLG and TPBL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests to PLG, TPBL, and Taiwan Basketball Wiki sources, including pages accessed with a stealth browser-style fetcher. <br>
Mitigation: Review the target domains and scraping behavior before installation, and run the skill only in environments where those outbound requests are acceptable. <br>
Risk: Some wiki and box score behavior relies on a separate CPBL skill virtual environment for the stealth fetcher. <br>
Mitigation: Install and update that dependency chain deliberately, and keep this skill isolated from unrelated credentials or sensitive local data. <br>
Risk: Live scores and scraped sports data can be stale or inaccurate because source sites, cache TTLs, and live-game status handling can change. <br>
Mitigation: Use no-cache or short-cache modes for time-sensitive checks and verify important game status against official league sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ichendong/taiwan-basketball) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Release README](artifact/README.md) <br>
- [Taiwan Basketball Wiki example](https://wikibasketball.dils.tku.edu.tw/wiki/index.php?title=林書豪) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and CLI output that can be returned as JSON or text tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local cache and SQLite storage for sports data; freshness depends on source availability, cache settings, and live-game status handling.] <br>

## Skill Version(s): <br>
1.3.6 (source: frontmatter, README, skill.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
