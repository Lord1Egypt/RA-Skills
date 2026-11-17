## Description:

Security audit + append-only logging + monitoring for OpenClaw skills (file-level diff, baseline approval, SHA-256 integrity).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ucloud-sec](https://clawhub.ai/user/ucloud-sec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security or operations engineers use this skill to statically audit OpenClaw skill directories, record append-only audit logs, compare file-level changes, and generate concise monitoring notifications before installing or updating skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Snapshot logic can preserve sensitive readable files outside the intended skill directory when an audited skill contains escaping symlinks.

Mitigation: Restrict access to the audit directory and avoid auditing untrusted skill packages until symlink containment is fixed or independently verified.

Risk: Monitoring notifications and diff summaries can expose change details to the configured delivery target.

Mitigation: Verify the notification destination before enabling monitoring and send concise summaries by default, with detailed diffs reviewed locally when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ucloud-sec/skills/test0413-6348)
- [Publisher Profile](https://clawhub.ai/user/ucloud-sec)
- [Skill Definition](artifact/SKILL.md)
- [Scripts README](artifact/scripts/README.md)
- [Notification Template README](artifact/templates/README.md)
- [Audit Log Template](artifact/log-template.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, notification text, and NDJSON/JSON audit records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The audit workflow produces local append-only logs, state files, baseline records, git-backed snapshots, file-level change summaries, and optional notification text.]

## Skill Version(s):

1.5.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
