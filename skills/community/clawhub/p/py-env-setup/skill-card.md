## Description: <br>
Host-specific Python execution guidance for OpenClaw on this machine. Prefer $PYTHON over python/python3 in PATH, because OpenClaw exec runs in a non-interactive shell and may not inherit interactive shell initialization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cndaqiang](https://clawhub.ai/user/cndaqiang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Python reliably in OpenClaw environments where non-interactive shells may not expose python, python3, or conda on PATH. It provides command patterns for validating $PYTHON, installing packages, and running scripts or modules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python commands can fail or run against an unintended interpreter when PYTHON is unset, invalid, or points to the wrong executable. <br>
Mitigation: Validate the interpreter with test -x "$PYTHON" and "$PYTHON" --version before running package installation, modules, scripts, or inline Python. <br>
Risk: Package installation commands may modify the selected Python environment. <br>
Mitigation: Review the exact pip command and target interpreter before execution, and use least-privilege environments for automation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cndaqiang/py-env-setup) <br>
- [Artifact-declared Homepage](https://github.com/QAA-Tools/skills) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a valid PYTHON environment variable and recommends failing loudly when it is missing or not executable.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
