## Description:

Manages OpenClaw session files by trimming large sessions, generating summaries, archiving older sessions, and cleaning up storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delgyd](https://clawhub.ai/user/delgyd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators maintaining OpenClaw environments use this skill to reduce session storage, retain compact summaries, and archive older JSONL session history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Session history can be rewritten, deleted, compressed, or moved during archive and trim operations.

Mitigation: Run the scripts manually on a test copy first, confirm target paths, and keep recoverable full backups before applying changes to active sessions.

Risk: Recurring cron execution can repeatedly modify session data through fixed root-oriented paths.

Mitigation: Avoid setup_cron.sh until the path, schedule, confirmation flow, logging, and uninstall behavior are reviewed and adjusted for the target environment.

Risk: Generated summaries and archives can contain sensitive session data such as commands, private paths, and credentials.

Mitigation: Store summaries and archives with restricted access, review them before sharing, and handle them as sensitive operational data.

Risk: Dependency installation guidance can alter the runtime environment unnecessarily.

Mitigation: Remove the pip install line identified by the security guidance and verify dependencies through the environment's normal package management process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/delgyd/skills/session-archive-manager)
- [Publisher Profile](https://clawhub.ai/user/delgyd)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands plus JSON summaries and compressed archive files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local session archives, summaries, cron entries, and compressed backups.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
