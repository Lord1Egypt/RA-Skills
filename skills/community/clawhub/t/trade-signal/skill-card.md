## Description: <br>
Provides real-time trade signals with Buy/Sell/Hold recommendations, price targets, and supporting stock analysis across US and global markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kslee9572](https://clawhub.ai/user/kslee9572) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to request stock research, technical and fundamental analysis, analyst sentiment, and actionable trade-signal responses for public securities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script can run unintended local code from crafted query text. <br>
Mitigation: Review carefully before installing, use only trusted query text, and update query encoding so user input is passed as data rather than embedded into Python source. <br>
Risk: The skill may process sensitive portfolio details, brokerage information, or trading plans. <br>
Mitigation: Avoid submitting private financial details and treat generated trade signals as research input that needs independent review before any investment decision. <br>


## Reference(s): <br>
- [Trade Singal on ClawHub](https://clawhub.ai/kslee9572/trade-signal) <br>
- [Terminal X](https://terminal-x.ai) <br>
- [Terminal X API](https://terminal-x.ai/api) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [JSON responses containing markdown analysis, tickers, trade signals, price targets, technical indicators, related analysis, and citations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Buy/Sell/Hold recommendations, entry and exit targets, stop loss levels, time horizons, and source citations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
