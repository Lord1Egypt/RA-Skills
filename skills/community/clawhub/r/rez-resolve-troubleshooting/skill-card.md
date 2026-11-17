## Description:

Guides developers through diagnosing Rez environment resolution failures with focused commands for identifying conflicts, missing packages, variant issues, and stale caches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to identify why rez-env, rez-build, or rez-test cannot resolve an environment and confirm the cause before changing package requests or configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic context files and command output may reveal internal package paths or configuration.

Mitigation: Keep .rxt files local and redact internal repository names, paths, and configuration before sharing output.

## Reference(s):

- [Rez Resolve Troubleshooting on ClawHub](https://clawhub.ai/loonghao/skills/rez-resolve-troubleshooting)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend saving a local .rxt diagnostic context.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
