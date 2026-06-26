## Description: <br>
Build and run ROSE compiler tools using ROSE installed in a Docker container. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build, test, and troubleshoot ROSE-based source analysis, AST traversal, call graph, and source-to-source translator tools inside a Docker container with the expected compiler toolchain. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Docker workflow bind-mounts the current project directory into the container, which can allow container commands to write to the workspace. <br>
Mitigation: Use a disposable checkout, a narrower mount, or a read-only mount when analysis does not require build outputs. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Makefile, C++, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is oriented around Docker, Makefile-based builds, ROSE headers and libraries, and container troubleshooting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
