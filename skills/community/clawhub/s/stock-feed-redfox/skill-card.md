## Description: <br>
A股每日新闻 helps agents research A-share market sentiment by querying Xiaohongshu, Douyin, and WeChat Official Accounts, filtering non-stock content, and producing cross-platform summaries with JSON and HTML reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[redfox-data](https://clawhub.ai/user/redfox-data) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, retail investors, financial researchers, and financial content creators use this skill to review A-share social sentiment, compare discussions across platforms, and prepare market research summaries. Outputs are research aids and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stock research terms, watchlists, and market queries may be sent to RedFox and web search providers. <br>
Mitigation: Use only data you are comfortable sharing externally, and avoid nonpublic portfolio or trading-plan details. <br>
Risk: The skill uses local API credentials for RedFox requests. <br>
Mitigation: Use a revocable API key, verify its scope and validity period, and do not hardcode or expose the key in prompts, logs, or output files. <br>
Risk: The skill creates local JSON and HTML reports and its workflow may open generated HTML. <br>
Mitigation: Review generated files before relying on them, and open HTML reports only in a trusted local browser session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/stock-feed-redfox) <br>
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=clawhub) <br>
- [RedFoxHub](https://redfox.hk?source=clawhub) <br>
- [Output rules and report templates](references/output-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with JSON data output and optional interactive HTML report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REDFOX_API_KEY; default query covers 17 A-share keywords across Xiaohongshu, Douyin, and WeChat Official Accounts for the past 7 days.] <br>

## Skill Version(s): <br>
1.0.4 (source: ClawHub release evidence; skill frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
