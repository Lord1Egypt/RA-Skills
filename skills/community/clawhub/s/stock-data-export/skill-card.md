## Description: <br>
Exports A-share stock and index daily, weekly, or monthly market data from the Tushare API to CSV, Excel, or JSON for quantitative analysis and backtesting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bingze00000](https://clawhub.ai/user/bingze00000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and quantitative researchers use this skill to prepare A-share stock and index datasets for backtesting, portfolio analysis, and data export workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires a Tushare API token, which could be exposed if pasted into unrelated chats or files. <br>
Mitigation: Use a token with only the access needed for market-data retrieval and keep it in trusted configuration only. <br>
Risk: Installing the Tushare dependency from an untrusted package source could introduce unwanted code. <br>
Mitigation: Install Tushare from an official package source before running export workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with command examples; generated datasets as CSV, Excel, or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Tushare API token and supports daily, weekly, and monthly stock or index exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
