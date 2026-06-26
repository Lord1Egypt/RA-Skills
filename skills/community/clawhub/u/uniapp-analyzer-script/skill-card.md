## Description: <br>
Analyzes uni-app and Vue projects offline to quantify technical debt, detect code issues, and generate project analysis reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[include5943](https://clawhub.ai/user/include5943) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect uni-app and Vue 2/3 projects, assess code quality and technical debt, and produce project documentation for review or follow-up analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local shell scripts against a target project path. <br>
Mitigation: Review the target path before execution, use preview mode when practical, and avoid elevated privileges. <br>
Risk: The script can optionally install the skill-seekers Python dependency with pip when it is missing. <br>
Mitigation: Install skill-seekers manually in a disposable or controlled Python environment before running the analyzer. <br>
Risk: Broad activation phrases may cause the skill to be considered for general project-analysis requests outside its intended scope. <br>
Mitigation: Use it only for uni-app or Vue projects and choose a different workflow for React, Angular, Svelte, Python, Java, native mini-program, or other non-Vue codebases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/include5943/uniapp-analyzer-script) <br>
- [Publisher profile](https://clawhub.ai/user/include5943) <br>
- [API reference](artifact/references/api_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON analysis files, and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated outputs may include SKILL.md, report.md, code_analysis.json, code_quality.json, project_metadata.json, and references for the analyzed project.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
