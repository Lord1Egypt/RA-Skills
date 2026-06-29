## Description: <br>
Stock Realtime Brief helps agents produce China A-share market analysis, portfolio briefings, single-stock deep dives, multi-stock comparisons, valuation checks, alerts, and backtest summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelliugh](https://clawhub.ai/user/michaelliugh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate rule-based China A-share analysis from stock codes, watchlists, or portfolio files. It is intended to support market review, risk discipline, and briefing workflows, not to replace professional financial judgment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Portfolio or alert information may be sent through push or watch modes, including hard-coded QQ recipient behavior noted by the security evidence. <br>
Mitigation: Review or disable push and watch modes before deployment, and remove or verify any hard-coded recipient. <br>
Risk: The security evidence notes hard-coded local portfolio and TinyFish credential paths. <br>
Mitigation: Replace hard-coded paths with approved per-user configuration and store credentials in managed secrets. <br>
Risk: Third-party market and search lookups can expose query or portfolio context. <br>
Mitigation: Use the skill only with approved data providers and avoid submitting sensitive portfolio details unless the deployment permits it. <br>
Risk: Stock outputs may be mistaken for investment advice. <br>
Mitigation: Treat outputs as analysis only and require qualified human review before any trading decision. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/michaelliugh/skills/stock-realtime-brief) <br>
- [README_EN.md](artifact/README_EN.md) <br>
- [Methodology](artifact/docs/methodology.md) <br>
- [Data Freshness Principle](artifact/docs/principles/data-freshness.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown briefings with tables, ranked findings, trigger-based action guidance, and occasional shell commands or JSON snippets for setup.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focused on China A-share portfolio, single-stock, multi-stock, selection, alerting, valuation, financial parsing, and backtesting workflows.] <br>

## Skill Version(s): <br>
5.0.0 (source: frontmatter, pyproject.toml, changelog, server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
