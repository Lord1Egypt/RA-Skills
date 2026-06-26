## Description: <br>
Signalbot analyzes crypto and gold markets with technical indicators and produces structured market reports that an agent can turn into commentary, alerts, or trading-signal summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shanhuhai5739](https://clawhub.ai/user/shanhuhai5739) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, market analysts, and agent users use Signalbot to run command-line analysis for BTC, ETH, SOL, BNB, and XAUUSD across single or multiple timeframes. The skill interprets JSON indicator output into concise market analysis, reports, scheduled updates, and BUY/SELL/HOLD-style informational summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or update an unpinned remote Go package with no confirmation before running market analysis. <br>
Mitigation: Prefer a reviewed or pinned signalbot installation, avoid automatic latest-version installs where possible, and review the binary before allowing agents to execute it. <br>
Risk: The skill may produce BUY/SELL/HOLD market outputs that users could mistake for financial advice. <br>
Mitigation: Present outputs as informational technical analysis and require human judgment before making trading or investment decisions. <br>


## Reference(s): <br>
- [Signalbot ClawHub page](https://clawhub.ai/shanhuhai5739/signalbot) <br>
- [Project homepage from ClawHub metadata](https://github.com/shanhuhai5739/signalbot) <br>
- [OpenClaw usage guide](artifact/OPENCLAW_USAGE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON-derived market-analysis summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill runs or interprets the signalbot CLI, whose stdout is structured JSON. Treat BUY/SELL/HOLD outputs as informational analysis, not financial advice.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
