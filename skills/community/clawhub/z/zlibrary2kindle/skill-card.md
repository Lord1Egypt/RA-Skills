## Description:

Search Z-Library for books, download them, and send to your Kindle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[semihum](https://clawhub.ai/user/semihum)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search for books on Z-Library, download EPUB files, and send selected files to a whitelisted Kindle email address.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow runs unpinned third-party command-line code with Z-Library and email credentials.

Mitigation: Use a pinned and verified zlibrary2kindle version, prefer revocable app-specific passwords, and avoid exporting long-lived credentials into broad shell environments.

Risk: Session cookies and downloaded files are handled locally before email delivery.

Mitigation: Review where session cookies are stored, confirm downloaded files may be emailed, and verify local deletion behavior matches the user's expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/semihum/skills/zlibrary2kindle)
- [Publisher profile](https://clawhub.ai/user/semihum)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that invoke zlibrary2kindle via uvx, pip, or z2k and use user-provided service and email credentials.]

## Skill Version(s):

0.1.1 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
