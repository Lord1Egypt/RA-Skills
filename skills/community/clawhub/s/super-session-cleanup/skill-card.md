## Description:

Session Cleanup helps Claw-family agents track and clean up temporary files, scripts, installed skills, libraries, and software generated during a conversation session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaobs](https://clawhub.ai/user/chaobs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Claw-family agent users use this skill to track session-created artifacts and clean up temporary files, installed packages, skill directories, and other transient resources at the end of a conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch cleanup can remove packages and skill directories with weaker safeguards than the skill promises.

Mitigation: Inspect the session-track file, run a dry-run preview, and require exact paths or package names before approving removal.

Risk: Cleanup actions can delete files or uninstall dependencies that may still be needed.

Mitigation: Use the skip list for retained items, avoid one-click cleanup, and require confirmation for package, software, and skill removal.

## Reference(s):

- [Session Cleanup Reference Guide](references/cleanup-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/chaobs/skills/super-session-cleanup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown checklist summaries with inline shell commands and JSON tracking records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run previews, deletion summaries, and user-confirmation prompts for package, software, and skill removal.]

## Skill Version(s):

1.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
