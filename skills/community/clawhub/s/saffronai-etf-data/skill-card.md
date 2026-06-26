## Description: <br>
Fetch Indian ETF tracker data (symbol, lastPrice, iNAV, timestamps) from SaffronAI (saffronai.in) and return it as JSON or filtered rows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subscriptionmanager26-png](https://clawhub.ai/user/subscriptionmanager26-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch the full SaffronAI Indian ETF tracker snapshot or filter it by NSE ETF symbols such as NIFTYBEES, GOLDBEES, and SILVERBEES. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs documented python3 commands that invoke curl and contact a public SaffronAI API endpoint. <br>
Mitigation: Review the command before execution and install only if outbound access to the documented endpoint is acceptable. <br>
Risk: ETF prices, iNAV values, timestamps, and blank fields come from an upstream CSV service and may be stale, unavailable, or require downstream type coercion. <br>
Mitigation: Check the returned source and timestamp fields, handle fetch failures, and validate or coerce numeric values before using the data in financial workflows. <br>


## Reference(s): <br>
- [SaffronAI ETF data endpoint](https://www.saffronai.in/api/etf-data) <br>
- [ClawHub skill page](https://clawhub.ai/subscriptionmanager26-png/saffronai-etf-data) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; command output is JSON or CSV] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON output includes ok, source, count, and data fields; CSV output passes through or re-emits endpoint columns.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
