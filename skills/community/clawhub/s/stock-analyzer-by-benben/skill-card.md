## Description: <br>
Stock Analyzer helps agents retrieve public stock data, calculate technical and fundamental indicators, produce simple price forecasts, and generate Markdown reports with optional charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopiabenben](https://clawhub.ai/user/utopiabenben) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to analyze publicly traded equities, inspect technical and fundamental signals, create local Markdown reports, and optionally save chart images. Outputs are informational and should not be treated as investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches stock symbols from Yahoo Finance and depends on third-party Python packages. <br>
Mitigation: Install only after reviewing the dependency set and use trusted package sources. <br>
Risk: Reports and charts may be saved locally in the configured output directory. <br>
Mitigation: Choose a non-sensitive output directory and avoid shared locations for generated files. <br>
Risk: Generated analysis and forecasts can be incorrect or misleading for investment decisions. <br>
Mitigation: Treat outputs as informational analysis only and require independent review before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/utopiabenben/stock-analyzer-by-benben) <br>
- [Publisher profile](https://clawhub.ai/user/utopiabenben) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, console text, Python code, shell commands, JSON configuration, and optional PNG charts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches public market data from Yahoo Finance and may save reports or charts to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
