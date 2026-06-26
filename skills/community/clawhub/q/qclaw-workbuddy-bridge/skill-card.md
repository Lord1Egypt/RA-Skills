## Description: <br>
Qclaw Workbuddy Bridge connects QClaw's WeChat-facing task intake to WorkBuddy automation through a shared local JSON task queue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuboacean](https://clawhub.ai/user/liuboacean) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to route tasks from QClaw or WeChat into WorkBuddy for execution, then return status and results through the queue workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chat-triggered requests can drive broad WorkBuddy automation through a local task queue. <br>
Mitigation: Install only for intentional QClaw or WeChat-to-WorkBuddy automation, keep the automation easy to pause or disable, and require confirmation before local-file or account-changing actions. <br>
Risk: Queue contents may include sensitive business context, file paths, or task results. <br>
Mitigation: Restrict write access to the queue file, use strict file permissions, and avoid placing secrets or sensitive business data in queued tasks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liuboacean/qclaw-workbuddy-bridge) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Queue manager script](artifact/scripts/qclaw_queue.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown guidance with shell commands and JSON queue records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local queue files under ~/.workbuddy/queue.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
