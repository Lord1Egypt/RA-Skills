## Description: <br>
Acts as a meta-orchestrator that routes stock-analysis requests across data, macro/news, backtesting, earnings quality, valuation, portfolio analytics, and risk skills under explicit budget controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to coordinate budget-aware stock research workflows across market data, macro/news context, backtesting, earnings quality, valuation, portfolio analytics, and risk-management skills. It produces transparent recommendation framing with assumptions, confidence, gaps, risk flags, and governance status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate downstream finance skills that may handle API keys, portfolio records, audit logs, or target-state changes. <br>
Mitigation: Review downstream skills before installation or use, especially any skill that handles credentials, portfolio state, audit logs, or governance mutations. <br>
Risk: Recommendation labels such as BUY, ADD, HOLD, TRIM, or EXIT could be mistaken for executable broker instructions. <br>
Mitigation: Treat recommendation labels as analytical outputs only; the artifact states broker execution is disabled and target-state changes require governance routing. <br>
Risk: Financial conclusions may be incomplete when dependent data, macro/news, valuation, or risk-management skills are unavailable or return partial outputs. <br>
Mitigation: Carry missing data forward, cap confidence when critical modules are absent or conflicting, and present assumptions and gaps in the final report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ndtchan/stock-picker-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/ndtchan) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown report with structured sections for fetched data, pipeline choice, assumptions, results, confidence, gaps, risks, next steps, and decision governance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include BUY, ADD, HOLD, TRIM, or EXIT recommendation labels as analytical guidance only; broker execution is disabled.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
