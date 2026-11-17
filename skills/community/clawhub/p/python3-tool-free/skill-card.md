## Description: <br>
Python 环境工具基础版 helps agents manage Python project environments by checking interpreters, creating virtual environments, installing dependencies, running checks, and diagnosing common setup issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to initialize and troubleshoot Python project environments, including virtual environment setup, dependency installation, basic test or tool checks, and common import or packaging diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary states that network, callback, and API-key instructions are unclear and conflict with privacy claims. <br>
Mitigation: Review the skill before installing and do not provide callback URLs or API keys unless the destination and data handling are understood. <br>
Risk: The skill may recreate virtual environments, install packages, or run project commands. <br>
Mitigation: Confirm commands before execution, prefer project-local virtual environments, and review dependency files before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/python3-tool-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash snippets and JSON-style result examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local Python environment commands, dependency installation steps, and diagnostic guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
