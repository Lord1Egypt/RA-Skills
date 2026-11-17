## Description:

Build SONiC switch images from sonic-buildimage across VS and ASIC platforms while configuring build resources, caching, troubleshooting, submodules, cleanup, and build performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rustiqly](https://clawhub.ai/user/rustiqly)

### License/Terms of Use:


## Use Case:

Developers and network engineers use this skill to build SONiC switch images from sonic-buildimage, tune build resources, troubleshoot failures, and prepare VS or ASIC platform images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide host-level package, Docker, and group membership changes.

Mitigation: Review setup commands and the bundled prerequisites script before execution, and prefer running them on a dedicated build host or disposable environment.

Risk: Cleanup guidance can delete build artifacts with commands such as removing target contents.

Mitigation: Verify the SONiC repository working directory before running cleanup commands and avoid broad deletion outside the intended build tree.

Risk: Docker cleanup commands can remove local images system-wide.

Mitigation: Inspect Docker disk usage and image lists before pruning or removing images, and run cleanup only when the loss of local images is intended.

Risk: Unpinned package and tool installation can change over time.

Mitigation: Prefer pinned dependencies where practical and review installed package sources before using the build environment for release work.

## Reference(s):

- [Prerequisites](references/prerequisites.md)
- [Troubleshooting](references/troubleshooting.md)
- [VS Platform Notes](references/vs-platform.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with bash and makefile code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include host setup, Docker, build, cleanup, and troubleshooting commands for SONiC build environments.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
