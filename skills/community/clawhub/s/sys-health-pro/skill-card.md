## Description:

Sys Health Pro is a local system health monitor for checking CPU, memory, disk, and network usage and reporting anomalies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxliuyu](https://clawhub.ai/user/sxliuyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and technical users can use this skill to run local status checks, generate system health reports, and monitor host resource thresholds on servers, studio machines, or personal computers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports include host resource details and top process names.

Mitigation: Use in environments where local system and process information is appropriate to display or share.

Risk: The psutil dependency is not pinned in the artifact metadata.

Mitigation: Pin and review the psutil package version before sensitive or production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sxliuyu/skills/sys-health-pro)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local system status, report, and watch-mode guidance based on host resource metrics.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
