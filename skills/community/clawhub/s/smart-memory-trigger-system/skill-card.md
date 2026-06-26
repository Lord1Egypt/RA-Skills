## Description: <br>
Intelligent system that helps an agent decide when to create or reuse workflow documentation based on task complexity, repetition patterns, and user intent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daddy-Sun](https://clawhub.ai/user/daddy-Sun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to decide when multi-step, repeated, configuration-sensitive, or explicitly requested work should be captured as reusable workflow documentation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can encourage persistent recording and reuse of task history without clear consent, retention, deletion, or sensitive-data limits. <br>
Mitigation: Require user confirmation before saving or reusing workflow notes, and avoid storing secrets or private operational details. <br>
Risk: Workflow notes may become stale or overly broad if they are reused without review. <br>
Mitigation: Review the saved workflow directory periodically and update or remove outdated workflow documents. <br>
Risk: Cross-agent sharing or recurring reviews could expose workflow details beyond the intended scope. <br>
Mitigation: Disable cross-agent sharing and recurring reviews unless they are explicitly needed for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daddy-Sun/smart-memory-trigger-system) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Task Type and Workflow Management System](artifact/memory-trigger-management.md) <br>
- [Memory Trigger Decision Logic](artifact/trigger-logic.md) <br>
- [Intelligent Memory Trigger System - Usage Monitoring](artifact/usage-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration instructions] <br>
**Output Format:** [Markdown guidance with decision rules, workflow templates, and monitoring notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces workflow-documentation decisions and reusable workflow notes; does not contain executable code.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
