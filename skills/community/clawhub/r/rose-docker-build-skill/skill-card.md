## Description:

Build the ROSE compiler in a Docker container using autotools or CMake.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to set up a Docker-based ROSE compiler build environment, run Autotools or CMake builds, and troubleshoot common ROSE build issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The build instructions use remote upstream sources and third-party downloads, which can introduce supply-chain risk.

Mitigation: Pin the ROSE commit, pin Docker base images by digest, and verify Kitware and EDG artifacts before building.

Risk: Docker bind mounts can expose local workspace files to the build container.

Mitigation: Run the build in a clean workspace with minimal credentials and only the bind mounts needed for the ROSE source tree.

## Reference(s):

- [Rose Docker Build Skill](https://clawhub.ai/chunhualiao/skills/rose-docker-build-skill)
- [Kitware APT Archive Key](https://apt.kitware.com/keys/kitware-archive-latest.asc)
- [Kitware Ubuntu APT Repository](https://apt.kitware.com/ubuntu/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Dockerfile examples, shell commands, configuration options, and troubleshooting tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
