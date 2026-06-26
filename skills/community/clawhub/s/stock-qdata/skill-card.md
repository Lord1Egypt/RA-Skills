## Description: <br>
Downloads and locally stores multi-period A-share historical market data through a configured QMT trading terminal, with natural-language task parsing and an optional localhost monitoring UI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[diudiuhuang](https://clawhub.ai/user/diudiuhuang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading users use this skill to run QMT-backed A-share historical data downloads, either from Chinese natural-language requests or explicit command-line parameters. It supports background execution and a localhost web UI for progress monitoring and task control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect QMT or output-path configuration can launch the wrong local executable or write data to an unexpected directory. <br>
Mitigation: Review config.json before execution and confirm qmt_path and base_path point to the intended QMT installation and data directory. <br>
Risk: Historical market-data downloads may create or overwrite large CSV files. <br>
Mitigation: Use a dedicated data directory, keep backups when needed, and choose bounded days and batch-size settings. <br>
Risk: The localhost web UI controls download jobs on the machine where the skill runs. <br>
Mitigation: Keep the UI bound to 127.0.0.1 and use it only on a trusted machine. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/diudiuhuang/stock-qdata) <br>
- [Publisher profile](https://clawhub.ai/user/diudiuhuang) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with command examples and CSV file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local CSV market-data files under the configured data directory and can launch a localhost monitoring interface.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
