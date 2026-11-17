## Description:

Workflow Engine provides a DAG-based workflow execution engine for defining and running sequential, conditional, and parallel task flows with checkpoint persistence and lifecycle events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to define, execute, test, and resume DAG-based workflows with task, condition, and parallel execution nodes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checkpoint persistence can write workflow context and node results to local JSON files.

Mitigation: Disable checkpointing or isolate the checkpoint directory when workflows may contain secrets, personal data, approvals, payments, deployments, deletion, or other side effects.

Risk: Resume and checkpoint loading depend on caller-provided execution IDs.

Mitigation: Validate execution IDs and avoid exposing checkpoint access directly to untrusted users.

Risk: The conditional workflow helper has a branch execution bug noted by security guidance.

Mitigation: Do not rely on conditional branching for security-sensitive decisions until the branch behavior is fixed and retested.

## Reference(s):

- [Workflow Engine documentation](artifact/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/yuyonghao-123/skills/yuyonghao-workflow-engine)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write JSON checkpoint files when checkpointing is enabled.]

## Skill Version(s):

0.1.0 (source: server release metadata, artifact package.json, and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
