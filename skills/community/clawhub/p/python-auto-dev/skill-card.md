## Description: <br>
Automates Python code generation, testing, debugging, and optimization within a configured conda environment, managing project files under a configured workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[APTjason](https://clawhub.ai/user/APTjason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate Python code from specifications, create tests, run and debug failures, and collect profiling or linting guidance in a Windows conda workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Test and optimization scripts can turn user-controlled paths into Windows shell commands. <br>
Mitigation: Use the skill only in a dedicated Windows conda environment with trusted project files, avoid unusual or untrusted path names, and inspect generated code before running tests or profiling. <br>


## Reference(s): <br>
- [Script Usage Guide](references/script-usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/APTjason/python-auto-dev) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Python files, pytest test files, JSON reports, plain text summaries, and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a configured Windows conda environment and writes generated files, tests, reports, profiles, and debug output under the configured project workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
