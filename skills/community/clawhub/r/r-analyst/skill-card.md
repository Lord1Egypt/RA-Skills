## Description: <br>
R-style statistical analysis powered by Python 3 for descriptive statistics, ASCII histograms, correlation matrices, missing-value and outlier detection, and CSV structure summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and other external users use this skill to inspect local CSV files from the command line, summarize numeric columns, generate text histograms, calculate Pearson correlations, and check data quality issues before further analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CSV contents may be exposed in terminal output because summary and describe commands can print file names, column names, and sample values. <br>
Mitigation: Run the skill only on CSV files whose contents are acceptable to display in the terminal or logs. <br>
Risk: Large CSV files are loaded into memory for analysis and may be slow or fail in constrained environments. <br>
Mitigation: Use appropriately sized local datasets or sample large files before running the skill. <br>


## Reference(s): <br>
- [R Analyst on ClawHub](https://clawhub.ai/loutai0307-prog/r-analyst) <br>
- [Publisher profile: loutai0307-prog](https://clawhub.ai/user/loutai0307-prog) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Terminal text output with tabular summaries, ASCII histograms, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local CSV files with Bash and Python 3 standard library only; describe can print sample values from the input data.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
