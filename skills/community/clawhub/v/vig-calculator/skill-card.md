## Description: <br>
Calculate vig (juice/overround/hold) for any sportsbook market, convert odds to no-vig fair lines, and rank books by efficiency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to calculate sportsbook vig, hold percentage, implied probabilities, and no-vig fair lines from American odds. It is useful when comparing market efficiency across books or explaining juice and overround calculations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Betting-related calculations may be mistaken for financial or gambling advice. <br>
Mitigation: Treat outputs as arithmetic support for vig and odds analysis, and review decisions independently before placing bets or making financial commitments. <br>
Risk: The skill may run a local Python command using user-supplied odds. <br>
Mitigation: Review the command before execution and pass only numeric odds values for the documented calculation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/rsquaredsolutions2026/vig-calculator) <br>
- [AgentBets OpenClaw Vig Calculator Skill Tutorial](https://agentbets.ai/guides/openclaw-vig-calculator-skill/) <br>
- [AgentBets OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline Python shell command examples and calculation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 for the documented local odds calculation.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
