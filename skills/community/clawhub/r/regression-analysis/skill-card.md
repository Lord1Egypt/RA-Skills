## Description: <br>
Analyzes Excel advertising-spend data with OLS regressions and generates a formatted Excel workbook with full-sample and 30-day period results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to run OLS regression analysis on Excel datasets containing advertising spend, short-video counts, play counts, payment totals, and partition dates, then produce a formatted Excel results workbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The documentation and script disagree about aggregation wording and expected sheet/model count. <br>
Mitigation: Confirm the intended aggregation method and expected workbook structure before relying on the generated output. <br>
Risk: The advertised built-in template file is not present in the scanned artifact. <br>
Mitigation: Provide a reviewed Excel template explicitly with the -t option before running the script. <br>
Risk: Regression results may be misleading if the input columns, dates, or sample data do not match the expected format. <br>
Mitigation: Validate outputs against representative sample data before business use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/regression-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated Excel workbook when the script is run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an input Excel workbook and may require an explicit template path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
