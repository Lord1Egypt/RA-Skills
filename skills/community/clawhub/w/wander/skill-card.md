## Description:

Close the loop on long-running remote work: pick the right completion signal per platform (CI, EAS, deploy, releases), run monitoring in the background, notify on finish, and never treat trigger as success. Includes GitHub Actions via the Wander scripts when applicable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erergb](https://clawhub.ai/user/erergb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use Wander to choose and run a suitable monitor for long-running CI, builds, deployments, and releases, then inspect the authoritative terminal result before continuing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following instructions to push to remote repositories or rerun failed workflows can trigger additional remote actions.

Mitigation: Review the target repository and workflow, and confirm the intended push or rerun before executing those actions.

Risk: The security scan was partial and could not verify referenced local paths or watcher scripts.

Mitigation: Review the referenced files and watcher scripts before installing or running the skill.

## Reference(s):

- [Wander README — GitHub Actions scope](https://github.com/ERerGB/wander/blob/main/README.md#v1-scope-github-actions-today)
- [Wander edge cases](https://github.com/ERerGB/wander/blob/main/EDGE_CASES.md)
- [Wander coffee break guide](https://github.com/ERerGB/wander/blob/main/COFFEE_BREAK.md)
- [Wander ClawHub skill page](https://clawhub.ai/erergb/skills/wander)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Platform-specific monitoring guidance and commands; the agent must verify the remote terminal result.]

## Skill Version(s):

1.0.9 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
