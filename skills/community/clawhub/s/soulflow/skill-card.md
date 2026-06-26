## Description: <br>
SoulFlow is a general-purpose OpenClaw workflow framework for building custom multi-step workflows across development, operations, research, content, and automation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xtommythomas-dev](https://clawhub.ai/user/0xtommythomas-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use SoulFlow to define and run multi-step OpenClaw workflows for development, operations, research, content, and automation tasks. It can invoke isolated worker sessions that read files, edit code, run shell commands, and report step outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persistent soulflow-worker can run commands, edit files, change OpenClaw configuration, and reuse existing credentials. <br>
Mitigation: Install only when broad local automation is intended, review workflows before execution, avoid production credentials unless necessary, and run sensitive work in a sandbox. <br>
Risk: Workflow execution can modify source files, configuration, worker-agent files, and run-state logs. <br>
Mitigation: Back up OpenClaw configuration and important files before running workflows, then remove the worker agent or .soulflow logs when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/0xtommythomas-dev/soulflow) <br>
- [SoulFlow README](README.md) <br>
- [SoulFlow Skill Definition](SKILL.md) <br>
- [Project Homepage](https://github.com/0xtommythomas-dev/soulflow) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and text guidance with inline shell commands, generated workflow JSON, and workflow execution summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Workflow runs may create or modify files, OpenClaw configuration, worker-agent files, and JSON run-state logs.] <br>

## Skill Version(s): <br>
1.1.2 (source: ClawHub release evidence; artifact package.json and CHANGELOG show 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
