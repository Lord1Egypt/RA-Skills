## Description:

泉水复活 helps QClaw users back up, snapshot, sync, verify, and restore AI memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xzxy1](https://clawhub.ai/user/xzxy1)

### License/Terms of Use:

MIT-0

## Use Case:

QClaw users and agents use this skill to preserve AI and user memory files through local backups, timestamped snapshots, cloud sync, integrity checks, and restore workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive QClaw memory, diary, user, identity, and agent-rule files may be copied into a cloud-synced folder.

Mitigation: Install only when that cloud sync behavior is acceptable, and use a trusted private cloud location rather than a shared or untrusted folder.

Risk: Crafted restore snapshots can overwrite files outside the intended workspace.

Mitigation: Do not restore snapshots from untrusted or shared cloud locations unless restore handling validates ZIP paths, authenticates snapshots, previews changes, and confirms before overwriting files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xzxy1/skills/spring-fountain-revival)
- [ClawHub publisher profile](https://clawhub.ai/user/xzxy1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to run backup, snapshot, sync, restore, list, and integrity-check commands against QClaw memory files.]

## Skill Version(s):

1.0.0 (source: evidence release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
