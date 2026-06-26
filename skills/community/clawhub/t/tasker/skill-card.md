## Description: <br>
Tasker guides agents through task execution, debugging, implementation, analysis, review, planning, workflow execution, and user dissatisfaction handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tealun](https://clawhub.ai/user/tealun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use Tasker to structure coding, troubleshooting, research, writing, review, and planning work with confirmation gates, verification, retries, and escalation handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad workflow-management guidance may lead an agent toward file, command, configuration, or other side effects during user tasks. <br>
Mitigation: Require explicit confirmation before side effects, preserve verification gates, and review proposed actions before execution. <br>
Risk: A tasker_handoff.md file can carry sensitive task context into another skill. <br>
Mitigation: Review handoff content before reuse and avoid including secrets, credentials, or sensitive paths. <br>
Risk: Repeated retries or escalation on difficult tasks can extend execution without resolving the underlying issue. <br>
Mitigation: Use the documented retry caps, retreat limits, and human-in-the-loop escalation points. <br>


## Reference(s): <br>
- [Tasker ClawHub Listing](https://clawhub.ai/tealun/tasker) <br>
- [Tasker v1.2.0 Release Notes](artifact/RELEASE_v1.2.0.md) <br>
- [Optional PUA Style Layer](https://github.com/tanweai/pua) <br>
- [Tasker SkillHub Listing](https://skillhub.cloud.tencent.com/skills/tasker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, concise text, inline code blocks, and optional structured handoff files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a tasker_handoff.md file for approved multi-agent handoff on complex tasks.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter, release evidence, release notes) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
