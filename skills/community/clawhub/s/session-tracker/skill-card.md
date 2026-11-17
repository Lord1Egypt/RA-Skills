## Description:

Session-tracker checkpoints multi-step file or code work to disk so an agent can resume after a crash, timeout, or dropped session without losing progress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darkd](https://clawhub.ai/user/darkd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to track qualifying multi-step work that writes files or generates code, preserving task state and recovery notes when a session is interrupted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session state persists task names, step descriptions, file paths, and progress notes on disk.

Mitigation: Avoid using the skill for secret-bearing or privacy-sensitive tasks, and do not log credentials, tokens, private keys, environment values, or file contents.

Risk: Cleanup is destructive if pointed at the wrong session directory.

Mitigation: Use a dedicated project .session directory, keep the ownership marker in place, and run cleanup --dry-run before cleanup --force.

Risk: Opt-in filesystem scan, journal, and monitor features increase local state collection and process-management surface.

Mitigation: Keep --fs-scan, --journal, and monitor disabled unless needed, and rely on the default minimal tracking mode for normal use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/darkd/skills/session-tracker)
- [ClawHub security audit](https://clawhub.ai/darkd/skills/session-tracker/security-audit)
- [Security review history](references/SECURITY.md)
- [Changelog](references/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and local state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes session state under .session/ by default; filesystem scanning, monitor, and journal features are opt-in.]

## Skill Version(s):

2.6.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
