## Description: <br>
TaskFlow 3.0 helps an agent read PROJECT.yaml project definitions, schedule enabled projects, execute ordered workflow steps, and record execution history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manwjh](https://clawhub.ai/user/manwjh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use TaskFlow to coordinate OpenClaw project workflows, check execution constraints, run scheduled project tasks, and review or edit project configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TaskFlow can read local OpenClaw workspace and intel files, persist logs or history, and edit project configuration. <br>
Mitigation: Review each PROJECT.yaml before execution, keep secrets out of referenced workspace folders, and restrict projects to known directories. <br>
Risk: Configured workflows may publish externally without clear approval controls. <br>
Mitigation: Require manual approval before browser-based publication or other external delivery steps. <br>


## Reference(s): <br>
- [TaskFlow 3.0 ClawHub release](https://clawhub.ai/manwjh/taskflow3) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with bash, YAML, and JSON examples; CLI scripts emit plain text and may write project configuration or history files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and PyYAML; operates on OpenClaw workspace project files and execution history.] <br>

## Skill Version(s): <br>
3.0.0 (source: evidence.release.version, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
