## Description: <br>
QA Agent helps an agent perform quality assurance tasks, including code analysis, test execution, and issue reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Steven-Mr3](https://clawhub.ai/user/Steven-Mr3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run local Python and JavaScript linting and test workflows, then review the resulting QA findings for a codebase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Linting and test commands execute code from the target project. <br>
Mitigation: Run the skill only on trusted projects or inside an isolated workspace before relying on results. <br>
Risk: Extra tool flags, such as fixer options, can modify project files. <br>
Mitigation: Review extra flags before execution and use version control or a disposable copy for file-changing runs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Steven-Mr3/qa-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local lint or test output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs local QA commands against a target path; results depend on project configuration and available Python or JavaScript tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
