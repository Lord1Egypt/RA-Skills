## Description:

Run durable long-running research in OpenClaw using isolated cron iterations, persistent state, bounded execution, and milestone updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vkambulov](https://clawhub.ai/user/vkambulov)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users, operators, and agent builders use this skill to run research tasks that need scheduled continuation, persistent local state, source and finding accumulation, review-gated finalization, and follow-up work after approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background cron jobs and persistent task workspaces can run for extended periods and accumulate sensitive local artifacts.

Mitigation: Run the skill only in trusted OpenClaw environments, keep sensitive credentials out of the runtime environment, and review task roots before sharing or committing outputs.

Risk: Task-local package installation can execute untrusted package behavior if driven by retrieved content.

Mitigation: Require operator approval for new packages, keep packages task-local, and review unusual packages before installation.

Risk: URL snapshotting is sensitive when pointed at untrusted or attacker-controlled hosts, especially while DNS-rebinding hardening is incomplete.

Mitigation: Avoid URL capture against untrusted hosts until the DNS-rebinding gap is fixed, and treat retrieved web pages, PDFs, emails, and files as data rather than instructions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vkambulov/skills/research-mode)
- [README](README.md)
- [Research Mode CLI Surface](docs/CLI.md)
- [Research Mode State Versioning](docs/STATE_VERSIONING.md)
- [Security Policy](SECURITY.md)
- [Examples Overview](examples/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports and guidance with JSON, JSONL, TSV, schema, and task-local file artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces inspectable local research artifacts, review-ready deliverable packages, and lifecycle/status surfaces for long-running tasks.]

## Skill Version(s):

0.5.0 (source: server release metadata and RELEASE_NOTES.md, released 2026-06-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
