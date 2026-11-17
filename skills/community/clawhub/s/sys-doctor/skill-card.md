## Description:

System Doctor runs Linux-focused system diagnostics for disk usage, memory, CPU load, network interfaces, running services, and system information, with text, JSON, and HTML report output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ericlooi504](https://clawhub.ai/user/ericlooi504)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to check server health, investigate resource or connectivity issues, and generate shareable or machine-readable health reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A narrow --check option can still run broader diagnostics before selecting the requested result.

Mitigation: Change option handling so each --check value invokes only its matching diagnostic before using the skill in monitored, private, or air-gapped environments.

Risk: The network diagnostic performs a google.com DNS lookup even though the skill documentation claims fully offline operation.

Mitigation: Remove the DNS lookup or make it explicit and opt-in before deploying where external network lookups are restricted.

Risk: The macOS fallback depends on psutil without a pinned dependency in the artifact.

Mitigation: Pin and review psutil before enabling the macOS fallback path.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files]

**Output Format:** [Plain text report, JSON object, or generated HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [HTML reports may be written to a timestamped or user-specified file; critical disk usage exits with code 2.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
