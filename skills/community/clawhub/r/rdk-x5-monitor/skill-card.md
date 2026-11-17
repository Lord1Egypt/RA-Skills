## Description:

Rdk X5 Monitor provides read-only RDK X5 hardware status checks for CPU, BPU, memory, disk, temperature, GPU frequency, and network IP information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[katherineedwards2475](https://clawhub.ai/user/katherineedwards2475)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and device operators use this skill to check live RDK X5 CPU, BPU, memory, disk, thermal, GPU, and network status, and to receive bounded troubleshooting guidance for common resource issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting guidance can terminate processes or run a privileged cleanup command, which may exceed strict read-only monitoring expectations.

Mitigation: Require explicit user confirmation and target review before running kill or sudo apt clean; use the normal status commands for read-only monitoring.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with bash command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes RDK X5 Linux status commands and concise troubleshooting notes.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
