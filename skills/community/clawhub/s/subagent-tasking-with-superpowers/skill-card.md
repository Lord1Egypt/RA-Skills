## Description: <br>
子代理任务拆分 + using-superpowers 技能执行。每次 spawn 子代理前必须遵守的铁律。结合 using-superpowers 和 subagent-tasking 规则。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weilixiong](https://clawhub.ai/user/weilixiong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when to split work into focused subagent tasks, prepare concise task briefs, and validate spawned subagent results before recording follow-up notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task briefs and forum notes may include secrets or sensitive user data when written to temporary task files or shared traces. <br>
Mitigation: Confirm where traces are written, avoid including secrets or sensitive user data, and clean /tmp/tasks regularly or adapt the workflow to a private per-user directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weilixiong/subagent-tasking-with-superpowers) <br>
- [Publisher profile](https://clawhub.ai/user/weilixiong) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown instructions with task brief templates and spawn command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise task decomposition guidance and task brief content for agent workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
