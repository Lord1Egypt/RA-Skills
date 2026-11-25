## Description:

Guides developers in building Go services with servicepack, a clone-and-own framework for concurrent services, dependency-aware startup, retries, readiness checks, and graceful shutdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scaffold and extend Go applications with multiple long-running services, including retry, dependency, readiness, CLI, and shutdown behavior. It is suited to new service projects or repositories already structured around servicepack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because setup steps reportedly clone a repository and alter files and Git metadata beyond the declared permissions; some referenced paths could not be resolved, so the scan evidence is incomplete.

Mitigation: Review setup steps and permissions before installing. Check the effects of `make own` and run it only in a fresh clone whose repository history can be replaced.

## Reference(s):

- [Setup and module guide](artifact/references/setup.md)
- [Project homepage](https://github.com/psyb0t/servicepack)
- [ClawHub release page](https://clawhub.ai/psyb0t/skills/servicepack)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with Go examples, inline shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.11.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
