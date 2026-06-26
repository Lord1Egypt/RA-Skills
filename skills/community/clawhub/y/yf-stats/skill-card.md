## Description: <br>
Fetches stock data and generates price charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grayson85](https://clawhub.ai/user/grayson85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to look up public stock ticker data and create simple price-trend charts when a user asks for market snapshots, charts, graphs, or trends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts Yahoo Finance through yfinance for public ticker data. <br>
Mitigation: Use it only in environments where outbound market-data requests are allowed. <br>
Risk: When charting is requested, the skill writes a PNG chart file in the working directory. <br>
Mitigation: Review and clean generated chart files according to the agent workspace retention policy. <br>
Risk: Python dependencies are specified with version ranges rather than pinned versions. <br>
Mitigation: Use pinned dependency versions or a lockfile in stricter environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Plain text from stdout and optional PNG chart file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a ticker symbol and optional --chart flag; chart output is saved as <TICKER>_chart.png.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
