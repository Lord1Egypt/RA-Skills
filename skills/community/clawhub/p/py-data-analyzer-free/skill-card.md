## Description: <br>
Py Data Analyzer Free helps agents provide Python data cleaning, descriptive statistics, grouped aggregation, and basic visualization guidance for business and research datasets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and data analysts use this skill to turn dataset-analysis requests into a structured flow of data understanding, cleaning advice, Python/pandas code, visualization recommendations, and conclusion templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad execution and file authority for Python data-analysis workflows. <br>
Mitigation: Review generated commands before running them, restrict execution to trusted workspaces, and require explicit user approval before writing files or exporting results. <br>
Risk: The declared input shape includes callback URLs and export-style operations without clear user controls. <br>
Mitigation: Use only approved callback endpoints, avoid sending sensitive datasets to external URLs, and confirm where results will be saved or sent before enabling callbacks. <br>
Risk: Security evidence marks the release suspicious for sensitive-dataset use. <br>
Mitigation: Review the skill before installation in sensitive environments and limit use to non-sensitive or approved datasets until controls are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/py-data-analyzer-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python code blocks and optional JSON-style status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pandas, NumPy, matplotlib, and seaborn snippets; execution and file-writing should remain user-approved.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
