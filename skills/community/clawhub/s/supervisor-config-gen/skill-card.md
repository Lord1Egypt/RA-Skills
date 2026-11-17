## Description:

Generates a Supervisor program configuration for the current app directory using its run.sh entrypoint and the invoking user's paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate a Supervisor program config for an application directory containing an executable run.sh, then review the file before deploying it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation downloads a script from the mutable GitHub master branch.

Mitigation: Review the downloaded script or pin it to a trusted commit before installing; avoid a sudo installation unless all users need access.

Risk: Regeneration silently replaces an existing configuration file.

Mitigation: Back up any existing generated config before rerunning the tool.

Risk: The generated config points Supervisor at run.sh without validating it.

Mitigation: Inspect the application's run.sh and the generated configuration before handing it to Supervisor.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/psyb0t/skills/supervisor-config-gen)
- [Setup and field reference](references/setup.md)
- [Project homepage listed in skill metadata](https://github.com/psyb0t/supervisor-config-gen)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands]

**Output Format:** [Supervisor INI-style [program:*] configuration file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes <directory-name>-supervisor.conf in the current directory; replaces an existing file of that name without prompting.]

## Skill Version(s):

1.0.6 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
