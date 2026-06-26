## Description: <br>
Check daily if given stocks hit the 4% volatility threshold condor signal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinntrance](https://clawhub.ai/user/jinntrance) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run a local options signal script for selected stock tickers and receive an informational condor or strangle trading signal with suggested put and call strike thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill produces options strike recommendations that can be mistaken for financial advice. <br>
Mitigation: Present outputs as informational trading analysis and require independent validation before any capital is committed. <br>
Risk: Short options, iron condors, and strangles can create substantial losses if the market moves beyond the modeled range. <br>
Mitigation: Use defined-risk structures such as protective wings, limit allocation, and verify suitability against the user's brokerage and risk controls. <br>
Risk: The script depends on current public market data and a locally trained model, so stale data or model error can produce misleading signals. <br>
Mitigation: Confirm the data timestamp, rerun the script close to decision time, and compare the result with independent market and options-chain analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinntrance/unbeatable-condor-strategy) <br>
- [jinntrance publisher profile](https://clawhub.ai/user/jinntrance) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown summary with shell command output and trading-risk guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are informational market analysis only and should be independently validated before risking capital.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
