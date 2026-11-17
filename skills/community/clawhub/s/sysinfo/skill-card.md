## Description:

Collects operating system, kernel, CPU, memory, disk, network, uptime, login-session, and local-account information, then summarizes it as a system report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyxsz](https://clawhub.ai/user/xyxsz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support staff use this skill to inspect host status, support troubleshooting, and generate concise system summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Default collection of networking, active-session, and local-account information can expose sensitive host details.

Mitigation: Confirm that the requester is authorized to view host details before collection, and omit or redact cat /etc/passwd, who, and detailed network output unless specifically needed.

Risk: A broad system report may reveal more local configuration than is needed for a routine status check.

Mitigation: Collect the smallest useful set of fields for the task and summarize sensitive sections instead of copying full raw command output by default.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xyxsz/skills/sysinfo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown report with optional .md or .txt file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive host, network, login-session, and local-account details.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
