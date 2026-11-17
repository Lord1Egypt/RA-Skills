## Description:

Ubuntu Inspector helps agents run an Ubuntu system health inspection covering CPU, memory, disk, network, service status, security audit, process, log, and update checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengchiangwork](https://clawhub.ai/user/chengchiangwork)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and system administrators use this skill to inspect Ubuntu server health, troubleshoot system issues, generate host reports, and support routine operations checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The inspection collects host, network, login, process, service, and security details that may be sensitive.

Mitigation: Run it only on systems where this level of inspection is authorized, and review or redact the generated report before sharing it.

Risk: Complete inspection is documented as requiring root access, and the generated report is written under /tmp.

Mitigation: Prefer running without root first; on multi-user or production systems, use a private report directory, mktemp, and 0600 permissions before running it.

## Reference(s):

- [ClawHub Ubuntu Inspector skill page](https://clawhub.ai/chengchiangwork/skills/ubuntu-inspector)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Analysis, Guidance]

**Output Format:** [Markdown with inline bash commands and a plain-text inspection report path]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script writes a timestamped report under /tmp and prints the report path.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
