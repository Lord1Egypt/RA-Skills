## Description:

Google Calendar via gcalcli: today-only agenda by default, bounded meaning-first lookup via agenda scans, and fast create/delete with verification--optimized for low tool calls and minimal output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onsra520](https://clawhub.ai/user/onsra520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent manage Google Calendar through the authenticated gcalcli command line tool. It supports agenda lookup, bounded search, event creation, event deletion, and delete-then-recreate style edits with concise responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill operates through authenticated gcalcli and can read, create, edit, and delete Google Calendar events.

Mitigation: Install only for accounts where agent-mediated calendar access is acceptable, and review gcalcli authentication and calendar configuration before use.

Risk: The security summary flags deletes and edits that may occur without a final confirmation.

Mitigation: Change the action policy to require confirmation for all deletes and edits before deployment when stricter control is needed.

Risk: The security guidance flags unsafe command patterns and possible shell interpolation issues.

Mitigation: Execute commands with safely separated arguments, avoid shell-interpolated user input, and pin the gcalcli version used in the runtime.

Risk: The setup examples include command-line OAuth client credentials.

Mitigation: Prefer gcalcli init or another manual OAuth setup path instead of passing OAuth secrets on a command line.

## Reference(s):

- [gcalcli](https://github.com/insanum/gcalcli)
- [Google Calendar API](https://www.googleapis.com/calendar/)
- [Google OAuth2 token service](https://oauth2.googleapis.com/)
- [ClawHub skill page](https://clawhub.ai/onsra520/skills/quick-gcalcli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Concise natural-language responses, with markdown and shell commands when the user asks for command details or setup guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses minimal output by default and suppresses CLI details unless requested.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
