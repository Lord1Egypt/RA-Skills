## Description: <br>
Generates warehouse analytics charts, product table images, CSV summaries, and report-ready visuals from a local SQLite warehouse database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChinmayaGit](https://clawhub.ai/user/ChinmayaGit) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Warehouse analysts, operators, and developers use this skill to generate chart images, a missing-products CSV, and KPI text summaries from a selected SQLite warehouse database for reports and presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated report files may contain business-sensitive warehouse data. <br>
Mitigation: Write outputs only to an approved local directory and handle PNG, CSV, and text files according to the relevant data policy. <br>
Risk: Existing report files with the same names may be overwritten. <br>
Mitigation: Use a dedicated output folder or review existing files before running the scripts. <br>
Risk: The scripts read the database path supplied with --db. <br>
Mitigation: Point --db only at the intended SQLite warehouse database. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ChinmayaGit/warehouse-reports) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, files, guidance] <br>
**Output Format:** [Markdown instructions with bash command examples; generated report files include PNG, CSV, and text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local SQLite database path and output directory; generated files may overwrite existing names.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
