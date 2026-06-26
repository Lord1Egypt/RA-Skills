## Description: <br>
Stock Realtime Brief generates China A-share portfolio, single-stock, multi-stock, smart-picking, price-watch, and trading-discipline briefs from public market data and configured portfolio or watchlist inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelliugh](https://clawhub.ai/user/michaelliugh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare informational China A-share market briefs, compare stocks, monitor watchlist triggers, and apply rule-based trading discipline checks. Outputs are analysis aids and must not be treated as investment, financial, or trading advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local secrets and portfolio files. <br>
Mitigation: Use environment-managed secrets, pass explicit portfolio paths, keep portfolio files outside shared workspaces, and review file access before installation. <br>
Risk: Push and watch modes can send alerts or briefs to a QQ recipient. <br>
Mitigation: Configure or remove the QQ recipient and enable background push/watch behavior only after confirming what data is sent and where. <br>
Risk: Trading outputs may be mistaken for professional financial advice. <br>
Mitigation: Treat all outputs as informational analysis aids, verify data independently, and consult qualified financial professionals before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/michaelliugh/stock-realtime-brief) <br>
- [README_EN.md](README_EN.md) <br>
- [Methodology](docs/methodology.md) <br>
- [Data Freshness Principle](docs/principles/data-freshness.md) <br>
- [Disclaimer](DISCLAIMER.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and CLI text with tables, stock rankings, action levels, alerts, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include realtime market data, portfolio-derived risk summaries, QQ push/watch alerts, and non-advisory trading-discipline guidance.] <br>

## Skill Version(s): <br>
4.2.0 (source: server release, frontmatter, pyproject.toml, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
