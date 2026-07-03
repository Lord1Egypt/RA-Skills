## Description: <br>
Worldcup 2026 Assistant helps agents answer Chinese-language 2026 FIFA World Cup schedule, team analysis, match prediction, and sports lottery guidance requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z-zihan](https://clawhub.ai/user/z-zihan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to get 2026 FIFA World Cup schedules, team-strength analysis, match predictions, and China Sports Lottery purchase guidance in Feishu-friendly Chinese output. <br>

### Deployment Geography for Use: <br>
Global; lottery-related use should follow local law and official channel availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can provide concrete sports-lottery betting advice that may influence financial decisions. <br>
Mitigation: Treat betting guidance as informational only, avoid relying on it for financial decisions, and verify lottery availability and odds through official channels before acting. <br>
Risk: The skill can write a local ledger of predictions, purchases, stakes, odds, returns, and profit/loss without clear opt-in or privacy controls. <br>
Mitigation: Review or disable ledger behavior before use, avoid storing sensitive personal information, and clear local worldcup-data records when they are no longer needed. <br>
Risk: Schedules, odds, single-match availability, injuries, and scores are time-sensitive and may be incorrect if sources fail or stale data is used. <br>
Mitigation: Cross-check time-sensitive details with official sources and do not act on generated recommendations when the skill cannot verify current data. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/z-zihan/skills/worldcup-2026-assistant) <br>
- [ClawDIS homepage](https://github.com/z-Zihan/awesome-skills) <br>
- [China Sports Lottery football calculator](https://m.sporttery.cn/mjc/jsq/zqspf/) <br>
- [ESPN FIFA World Cup scoreboard API](https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard) <br>
- [Zgzcw football lottery data](https://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Feishu-oriented Markdown-style text with optional local JSON records and Python command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local worldcup-data JSON files, including a betting-ledger.json record of predictions, purchases, stakes, odds, returns, and profit/loss.] <br>

## Skill Version(s): <br>
1.4.0 (source: ClawHub release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
