## Description: <br>
TradingView platform skill for SurfAgent, covering chart workflows, proof rules, blockers, and when to use the TradingView adapter over generic browser control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[surfagentapp](https://clawhub.ai/user/surfagentapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate TradingView charts through SurfAgent workflows, including chart state inspection, market-data reads, indicator checks, Pine workflows, alerts, drawings, and watchlist updates with explicit proof standards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TradingView account changes such as alerts, drawings, cleanup, and watchlist updates can affect a user's workspace. <br>
Mitigation: Use adapter-level state checks and visual proof where appropriate, and require human confirmation when the TradingView flow still needs it. <br>
Risk: Chart, market-data, indicator, or Pine results can be misleading if the agent relies on page loads or clicks as proof. <br>
Mitigation: Verify results with TradingView adapter state, quote, OHLCV, indicator, study, alert, drawing, watchlist, compile, or screenshot evidence before claiming success. <br>


## Reference(s): <br>
- [SurfAgent homepage](https://surfagent.app) <br>
- [ClawHub skill page](https://clawhub.ai/surfagentapp/surfagent-tradingview) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with tool and workflow names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no executable code is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
