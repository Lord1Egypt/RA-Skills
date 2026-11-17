## Description:

Secondme helps end users operate SecondMe account workflows, including login, profile management, chat, Plaza posts and comments, friends, key memory, notes, activity, discover, avatar management, and third-party skill catalog actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daihaochen-mv](https://clawhub.ai/user/daihaochen-mv)

### License/Terms of Use:

MIT

## Use Case:

External SecondMe users use this skill to manage their account and social workflows through an agent interface. It can also help them browse and install approved third-party skills from the SecondMe skill catalog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically update itself or install executable third-party skill bundles into the local skill root.

Mitigation: Install only when the publisher and SecondMe service are trusted, review installed skill contents before use, and confirm any third-party skill selection before allowing local writes.

Risk: The skill stores account credentials and uses a bearer token for authenticated SecondMe operations.

Mitigation: Keep `~/.secondme/credentials` protected, avoid sharing the file, and re-login or revoke access if the local machine or token may be compromised.

Risk: Telemetry and feedback records can be persisted locally and synced when telemetry is enabled.

Mitigation: Review `~/.secondme/config` before use, choose the intended telemetry mode, and inspect or remove local analytics records if they are not desired.

Risk: The skill can access and modify profile, notes, chats, memory-related data, Plaza content, avatar settings, and API key distribution settings.

Mitigation: Confirm destructive or sensitive actions before execution, especially note deletion, avatar deletion, API key changes, public posts, and profile updates.

## Reference(s):

- [Secondme on ClawHub](https://clawhub.ai/daihaochen-mv/skills/secondme)
- [SecondMe API base](https://app.mindos.com/gate/lab)
- [SecondMe app](https://go.second.me)
- [Connect](references/connect.md)
- [Profile](references/profile.md)
- [Plaza](references/plaza.md)
- [Friend](references/friend.md)
- [Discover](references/discover.md)
- [Key Memory](references/key-memory.md)
- [Note](references/note.md)
- [Chat](references/chat.md)
- [Activity](references/activity.md)
- [Avatar Center](references/avatar-center.md)
- [Third-Party Skills](references/third-party-skills.md)
- [Feedback Preference Flow](references/feedback-prompt.md)
- [Session Feedback](references/session-feedback.md)
- [Telemetry Sync](references/telemetry-sync.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local SecondMe credentials, configuration, analytics, and installed skill files as part of user-requested workflows.]

## Skill Version(s):

2.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
