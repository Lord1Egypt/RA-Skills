## Description: <br>
雀阴·平衡魄 helps an agent produce Chinese-language load-balancing, task-scheduling, and resource-allocation plans for coordinating multiple tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lt8899789](https://clawhub.ai/user/lt8899789) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to draft scheduling plans, task priorities, parallelization guidance, and resource allocation suggestions when several tasks need coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Activation may route ordinary workload or scheduling mentions to this skill unexpectedly. <br>
Mitigation: Review activation behavior in the host agent and scope use to explicit multi-task scheduling or load-balancing requests. <br>
Risk: The artifact describes resource monitoring and optimization advice but contains no code or trusted metric collection mechanism. <br>
Mitigation: Treat resource usage recommendations as advisory unless a separately trusted system-metrics tool is granted and reviewed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown task scheduling plan with tables and ordered lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language advisory output; no tool execution or metric collection is provided by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
