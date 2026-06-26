## Description: <br>
Calculates Parabolic SAR indicators for A-share stocks, analyzes trend, price position, volume ratio, and momentum, and prints a four-dimensional score with a trading-oriented suggestion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haohanyang92](https://clawhub.ai/user/haohanyang92) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market-analysis users can run the command-line tool to fetch A-share K-line data from Baostock, calculate SAR-based technical indicators, and summarize stock posture across trend, price position, volume, and momentum. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool sends stock symbols and date ranges to Baostock to retrieve market data. <br>
Mitigation: Use it only when sharing those query values with Baostock is acceptable. <br>
Risk: The output includes buy/sell-style technical-analysis suggestions that may be mistaken for financial advice. <br>
Mitigation: Treat recommendations as informational indicators and review them with appropriate financial judgment before acting. <br>
Risk: The command-line script requires external Python dependencies. <br>
Mitigation: Install and run the listed dependencies in an environment where adding baostock and pandas is acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Console text from a Python command-line tool] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports one or more stock symbols, optional start and end dates, quiet output, and SAR acceleration factor settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
