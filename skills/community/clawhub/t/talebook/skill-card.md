## Description:

Talebook helps an agent manage a Talebook/MyBooks personal library by querying library and reading statistics, searching books, updating metadata, uploading books, and sending books to email or reading devices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poxenstudio](https://clawhub.ai/user/poxenstudio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a Talebook/MyBooks personal library through a Python command-line API client. It supports book discovery, metadata maintenance, reading-state updates, uploads, ISBN-based physical-book additions, and delivery to email or supported reading devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials and session data are sent to a user-configured Talebook/MyBooks server.

Mitigation: Use only a server you control, prefer HTTPS, and avoid LAN or public HTTP hosts for credentialed use.

Risk: Book upload and delivery actions can send local files or books to configured destinations.

Mitigation: Confirm upload paths and recipient device or email destinations before execution, and do not provide paths to sensitive non-book files.

Risk: Library modification tools can change metadata, reading states, favorites, and collection entries.

Mitigation: Use a least-privileged Talebook account and review requested write operations before running them.

## Reference(s):

- [MyBooks homepage](https://www.mybooks.top)
- [ClawHub Talebook skill listing](https://clawhub.ai/poxenstudio/skills/talebook)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TALEBOOK_HOST, TALEBOOK_USER, and TALEBOOK_PASSWORD environment variables.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
