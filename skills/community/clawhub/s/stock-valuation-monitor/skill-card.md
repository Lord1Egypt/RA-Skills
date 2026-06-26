## Description: <br>
Stock Valuation Monitor analyzes stocks and ETFs with PE/PB bands, historical percentiles, and valuation-zone guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockszq](https://clawhub.ai/user/rockszq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agents use this skill to query single or multiple stock and ETF symbols, compare valuation levels, and identify opportunity, reasonable, or risk zones. Outputs are research aids and should not be treated as financial advice. <br>

### Deployment Geography for Use: <br>
Global, with market-data coverage focused on Chinese A-shares and ETFs. <br>

## Known Risks and Mitigations: <br>
Risk: Stock and ETF symbols may be sent to external finance data services. <br>
Mitigation: Use the skill only where transmitting queried symbols to those services is acceptable. <br>
Risk: Valuation outputs can be incomplete, stale, or misleading if market data is delayed or historical coverage is limited. <br>
Mitigation: Treat outputs as research aids, verify important results with authoritative sources, and avoid relying on them as financial advice. <br>
Risk: Runtime behavior depends on third-party Python packages and finance data libraries. <br>
Mitigation: Prefer reviewed and locked dependency versions in managed or enterprise environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rockszq/stock-valuation-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, csv, excel, guidance] <br>
**Output Format:** [Text summaries with optional JSON, CSV, or Excel export] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes queried symbols, valuation results, PE/PB metrics, historical percentiles, valuation bands, and system health data when available.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
