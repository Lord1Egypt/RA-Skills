## Description: <br>
Retrieves real-time stock quote data such as price, change, volume, turnover, and market details through Sina Finance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asterisk622](https://clawhub.ai/user/asterisk622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to query stock symbols and return concise market snapshots for quick informational lookup. It is suitable for retrieving current quote fields for supported A-share and Hong Kong symbols, with documentation also describing US market examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market data from an external quote endpoint may be delayed, unavailable, or parsed incorrectly. <br>
Mitigation: Treat the output as informational and verify important financial or trading decisions against an authoritative market data source. <br>
Risk: The documentation and implementation differ on US stock support. <br>
Mitigation: Validate market support in the installed version before relying on US symbols; the included command implementation accepts six-digit A-share symbols and five-digit Hong Kong symbols. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asterisk622/xiaoding-stock) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns quote fields including current price, price change, open, high, low, volume, amount, turnover, and market when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
