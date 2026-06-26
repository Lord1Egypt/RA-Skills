## Description: <br>
Sudo Gold helps agents retrieve Tavily-backed gold market information and produce concise reports covering price, technical indicators, fundamentals, and risk caveats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FMouseBoy](https://clawhub.ai/user/FMouseBoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to gather current gold-market search results and summarize price action, technical signals, fundamentals, and investment-risk reminders. It is intended as market-analysis support, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Gold-related search terms are sent to Tavily under the user's API key. <br>
Mitigation: Use a monitored Tavily key and avoid entering private holdings, account details, or other sensitive financial information. <br>
Risk: The skill produces market-analysis summaries that could be mistaken for personalized financial advice. <br>
Mitigation: Treat outputs as informational support only and apply independent financial review before making investment decisions. <br>
Risk: The skill includes a JD Finance promotional link unrelated to the core gold-analysis workflow. <br>
Mitigation: Treat the link as optional advertising and review it separately before following it. <br>


## Reference(s): <br>
- [Sudo Gold ClawHub page](https://clawhub.ai/FMouseBoy/sudo-gold-v2) <br>
- [Publisher profile](https://clawhub.ai/user/FMouseBoy) <br>
- [Gold technical indicators reference](references/technical-indicators.md) <br>
- [Tavily Search API endpoint](https://api.tavily.com/search) <br>
- [JD Finance promotional link](https://eco.jr.jd.com/common-growth-page/index.html?channel=clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style analysis report with sourced search summaries and risk reminders] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and TAVILY_API_KEY; sends gold-related search terms to Tavily.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
