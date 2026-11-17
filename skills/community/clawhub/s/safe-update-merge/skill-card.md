## Description:

Safely merges upstream OpenClaw updates into a fork while preserving custom UI, plugin, skill, workspace, session, and gateway changes through a two-phase merge, build, restart, and user-confirmed promotion workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and operators maintaining a customized OpenClaw fork use this skill to check upstream divergence, merge on a temporary branch, resolve conflicts with optional Claude assistance, validate builds and protected patterns, and promote only after manual verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can perform high-impact repository operations, restart the OpenClaw gateway, and force-push to the target branch during promotion.

Mitigation: Run in a disposable clone or VM first, use --dry-run, verify remotes and branches before --promote, and promote only after manually confirming the gateway is healthy.

Risk: Optional automated conflict resolution sends redacted conflicted file content to the Claude CLI and depends on the quality of the generated merge resolution.

Mitigation: Use --no-auto-resolve for sensitive repositories, inspect resolved diffs, and confirm protected patterns and validation reports before promotion.

Risk: The background-session panel can let operators view and message cron or isolated agent sessions.

Mitigation: Install that UI only when this operator access is intended, and restrict access to trusted users.

Risk: Dependency installation and upstream fetches introduce network activity during validation and merge checks.

Mitigation: Review upstream package changes first and run package installation with lifecycle scripts disabled as provided by the validation workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/safe-update-merge)
- [Publisher profile](https://clawhub.ai/user/maverick-software)
- [OpenClaw upstream repository](https://github.com/openclaw/openclaw)
- [Skill instructions](artifact/SKILL.md)
- [Merge manifest](artifact/MERGE_MANIFEST.json)
- [Safe merge update script](artifact/scripts/safe-merge-update.sh)
- [Preflight script](artifact/scripts/preflight.sh)
- [Validation script](artifact/scripts/validate.sh)
- [Secret redaction script](artifact/scripts/redact-secrets.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update Git branches, build artifacts, validation reports, redacted conflict files, and a pending promotion state file during execution.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
