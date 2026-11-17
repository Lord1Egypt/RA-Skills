## Description:

Guides agents in exposing tools from multiple Rez contexts through suites and packaging resolved environments as relocatable bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and pipeline engineers use this guidance to expose tools from several Rez contexts to artists or deliver bundled environments to render farms, containers, and other machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundling copies packages into a destination directory, and --force can bypass relocatability checks.

Mitigation: Confirm the destination and review whether --force is necessary before running bundle commands.

Risk: Bundled libraries may be patched and might still depend on libraries outside the bundle.

Mitigation: Review library patching and run the bundled context in its destination environment before relying on it.

## Reference(s):

- [rez-suites-bundles on ClawHub](https://clawhub.ai/loonghao/skills/rez-suites-bundles)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with shell and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers Rez 3.4.0; does not itself execute commands or install code.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
