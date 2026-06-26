## Description: <br>
Reviews local git diffs before commit, grouping changed files and reporting potential bugs, security risks, and optimization suggestions in a structured Markdown report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wed840313](https://clawhub.ai/user/wed840313) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill before committing code to inspect staged, unstaged, and new files for defects, security risks, regression risk, and practical cleanup opportunities. It helps decide whether changes are ready to commit or need fixes first. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local diffs or full new files that contain secrets. <br>
Mitigation: Specify the repository or files to review and avoid including secret-bearing changes unless you intend the agent to inspect them. <br>
Risk: Pre-commit review findings are advisory and may miss issues or suggest changes that do not fit the project. <br>
Mitigation: Review the reported findings, run the project tests, and apply team security checks before committing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown review report with issue levels, file locations, summary counts, and commit guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request repository or file scope when the target is ambiguous.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
