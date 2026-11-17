## Description:

Inspects Linux system memory by periodically scanning all processes, recording memory snapshots, analyzing growth trends, and reporting suspected memory leaks with investigation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhur0ng](https://clawhub.ai/user/zhur0ng)

### License/Terms of Use:

MIT-0

## Use Case:

SREs, developers, and operations engineers use this skill to monitor Linux hosts for process-level memory growth, identify likely leak candidates, and generate a practical investigation report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent all-process command-line capture can expose sensitive arguments or operational details on shared or production hosts.

Mitigation: Run with the least-privileged account that still provides useful visibility, redact or remove command-line capture where needed, and restrict report and snapshot permissions.

Risk: Memory inspection snapshots are written under /var/log/memory-inspector and may be readable by users beyond the intended operators if permissions are left implicit.

Mitigation: Set a restrictive umask such as 077 or create the log and trend directories with explicit 0700 directory and 0600 file permissions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhur0ng/skills/system-memory-inspector)
- [Publisher profile](https://clawhub.ai/user/zhur0ng)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes a local Linux inspection workflow and report output; generated reports may include process names, memory usage, growth rates, and captured command lines.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
