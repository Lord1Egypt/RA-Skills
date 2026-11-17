## Description:

Guides use of Wander to monitor GitHub Actions without polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erergb](https://clawhub.ai/user/erergb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to monitor GitHub Actions runs after code pushes, get CI completion status, and decide how to inspect or rerun failed workflows without manually refreshing GitHub Actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic background monitoring can run shell scripts after pushes, including repository-selected wrappers.

Mitigation: Start Wander only when CI monitoring is explicitly desired, and inspect any scripts/watch-*.sh wrapper before running it.

Risk: Installation guidance can involve chmodding and executing shell scripts from a Wander checkout.

Mitigation: Pin or verify the Wander repository version before changing permissions or executing its scripts.

## Reference(s):

- [Wander README](https://github.com/ERerGB/wander)
- [Wander Edge Cases](https://github.com/ERerGB/wander/blob/main/EDGE_CASES.md)
- [Wander Coffee Break](https://github.com/ERerGB/wander/blob/main/COFFEE_BREAK.md)
- [Wander Monitor on ClawHub](https://clawhub.ai/erergb/skills/wander-monitor)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend background CI monitoring and wrapper scripts; commands should be reviewed before execution.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
