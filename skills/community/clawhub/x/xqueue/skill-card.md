## Description:

File-based X/Twitter post scheduler. Drop tweets into day/time folders, they post automatically. No frontend, no app - your file system is the UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[madebydia](https://clawhub.ai/user/madebydia)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Xqueue to schedule X/Twitter posts, threads, media posts, and community posts by placing text and media files into day and time folders. It is intended for personal or team social posting workflows that can be run from cron with X API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A queue-isolation weakness could allow symlinked files outside the queue to be posted to X under the user's account.

Mitigation: Use a private queue directory that untrusted users and processes cannot write to, and avoid symlinks in the queue.

Risk: When deleteAfterPost is enabled, successfully posted content and media are removed after posting.

Mitigation: Keep backups of scheduled content and media if retaining originals matters.

Risk: The skill can post scheduled content and media to X using the user's account credentials.

Mitigation: Review queued files before enabling cron, start with dryRun when validating setup, and only provide credentials for an account authorized for this posting workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/madebydia/skills/xqueue)
- [Xqueue Homepage](https://github.com/madebydia/xqueue)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operating guidance for a local file-based queue; posting behavior depends on the user's configured cron schedule, queue contents, and X API credentials.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
