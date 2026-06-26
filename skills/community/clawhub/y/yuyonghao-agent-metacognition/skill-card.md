## Description: <br>
Enables agents to monitor execution, track decisions, reflect on task outcomes, analyze errors, and accumulate lessons for future strategy adjustment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add in-process execution monitoring and reflection to agents, including decision confidence tracking, anomaly reporting, post-run analysis, and lesson accumulation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task context, errors, decisions, and lessons passed into the skill may remain in process memory during execution. <br>
Mitigation: Avoid passing secrets or sensitive data into monitored context or reflection inputs, and clear or limit retained sessions and experiences when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/yuyonghao-agent-metacognition) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Package metadata](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, Configuration] <br>
**Output Format:** [JavaScript objects and event payloads, with Markdown usage examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [In-process state may include task context, errors, decisions, lessons, confidence scores, and recommendations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
