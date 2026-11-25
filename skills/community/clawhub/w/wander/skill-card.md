## Description:

Close the loop on long-running remote work: pick the right completion signal per platform (CI, EAS, deploy, releases), run monitoring in the background, notify on finish, and never treat trigger as success. Includes GitHub Actions via the Wander scripts when applicable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erergb](https://clawhub.ai/user/erergb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Wander to monitor long-running CI, build, deploy, and release jobs until the platform reports an authoritative terminal result, including GitHub Actions workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this release suspicious with medium confidence because its GitHub Actions guide includes repository updates and rerunning failed jobs beyond the stated monitoring and notification purpose; the watcher implementation was not supplied for verification.

Mitigation: The scanner recommends not installing. If considering it anyway, review the guide's repository push and rerun instructions and confirm affected workflows' side effects and costs are acceptable.

## Reference(s):

- [GitHub Actions adapter guide](references/github-actions.md)
- [Wander repository](https://github.com/ERerGB/wander)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.11 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
