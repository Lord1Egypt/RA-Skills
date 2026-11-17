## Description:

ZFS filesystem administration, pool management, dataset configuration, snapshots, replication, encryption, performance tuning, and troubleshooting on OpenZFS (Linux and macOS).

This skill is ready for commercial/non-commercial use.

## Publisher:

[mightybyte](https://clawhub.ai/user/mightybyte)

### License/Terms of Use:


## Use Case:

Developers, operators, and storage administrators use this skill to plan, configure, tune, monitor, replicate, and troubleshoot OpenZFS pools and datasets on Linux and macOS systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Replication guidance includes broad passwordless SSH automation and ZFS permissions that can increase operational blast radius.

Mitigation: Use restricted SSH keys, non-interactive accounts, per-replica keys, and only the ZFS permissions required for the specific replication workflow.

Risk: Rollback, destroy, forced receive, and automated pruning commands can cause data loss when applied to the wrong pool, dataset, or snapshot.

Mitigation: Add explicit operator checks, dry runs where supported, target validation, and backup confirmation before destructive ZFS operations.

Risk: File-backed pools are unsuitable for production storage and can hide device errors or weaken reliability guarantees.

Mitigation: Use real block devices for production pools and reserve file-backed pools only for learning, development, CI, or isolated tests.

## Reference(s):

- [ZFS Property Reference](references/properties.md)
- [ZFS Workload Tuning Guide](references/workload-tuning.md)
- [ZFS Replication Guide](references/replication.md)
- [ZFS Troubleshooting Guide](references/troubleshooting.md)
- [ZFS Platform Notes: Linux vs macOS](references/platform-notes.md)
- [OpenZFS on OS X](https://openzfsonosx.org)
- [ZFS on Linux repository package](https://zfsonlinux.org/epel/zfs-release-2-3.el9.noarch.rpm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shell commands that require administrative review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
