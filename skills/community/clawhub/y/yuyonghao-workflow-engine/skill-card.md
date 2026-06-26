## Description: <br>
DAG-based workflow engine supporting sequential, conditional, and parallel task execution with checkpoint persistence and event-driven lifecycle events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to define and run JavaScript DAG workflows with sequential, conditional, and parallel tasks. It supports checkpoint-based resume behavior and event hooks for workflow and node lifecycle tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow task functions can execute arbitrary logic supplied by the user. <br>
Mitigation: Review task functions before execution and run untrusted workflows only in controlled environments. <br>
Risk: Checkpoint files may persist workflow context, node results, or other sensitive runtime data. <br>
Mitigation: Keep checkpoint directories local and protected, and avoid placing secrets in workflow context unless persistence is acceptable. <br>


## Reference(s): <br>
- [Workflow Engine ClawHub release](https://clawhub.ai/yuyonghao-123/yuyonghao-workflow-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce workflow definitions, execution snippets, checkpoint configuration, and operational guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
