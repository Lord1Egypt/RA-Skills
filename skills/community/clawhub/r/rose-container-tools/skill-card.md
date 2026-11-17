## Description:

Build and run ROSE compiler tools in a Docker-based ROSE environment for source-to-source translators, call graph analyzers, AST processors, and tools that link against librose.so.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chunhualiao](https://clawhub.ai/user/chunhualiao)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create, build, test, and troubleshoot ROSE-based C++ analysis tools inside a containerized ROSE environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells users to run a Docker image that may be unverified while mounting the project workspace with write access.

Mitigation: Use only a trusted or locally built rose-dev image, preferably pinned to a verified digest, and narrow the mounted workspace or use a disposable checkout.

Risk: The documented make clean target deletes the configured build directory.

Mitigation: Review the Makefile build directory setting before running cleanup commands, especially in shared or mounted workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chunhualiao/skills/rose-container-tools)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash, Makefile, and C++ code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker commands, Makefile targets, ROSE C++ examples, AST traversal patterns, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
