## Description: <br>
Python数据可视化-免费版 helps agents generate and run Python visualization code with matplotlib, seaborn, and plotly for static and interactive charts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, data analysts, and researchers use this skill to create Python charts from CSV files, dictionaries, NumPy arrays, or pandas DataFrames for analysis, reports, academic figures, and personal projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated visualization code may read local datasets selected by the user and include sensitive values in chart outputs. <br>
Mitigation: Use intended input files only, review generated code before execution, and inspect outputs before sharing them. <br>
Risk: Package installation and local execution can change the Python environment or run code with the agent's current permissions. <br>
Mitigation: Run in a project-specific virtual environment and approve dependency installation commands before execution. <br>
Risk: Chart export commands may overwrite existing PNG, SVG, PDF, or HTML files in the working directory. <br>
Mitigation: Specify safe output filenames and require confirmation before overwriting existing files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/python-dataviz-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with Python and bash code blocks, plus chart files such as PNG, SVG, PDF, or HTML when executed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read selected local data files, install common plotting packages, and write chart outputs in the working directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
