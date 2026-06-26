## Description: <br>
This skill should be used when users need to estimate test effort based on product requirements. It analyzes requirements, breaks down tasks, estimates test effort (case design, first run, retest, regression), and exports results to Excel. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuping2012](https://clawhub.ai/user/xuping2012) <br>

### License/Terms of Use: <br>


## Use Case: <br>
QA engineers, test leads, and product teams use this skill to turn product requirements into test effort estimates for case design, first run, retest, and regression planning. It can also prepare structured estimation rationale for Excel export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled scripts can write output files and one packaging script can archive files from a supplied skill path. <br>
Mitigation: Inspect scripts before use, run them only on explicit project requirement inputs or intended skill directories, and confirm they are not scanning unrelated directories or packaging local files. <br>
Risk: Effort estimates may be inaccurate if requirements are incomplete, ambiguous, or outside the bundled complexity standards. <br>
Mitigation: Review the generated estimates and rationale with QA or project stakeholders before using them for staffing or schedule commitments. <br>


## Reference(s): <br>
- [Complexity Standards](references/complexity-standards.md) <br>
- [Estimation Formulas](references/estimation-formulas.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/xuping2012/test-effort-estimator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with optional Excel workbook output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces person-day estimates and rationale for requirements supplied by the user; Excel export requires the bundled Python script and pandas.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
