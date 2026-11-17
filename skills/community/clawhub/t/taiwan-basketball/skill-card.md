## Description:

Taiwan professional basketball stats, scores, schedules, player data, live scores, box scores, notifications, and transactions for PLG and TPBL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ichendong](https://clawhub.ai/user/ichendong)

### License/Terms of Use:

MIT-0

## Use Case:

Sports analysts, fans, and agents use this skill to retrieve Taiwan professional basketball schedules, scores, standings, player statistics, box scores, reminders, and transaction updates for PLG and TPBL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports an isolation risk because wiki and TPBL box-score scraping depend on Scrapling from a shared CPBL virtual environment.

Mitigation: Vendor or declare Scrapling in this skill's own isolated environment before deployment, and review that dependency path during installation.

Risk: The skill writes a local cache and SQLite database under the user's home directory.

Mitigation: Run it with an appropriate user account and review stored subscriptions, cached sports data, and database permissions before scheduled or shared use.

Risk: Scraping and live-score results can be incomplete or stale when source sites change or when PLG live scores are estimated from schedule windows.

Mitigation: Treat outputs as informational and verify time-sensitive scores or box scores against the official PLG or TPBL source when accuracy matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ichendong/skills/taiwan-basketball)
- [PLG official website](https://pleagueofficial.com)
- [TPBL official API](https://api.tpbl.basketball/api)
- [Taiwan Basketball Wiki](https://wikibasketball.dils.tku.edu.tw/wiki/index.php)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown or JSON/table CLI output, depending on the invoked script and format option]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read live web data, use cached data, and write local SQLite records for subscriptions, transactions, schedules, and results.]

## Skill Version(s):

1.3.6 (source: frontmatter, README, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
