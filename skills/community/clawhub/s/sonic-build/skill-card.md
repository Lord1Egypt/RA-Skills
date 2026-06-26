## Description: <br>
Build SONiC (Software for Open Networking in the Cloud) switch images from sonic-buildimage for VS/ASIC platforms while configuring build parallelism, memory, caching, troubleshooting, submodules, cleanup, and build performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rustiqly](https://clawhub.ai/user/rustiqly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and network engineers use this skill to build and troubleshoot SONiC switch images, prepare host prerequisites, tune build performance, manage clean rebuilds, and test VS platform images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled prerequisites script uses sudo, installs packages and Docker, adds an external apt repository, changes Docker group membership, and clones external source code. <br>
Mitigation: Review scripts/prerequisites.sh before execution and run it only on a dedicated VM or build host intended for SONiC image builds. <br>
Risk: Cleanup guidance such as removing target artifacts and Docker images can delete local build outputs or shared Docker resources. <br>
Mitigation: Confirm the working directory and inspect Docker resources before running cleanup commands. <br>
Risk: The VS platform notes document a default VM password. <br>
Mitigation: Change or isolate any VS VM that uses the documented default password before exposing it beyond a trusted local test environment. <br>


## Reference(s): <br>
- [SONiC Image Build skill instructions](SKILL.md) <br>
- [Prerequisites](references/prerequisites.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [VS Platform Notes](references/vs-platform.md) <br>
- [ClawHub skill page](https://clawhub.ai/rustiqly/sonic-build) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Makefile configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes host setup and build commands for SONiC images; no API keys or MCP tools are required.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
