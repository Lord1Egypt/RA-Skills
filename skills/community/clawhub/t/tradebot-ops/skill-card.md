## Description: <br>
Tradebot Ops helps an agent monitor trading bot health, detect stale updates, verify LIVE and halted state, restart safely when approved, and summarize status clearly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[motivationationdaily](https://clawhub.ai/user/motivationationdaily) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-bot operators use this skill to diagnose whether a trading bot is running, stale, halted, or safe to restart, then produce a short operational summary and next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to stop, clear, or restart a potentially live trading bot. <br>
Mitigation: Require explicit user approval before any stop, clear, or restart action, and confirm live mode, open positions, and open orders before changes. <br>
Risk: The skill may act on stale or ambiguous bot state when diagnosing frozen charts, heartbeats, signals, or bars. <br>
Mitigation: Limit use to a known bot and environment, verify heartbeat and bar freshness before action, and re-check that timestamps advance after recovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/motivationationdaily/tradebot-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Concise Markdown with health summaries, proposed recovery actions, verification steps, and audit-log text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose stop, clear, or restart actions for a known trading bot; user approval should precede any control action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
