## Description: <br>
Real-time monitoring of NVIDIA Jetson GPU status, memory usage, CPU temperature, and frequency information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxd9199](https://clawhub.ai/user/wxd9199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect Jetson hardware telemetry through the local tegrastats utility. It is suited for quick GPU, memory, temperature, and frequency checks on systems where tegrastats is installed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the local tegrastats executable, so missing or unexpected PATH resolution can produce errors or confusing output. <br>
Mitigation: Install only on Jetson systems with the legitimate NVIDIA tegrastats utility available locally and review the command before running it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wxd9199/tegrastats) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and terminal output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local NVIDIA tegrastats utility on compatible Jetson hardware.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
