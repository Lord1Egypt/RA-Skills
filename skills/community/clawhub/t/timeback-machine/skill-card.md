## Description:

Provides automated and manual rollback of long-running OpenClaw tasks by saving and restoring state snapshots to handle errors or unexpected issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cortez-1](https://clawhub.ai/user/cortez-1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating OpenClaw workflows use this skill to add task-level rollback prompts and restore saved state after long-running tasks encounter errors or unexpected behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default rollback behavior may not fully preserve non-JSON-serializable state.

Mitigation: Provide explicit onSaveState and onRestoreState handlers for complex state and test rollback before deployment.

Risk: The current release includes Chinese prompt text in user-facing rollback dialogs.

Mitigation: Review and localize prompt text for the deployment audience before release.

Risk: Installation depends on the ClawHub installer used by the environment.

Mitigation: Verify the ClawHub installer source and version before installing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cortez-1/skills/timeback-machine)
- [Publisher profile](https://clawhub.ai/user/cortez-1)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [JavaScript module API with Markdown installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local in-memory snapshots; default save and restore behavior is best suited to JSON-serializable state.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
