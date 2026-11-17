## Description:

Copies OpenClaw configuration and key information from its default location to a backup file path.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yegou777](https://clawhub.ai/user/yegou777)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to back up OpenClaw configuration files that may contain API keys, endpoints, and related sensitive settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can duplicate OpenClaw configuration and key material into plaintext files.

Mitigation: Install and run it only when plaintext backup is intended, store backups under a scoped user-controlled path, and restrict file permissions manually.

Risk: The helper accepts broad source and destination paths, which can copy arbitrary sensitive files if misused.

Mitigation: Avoid /root/keys.txt and arbitrary source paths unless explicitly required; review the source and target paths before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yegou777/skills/save-secure-keys)
- [ClawHub publisher profile](https://clawhub.ai/user/yegou777)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute a Python helper that copies sensitive configuration data to a local plaintext destination file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
