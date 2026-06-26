## Description: <br>
Generate US pre-market outlooks and post-market recaps in a fixed 3-section format using finance news plus structured market-data pages for index snapshots and top gainers/losers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevinksaji](https://clawhub.ai/user/kevinksaji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and employees use this skill to generate concise US market briefings for pre-market outlooks, post-market recaps, or optional scheduled daily delivery. It emphasizes repeatable formatting, source-backed catalysts, and structured market-data sources for index and movers data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled automation may run without the user's intended review or timing if cron jobs are enabled casually. <br>
Mitigation: Review any OpenClaw cron jobs before enabling automation and require explicit approval when schedule tooling or scope is unclear. <br>
Risk: Person-specific early-close wording in the artifact may not fit broad sharing. <br>
Mitigation: Replace person-specific early-close wording with a normal user-approved override before broad distribution. <br>
Risk: Market data or mover pages can be delayed, stale, rate-limited, or incomplete. <br>
Mitigation: Prefer structured movers pages for ranking and percentages, label partial or stale data clearly, and use trusted finance sources for catalyst explanations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kevinksaji/us-market-briefing) <br>
- [Templates](references/templates.md) <br>
- [US Market Holidays 2026](references/us-market-holidays-2026.md) <br>
- [Yahoo Finance Gainers](https://finance.yahoo.com/markets/stocks/gainers/) <br>
- [Yahoo Finance Losers](https://finance.yahoo.com/markets/stocks/losers/) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown briefings with inline source links, plus optional shell commands and configuration guidance for scheduled automation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces fixed three-section pre-market or post-market briefings; scheduled automation can skip full US market-closure days using the bundled 2026 holiday check.] <br>

## Skill Version(s): <br>
1.1.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
