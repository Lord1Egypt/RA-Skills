## Description: <br>
Manages a stock and crypto watchlist with target and stop alerts using live AISA price checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bibaofeng](https://clawhub.ai/user/bibaofeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain local stock and crypto watchlists, configure target or stop alerts, and run live AISA checks for ticker price and signal status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker symbols and watchlist context are sent to AIsa when live checks run. <br>
Mitigation: Use this skill only for watchlists you are comfortable sharing with AIsa, and avoid sensitive or proprietary lists unless the publisher documents destination, retention, and privacy handling. <br>
Risk: The skill requires an AISA_API_KEY to call the live price-check API. <br>
Mitigation: Provide the key through the runtime environment and avoid committing it to shared files or watchlist state. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bibaofeng/stock-watchlist-aisa) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Command-line text with local JSON watchlist state and optional alert summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY; watchlist state is stored locally unless CLAWDBOT_STATE_DIR is set.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
