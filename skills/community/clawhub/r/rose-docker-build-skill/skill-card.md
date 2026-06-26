## Description: <br>
Build the ROSE compiler in a Docker container using autotools or CMake. Use when setting up ROSE development environment, building ROSE from source, or troubleshooting ROSE build issues. ROSE requires GCC 7-10 which most modern hosts do not have, so Docker is the recommended approach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chunhualiao](https://clawhub.ai/user/chunhualiao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create a Docker-based ROSE compiler build environment, run Autotools or CMake builds, and troubleshoot common ROSE build issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Docker build installs packages and CMake from external package repositories during image creation. <br>
Mitigation: Review the Dockerfile before use and pin repository keys, package versions, and downloaded binaries when using the skill in sensitive environments. <br>
Risk: ROSE builds can require substantial memory and long build times, especially on first build. <br>
Mitigation: Use the documented lower parallelism, such as make -j4 on 16 GB systems, and adjust based on available resources. <br>


## Reference(s): <br>
- [Kitware APT repository](https://apt.kitware.com/ubuntu/) <br>
- [Kitware archive signing key](https://apt.kitware.com/keys/kitware-archive-latest.asc) <br>
- [ClawHub skill page](https://clawhub.ai/chunhualiao/rose-docker-build-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and Dockerfile code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes Docker build instructions, command sequences, configuration options, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
