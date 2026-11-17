## Description:

Manage Qiniu Cloud Storage (Kodo) files, buckets, CDN operations, private download links, and batch transfers through the qshell CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijianfei](https://clawhub.ai/user/lijianfei)

### License/Terms of Use:


## Use Case:

External users, developers, and storage operators use this skill to turn natural-language Qiniu Kodo requests into qshell prerequisite checks, command guidance, and recovery steps for file, bucket, CDN, and download-link workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Qiniu access keys and secret keys may be exposed through shell history, terminal logs, or broad credential handling.

Mitigation: Use least-privilege Qiniu keys, treat account setup commands as sensitive, and avoid storing or sharing AccessKey and SecretKey values in logs.

Risk: Manual qshell installation can introduce executable supply-chain risk.

Mitigation: Prefer Homebrew when available or verify qshell from the official release source before manual installation.

Risk: Broad cloud-storage prompts may trigger the wrong provider workflow.

Mitigation: Proceed only when Qiniu, qshell, Kodo, or the configured Qiniu provider context is clear.

Risk: Delete operations can cause unrecoverable Kodo data loss when versioning or backups are absent.

Mitigation: Run qshell stat first, show file details, and require explicit confirmation before executing qshell delete.

## Reference(s):

- [qshell Installation Guide](references/install-guide.md)
- [Batch Download Configuration](references/batch-download.md)
- [qshell GitHub Releases](https://github.com/qiniu/qshell/releases)
- [Qiniu Key Management](https://portal.qiniu.com/user/key)
- [ClawHub Skill Page](https://clawhub.ai/lijianfei/skills/qshell-copilot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include qshell command proposals, prerequisite checks, confirmation prompts for deletion, and concise recovery guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
