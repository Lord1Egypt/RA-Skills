## Description: <br>
Python Support helps OpenClaw agents set up Python environments, manage dependencies, lint and test code, run scripts, debug issues, and follow Python execution best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to guide Python environment checks, script execution, package installation, code quality practices, and debugging workflows for OpenClaw agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Package installation examples and inline dependency installation can install untrusted or unpinned packages if followed without review. <br>
Mitigation: Use a virtual environment or sandbox, install only trusted and preferably pinned packages, and require explicit approval before an agent runs pip or auto-installs dependencies. <br>


## Reference(s): <br>
- [Python Style Guide](references/style-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/python-support) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; no agent tool calls or credentials are required.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
