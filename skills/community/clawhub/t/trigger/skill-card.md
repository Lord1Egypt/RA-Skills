## Description:

Trigger is a command-line productivity tracker for recording, reviewing, searching, and exporting local workflow entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use Trigger to capture plans, reminders, reviews, reports, and other workflow notes from a shell, then inspect or export the local activity history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently stores user-entered plans, reminders, reviews, and similar workflow data locally.

Mitigation: Avoid entering sensitive personal, business, or credential-like information unless the storage location, permissions, and retention are acceptable.

Risk: Export commands can consolidate stored history into JSON, CSV, or TXT files.

Mitigation: Review exported files before sharing, archiving, or moving them outside the approved environment.

Risk: The security summary notes vague documentation and behavior that includes persistent storage, search, and export.

Mitigation: Review the command behavior before installation or deployment and set an approved data directory when local storage controls are required.

## Reference(s):

- [Trigger Skill Page](https://clawhub.ai/ckchzh/skills/trigger)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text command output with optional JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores user-entered workflow data in local log files and can consolidate that history into export files.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
