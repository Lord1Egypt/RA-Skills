## Description: <br>
查询沪深主板 A 股股票列表（排除创业板、科创板）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxyu94](https://clawhub.ai/user/dxyu94) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to fetch public Shanghai and Shenzhen main-board A-share listings, excluding ChiNext and STAR Market stocks, and export the results for local analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes a public Baostock network request when executed. <br>
Mitigation: Run it only in environments where outbound access to Baostock is acceptable. <br>
Risk: The script writes JSON and CSV files locally beside the Python file. <br>
Mitigation: Review the output path and run from a controlled working directory when file writes matter. <br>
Risk: Unpinned baostock and pandas dependency versions can reduce reproducibility in shared or production environments. <br>
Mitigation: Pin dependency versions before operational use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxyu94/query-main-board-stocks) <br>
- [Publisher profile](https://clawhub.ai/user/dxyu94) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, CSV] <br>
**Output Format:** [Markdown usage guidance plus terminal text; runtime writes JSON and CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 with baostock and pandas; the script writes main_board_stocks.json and main_board_stocks.csv beside the Python file.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
