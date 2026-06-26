## Description: <br>
Python Use Agent is a compatibility skill for task-driven Python execution that forwards users toward the unified code entry point. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to request Python-based task execution, direct Python execution, or code review through a backward-compatible entry point. The current documentation recommends using the unified code python workflow for future tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python execution may run with local workspace permissions even when sandbox settings appear enabled. <br>
Mitigation: Run the skill only in a disposable workspace or OS-level container and avoid exposing secrets or sensitive files. <br>
Risk: Generated or supplied Python code may perform unintended file, network, or system actions. <br>
Mitigation: Review code before execution and treat dangerous-function blocking and sandbox indicators as advisory rather than enforced controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jirboy/python-use-agent) <br>
- [AiPy App Homepage](https://www.aipy.app/) <br>
- [Package Repository](https://github.com/knownsec/aipyapp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON result objects, console text, and generated Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write logs, temporary Python files, and result files under ./python-use-results when execution paths are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
