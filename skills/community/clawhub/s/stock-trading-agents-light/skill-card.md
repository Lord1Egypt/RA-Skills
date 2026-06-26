## Description: <br>
Trading Agents 简化版 analyzes a stock ticker through seven analyst and research-manager agents to produce a Markdown BUY/SELL/HOLD research report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laigen](https://clawhub.ai/user/laigen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to coordinate stock research agents around one ticker, combining market, fundamental, news, sentiment, bull, bear, and manager perspectives into a decision-support report. The output should be treated as research support, not personalized financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BUY/SELL/HOLD output can be incorrect, stale, or unsuitable for a user's personal financial situation. <br>
Mitigation: Treat the report as research support, review cited sources and assumptions, and do not rely on it as personalized financial advice. <br>
Risk: API tokens or other credentials could be exposed if pasted into prompts or included in generated reports. <br>
Mitigation: Provide TUSHARE_TOKEN and BRAVE_API_KEY through environment variables only, avoid sharing brokerage or portfolio secrets, and redact credential-like strings from generated content. <br>
Risk: The skill performs web and market-data lookups and saves generated stock-analysis reports locally. <br>
Mitigation: Install and run it only when those network calls and local report files are acceptable for the user's environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/laigen/stock-trading-agents-light) <br>
- [Fundamental Analyst Prompt](references/fundamental-analyst.md) <br>
- [Market Analyst Prompt](references/market-analyst.md) <br>
- [News Analyst Prompt](references/news-analyst.md) <br>
- [Social Analyst Prompt](references/social-analyst.md) <br>
- [Bull Researcher Prompt](references/bull-researcher.md) <br>
- [Bear Researcher Prompt](references/bear-researcher.md) <br>
- [Research Manager Prompt](references/research-manager.md) <br>
- [Tushare Pro registration](https://tushare.pro/register) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown report saved to a local file, with text summary or guidance in the agent conversation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a stock ticker and TUSHARE_TOKEN; may use BRAVE_API_KEY or web search; writes reports under ~/.openclaw/workspace/memory/reports/.] <br>

## Skill Version(s): <br>
2.4.2 (source: server release evidence and SKILL.md version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
