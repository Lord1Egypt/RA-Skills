## Description:

Guides developers in building Go services with the servicepack clone-and-own framework, including service lifecycle, retries, dependencies, readiness, and graceful shutdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to start or extend Go services that run concurrent long-lived workers, with coordinated startup, retry and readiness behavior, service commands, and graceful shutdown. It is intended for projects built from the servicepack template rather than as a library added to an existing application.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan marked the release suspicious because setup instructions were reported to exceed declared shell and filesystem permissions; scan coverage was partial because referenced paths were missing from the bundled artifact.

Mitigation: Review setup instructions and referenced material before use. Inspect the effects of `make own` and run it only in a fresh clone whose repository metadata and files can be replaced.

## Reference(s):

- [Setup and module guide](artifact/references/setup.md)
- [servicepack project homepage](https://github.com/psyb0t/servicepack)
- [ClawHub skill page](https://clawhub.ai/psyb0t/skills/servicepack)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Go code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
