## Description: <br>
Manage Volcengine ECS instances and related resources for instance inventory, lifecycle operations, troubleshooting, and automation templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cinience](https://clawhub.ai/user/cinience) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect Volcengine ECS inventory and prepare or execute scoped lifecycle operations such as start, stop, and reboot with explicit account, region, and instance targeting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud lifecycle operations can affect running Volcengine ECS instances if the wrong account, region, or targets are used. <br>
Mitigation: Confirm account and region, query inventory first, and require exact instance IDs before start, stop, reboot, or batch operations. <br>
Risk: Over-privileged cloud credentials could allow broader infrastructure changes than intended. <br>
Mitigation: Use least-privileged Volcengine credentials scoped to the needed ECS actions and regions. <br>


## Reference(s): <br>
- [Source Notes](references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with command examples and action summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include account, region, instance IDs, requested action, and pre/post status when lifecycle operations are performed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
