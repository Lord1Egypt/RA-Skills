## Description: <br>
Checks real-time RDK X5 hardware status, including CPU usage and frequency, BPU utilization, memory, disk, temperature, GPU frequency, and network IP address. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect current RDK X5 device health and resource status without changing system settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting guidance includes commands that can change system state, such as killing a process or clearing the package cache. <br>
Mitigation: Run those commands only after reviewing the target process or cache action and confirming that the user explicitly wants the change. <br>
Risk: Hardware status commands are platform-specific and may fail or return incomplete data outside an RDK X5 environment. <br>
Mitigation: Use the skill only on RDK X5 systems or verify equivalent device paths before relying on the output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/katherineedwards2475/rdk-x5-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill primarily proposes read-only status commands for RDK X5 monitoring.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
