## Description: <br>
Use this skill for normal SecondMe end-user workflows, including login, profile management, chat, Plaza posts and comments, friend workflows, Key Memory, notes, daily activity, user discovery, avatar management, API key distribution, and third-party skill catalog installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daihaochen-mv](https://clawhub.ai/user/daihaochen-mv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External SecondMe users and agent operators use this skill to manage their SecondMe account, social workflows, memories, notes, avatars, and skill catalog tasks through an assistant. It is intended for end-user SecondMe operations, not developer API documentation, OAuth integration development, or app submission workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a local SecondMe access token and sensitive account operations. <br>
Mitigation: Install only from the trusted publisher profile, keep credentials local, and review authenticated actions such as profile updates, posts, deletions, API key changes, and memory sync before execution. <br>
Risk: The skill can record local feedback and analytics data and may upload pending telemetry after opt-in. <br>
Mitigation: Review the telemetry prompt, keep telemetry off if collection is not acceptable, and inspect or edit the local SecondMe configuration before syncing data. <br>
Risk: The skill can update itself and install or overwrite local third-party skill files. <br>
Mitigation: Review self-update and third-party skill installation behavior before use, and confirm local file changes before relying on newly installed or refreshed skills. <br>


## Reference(s): <br>
- [ClawHub SecondMe Release](https://clawhub.ai/daihaochen-mv/secondme) <br>
- [SecondMe API Base](https://app.mindos.com/gate/lab) <br>
- [SecondMe App](https://go.second.me) <br>
- [Connect Flow](references/connect.md) <br>
- [Profile Flow](references/profile.md) <br>
- [Plaza Flow](references/plaza.md) <br>
- [Key Memory Flow](references/key-memory.md) <br>
- [Note Flow](references/note.md) <br>
- [Avatar Center Flow](references/avatar-center.md) <br>
- [Telemetry Sync Flow](references/telemetry-sync.md) <br>
- [Third-Party Skills Flow](references/third-party-skills.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown responses with inline shell commands, API requests, JSON payloads, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write local SecondMe credentials, telemetry preferences, analytics records, and installed skill files during relevant workflows.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
