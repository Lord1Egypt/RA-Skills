## Description:

Use when auditing, updating, or migrating project dependencies, runtimes, package managers, lockfiles, or toolchains. Requires reading authoritative release and migration notes, changing one compatibility boundary at a time, and verifying the resolved dependency graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[escoffier-labs](https://clawhub.ai/user/escoffier-labs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Stocktake to audit dependency and toolchain state, plan bounded updates or migrations, and verify resolved versions and project checks. It can also apply approved changes and produce an audit report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Updates and migrations can change source files and lockfiles and run installation or test commands.

Mitigation: Use a version-controlled checkout, review dependency changes, and provide the separately referenced check skill and lint script before relying on those checks.

## Reference(s):

- [Stocktake on ClawHub](https://clawhub.ai/escoffier-labs/skills/skillet-stocktake)
- [Publisher profile: escoffier-labs](https://clawhub.ai/user/escoffier-labs)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown audit reports, repository changes, and verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope-limited dependency and toolchain changes; disruptive steps require user approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
