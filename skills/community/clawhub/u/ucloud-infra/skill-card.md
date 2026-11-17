## Description:

UCloud Cloud Management - Complete Version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianjunye](https://clawhub.ai/user/qianjunye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to inspect and manage UCloud infrastructure through the UCloud CLI, including compute, database, networking, storage, firewall, image, project, and region resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses powerful UCloud credentials that can authorize infrastructure changes.

Mitigation: Use least-privilege, revocable UCloud credentials and rotate or revoke them when the skill is no longer needed.

Risk: Supported operations include destructive or disruptive cloud actions such as delete, resize, stop, restart, and firewall changes.

Mitigation: Review planned commands before execution, require explicit confirmation for destructive actions, and create backups before important changes.

Risk: Local operation logs and agent transcripts may contain sensitive resource parameters or command results.

Mitigation: Treat logs and transcripts as sensitive, restrict access to them, and redact secrets before sharing.

Risk: Command execution can be unsafe when arguments are built from untrusted input.

Mitigation: Avoid running the skill with untrusted input and prefer a fixed version that uses argument-array execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qianjunye/skills/ucloud-infra)
- [UCloud CLI installation documentation](https://github.com/UCloudDoc-Team/cli/blob/master/intro.md)
- [UCloud console](https://console.ucloud.cn/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, JSON, Text]

**Output Format:** [Markdown guidance with bash examples and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires UCloud credential environment variables; create and delete operations may write local JSONL operation logs.]

## Skill Version(s):

1.0.0 (source: server release metadata and script constant)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
