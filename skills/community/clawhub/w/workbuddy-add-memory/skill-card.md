## Description: <br>
Adds memory management for WorkBuddy, including automatic knowledge distillation, intelligent retrieval, and task-start memory recall. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zcg007](https://clawhub.ai/user/zcg007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WorkBuddy and OpenClaw users use this skill to retrieve prior work memories, prepare for new tasks, and generate local preparation reports before starting work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags broad local memory-directory access, cached indexes, local report writing, and influence over the agent's workflow. <br>
Mitigation: Review and narrow configured memory sources before use, avoid directories with credentials or private project files, and inspect generated reports before relying on them. <br>
Risk: The artifact includes executable maintenance and installation scripts that can modify local skill files or run shell commands. <br>
Mitigation: Review scripts such as install_and_test.sh and fix_imports.py before execution and run them only in a controlled workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zcg007/workbuddy-add-memory) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Installation and test report](artifact/INSTALLATION_AND_TEST.md) <br>
- [Memory operation workflow](artifact/memory_operation_workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON report data and shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local WorkBuddy preparation reports, indexes, caches, and logs.] <br>

## Skill Version(s): <br>
3.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
