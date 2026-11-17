## Description:

Manage and monitor a local 3x3 grid of offline s2-matrix-pod agents with real-time status and local chat within the current directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to inspect local s2-matrix-pod state files, view pod activity status, and leave local terminal chat messages for occupied slots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat-log writes can be redirected outside the advertised data folder by pod metadata or symlinks.

Mitigation: Run the skill only in trusted directories, avoid pod JSON files from untrusted users or tools, and prefer a fixed version that validates pod IDs and blocks symlink or path traversal writes.

Risk: Chat messages are stored in local plaintext logs.

Mitigation: Do not enter sensitive chat content unless local plaintext storage is acceptable and the working directory is protected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-matrix-manager)
- [Space2.world](https://space2.world)

## Skill Output:

**Output Type(s):** [text, files, guidance]

**Output Format:** [Interactive terminal text and local plaintext chat log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local pod JSON files from s2_matrix_data and appends local chat_log_<POD-ID>.txt files.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
