## Description: <br>
QuantConnect automated backtest pipeline - submit local strategies, compile, execute, monitor with early-stop, and download results in one command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tltby12341](https://clawhub.ai/user/tltby12341) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers use this skill to submit local QuantConnect strategy files, run cloud backtests, monitor execution, stop runs that exceed drawdown thresholds, and retrieve statistics and order records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local strategy and auxiliary files to a QuantConnect project, replacing cloud project files such as main.py. <br>
Mitigation: Use a dedicated QuantConnect project, inspect the strategy folder before running, and keep secrets out of adjacent .json, .txt, and .csv files. <br>
Risk: The skill can delete cloud files or early-stopped backtests, and those deleted assets may not be recoverable. <br>
Mitigation: Confirm the target project and drawdown threshold before execution, keep independent backups of project files, and treat early-stop deletion as permanent. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tltby12341/qc-backtest-master) <br>
- [Publisher Profile](https://clawhub.ai/user/tltby12341) <br>
- [QuantConnect REST API v2](https://www.quantconnect.com/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated JSON/CSV result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses QC_USER_ID, QC_API_TOKEN, and QC_PROJECT_ID environment variables; downloaded backtest statistics are JSON and order records are CSV.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
