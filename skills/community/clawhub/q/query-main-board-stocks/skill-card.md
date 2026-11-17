## Description:

查询沪深主板 A 股股票列表（排除创业板、科创板）

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxyu94](https://clawhub.ai/user/dxyu94)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to query Shanghai and Shenzhen main-board A-share listings, excluding ChiNext and STAR Market stocks, and export the result for downstream review or processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package.json lists Python packages as npm dependencies, which can lead users to install the wrong dependency set.

Mitigation: Install in an isolated Python environment and pin baostock and pandas in a Python-native requirements file before use.

Risk: The skill contacts Baostock and writes JSON/CSV outputs into its own directory.

Mitigation: Run it only where outbound access to Baostock and local output file creation are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxyu94/skills/query-main-board-stocks)
- [Publisher profile](https://clawhub.ai/user/dxyu94)

## Skill Output:

**Output Type(s):** [text, shell commands, code, configuration, files]

**Output Format:** [Console text plus generated JSON and CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates main_board_stocks.json and main_board_stocks.csv in the skill directory after contacting Baostock.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
