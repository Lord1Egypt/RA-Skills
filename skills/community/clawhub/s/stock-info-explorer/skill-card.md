## Description: <br>
A Yahoo Finance (yfinance) powered financial analysis tool that gets quotes, summarizes fundamentals, generates charts with technical indicators, and produces one-shot text and chart reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kys42](https://clawhub.ai/user/kys42) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to fetch Yahoo Finance market data, inspect prices and fundamentals, and generate local text summaries or chart files for ticker analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local Python script that resolves third-party packages and sends ticker queries to Yahoo Finance through yfinance. <br>
Mitigation: Review the script and package dependencies before use, and avoid submitting sensitive or proprietary ticker lists when that would be inappropriate. <br>
Risk: Generated charts are saved under /tmp using ticker-based filenames and may overwrite existing files with the same name. <br>
Mitigation: Move or rename important chart outputs after generation, or adjust the output path before repeated runs. <br>


## Reference(s): <br>
- [Stock Info Explorer on ClawHub](https://clawhub.ai/kys42/stock-info-explorer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; runtime output is terminal text and PNG chart files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated chart paths are printed as CHART_PATH values and chart files are written under /tmp.] <br>

## Skill Version(s): <br>
1.2.10 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
