## Description: <br>
Provides US Treasury debt and foreign holding data analysis, including risk signals for Treasury supply and demand conditions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kai157isme-lgtm](https://clawhub.ai/user/kai157isme-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts can use this skill to generate a concise Treasury demand and supply report from public TreasuryDirect data and TIC-based estimates. The output is informational and should be checked against official releases before decisions are made. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Treasury or TIC values may be stale, delayed, estimated, or replaced by fallback values when live requests fail. <br>
Mitigation: Verify figures against official TreasuryDirect and TIC releases and check the output's source dates before relying on the analysis. <br>
Risk: Risk signals could be mistaken for investment advice. <br>
Mitigation: Treat the report as informational financial analysis only and apply independent review before making trading, allocation, or policy decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kai157isme-lgtm/us-treasury-radar) <br>
- [Publisher profile](https://clawhub.ai/user/kai157isme-lgtm) <br>
- [TreasuryDirect debt API](https://www.treasurydirect.gov/NP_WS/debt/current) <br>
- [TreasuryDirect Fed holdings API](https://www.treasurydirect.gov/NP_WS/feddata/current) <br>
- [Treasury International Capital reports](https://home.treasury.gov/data/treasury-international-capital-tic-system) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text report with tabular metrics and risk-signal guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes live TreasuryDirect values when available and clearly notes estimated or delayed TIC-based values.] <br>

## Skill Version(s): <br>
4.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
