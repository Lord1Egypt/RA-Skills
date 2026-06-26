## Description: <br>
Checks a local development or AI workstation for hardware status, system tools, Python packages, Docker state, network ports, and related Ollama/OpenClaw environment details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tilannlou](https://clawhub.ai/user/Tilannlou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local AI workstation operators use this skill to inspect system readiness, identify missing tools or packages, and generate environment reports. It also provides copyable guidance for managing Ollama, Docker, GPU monitoring, and OpenClaw environment snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included management script can append Ollama variables to ~/.bashrc, creating persistent shell changes. <br>
Mitigation: Inspect the script before use, back up ~/.bashrc, and apply the environment-variable changes manually if persistent modification is not desired. <br>
Risk: Docker and Ollama helper actions can stop, start, or recreate an ollama container and change model directory mounts. <br>
Mitigation: Run Docker actions only on systems where modifying the ollama container is intended, and verify current container state and mount paths before confirming changes. <br>
Risk: Snapshot and memory-indexing guidance may expose local environment details to downstream indexing. <br>
Mitigation: Review any generated environment snapshot for sensitive paths, hostnames, or configuration values before running OpenClaw memory indexing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tilannlou/tilannlou) <br>
- [Publisher profile](https://clawhub.ai/user/Tilannlou) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and Bash code blocks; generated reports can be human-readable text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include file layouts, commands, local report outputs, and configuration snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
