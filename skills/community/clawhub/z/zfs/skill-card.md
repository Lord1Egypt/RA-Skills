## Description: <br>
ZFS helps agents provide OpenZFS administration guidance for pool management, dataset configuration, snapshots, replication, encryption, performance tuning, health checks, and troubleshooting on Linux and macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mightybyte](https://clawhub.ai/user/mightybyte) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, storage administrators, and infrastructure engineers use this skill to plan and operate OpenZFS pools and datasets, including snapshots, replication, encryption, tuning, health checks, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Storage commands can modify or destroy real data when pool names, dataset names, disk IDs, snapshots, or force flags are wrong. <br>
Mitigation: Review every proposed command before execution and verify disk IDs, pool names, dataset names, snapshots, and current backups. <br>
Risk: Rollback, destroy, forced receive, scheduled automation, passphrase-less SSH keys, and NFS no_root_squash examples carry elevated operational risk. <br>
Mitigation: Use least-privilege access, confirm intent with dry runs or test systems where available, and avoid applying destructive examples without an operator-approved recovery plan. <br>
Risk: File-backed pools are unsuitable for production storage. <br>
Mitigation: Use real block devices with stable identifiers for production and reserve file-backed pools for learning or CI testing only. <br>


## Reference(s): <br>
- [ZFS Property Reference](references/properties.md) <br>
- [ZFS Workload Tuning Guide](references/workload-tuning.md) <br>
- [ZFS Replication Guide](references/replication.md) <br>
- [ZFS Troubleshooting Guide](references/troubleshooting.md) <br>
- [ZFS Platform Notes: Linux vs macOS](references/platform-notes.md) <br>
- [OpenZFS on OS X](https://openzfsonosx.org) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend commands that affect real storage; users should review names, devices, snapshots, and backups before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
