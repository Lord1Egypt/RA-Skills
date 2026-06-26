## Description: <br>
Create and manage stock and crypto portfolios with live AISA pricing, portfolio updates, and profit and loss tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage local stock and crypto portfolios, fetch AISA-based price quotes, and review current P&L from the command line. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Price quotes may be incorrect or incomplete and should not be treated as guaranteed market data. <br>
Mitigation: Verify important prices with a trusted market-data source before making financial decisions. <br>
Risk: Portfolio holdings and cost basis are stored in a local plaintext JSON file. <br>
Mitigation: Run only in a trusted workspace and protect or delete the local state file when it is no longer needed. <br>
Risk: Delete, remove, rename, and update commands mutate saved portfolio data. <br>
Mitigation: Review the intended portfolio and ticker before running mutating commands and keep backups when the data matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/stock-portfolio-aisa-api) <br>
- [AISA API endpoint](https://api.aisa.one/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Command-line text output and local JSON portfolio state] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires AISA_API_KEY and python3; stores portfolio holdings and cost basis in a local plaintext JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
