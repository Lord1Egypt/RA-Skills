## Description: <br>
Tests Python code by searching for requested functionality, generating test cases, running them, logging results, and proposing fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouhh2017](https://clawhub.ai/user/zhouhh2017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create and run Python tests for specific functions or classes, capture results, and review suggested fixes before applying changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install Python packages while preparing or rerunning tests. <br>
Mitigation: Run it only in a disposable or isolated environment, and avoid installing dependencies into a main Python environment. <br>
Risk: Generated tests may execute project code and produce files in the workspace. <br>
Mitigation: Review generated test scripts and commands before running them, and use a version-controlled workspace. <br>
Risk: Suggested fixes or source-code updates may change real project files. <br>
Mitigation: Require manual diff review before applying changes and keep backups or version-control checkpoints. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with generated Python test code, command output summaries, and JSON log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create test data, logs, and release test files in the skill workspace.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
