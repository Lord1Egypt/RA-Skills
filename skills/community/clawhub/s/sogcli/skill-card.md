## Description:

Standards Ops Gadget is a CLI for IMAP/SMTP, CalDAV, CardDAV, and WebDAV that provides an open-standards alternative to Google and Microsoft operations CLIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[visionik](https://clawhub.ai/user/visionik)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation agents use Sog to configure standards-based accounts and operate mail, calendars, contacts, tasks, files, and meeting invites through IMAP/SMTP, CalDAV, CardDAV, WebDAV, and iTIP/iMIP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can access configured mail, calendar, contacts, task, and WebDAV accounts.

Mitigation: Install only after reviewing whether that account access is acceptable for the intended environment.

Risk: Transport and credential-safety controls can be weakened with --no-tls, --insecure, http:// DAV URLs, or --storage file.

Mitigation: Use keychain storage and HTTPS/TLS-only endpoints; avoid those flags and URL forms unless the weaker posture is intentional.

Risk: delete, clear, send, upload, move, and contact/calendar update commands perform real remote account mutations.

Mitigation: Review command targets and arguments before execution, especially in unattended or scripted runs.

Risk: sog idle --exec executes a shell command when new mail arrives.

Mitigation: Avoid --exec by default; if used, restrict it to reviewed static commands in a trusted account context.

Risk: The security evidence marks this release suspicious due to under-documented command execution and credential-safety risks.

Mitigation: Use a pinned, reviewed version and re-check the security guidance before deployment.

## Reference(s):

- [Sog README](artifact/README.md)
- [Sog changelog](artifact/CHANGELOG.md)
- [Sog homepage](https://github.com/visionik/sogcli)
- [Go install package](https://pkg.go.dev/github.com/visionik/sogcli/cmd/sog)
- [Publisher profile](https://clawhub.ai/user/visionik)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples; CLI output may be human-readable text, JSONL, or TSV.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the sog binary and configured account credentials; several commands can mutate remote mail, calendar, contact, task, or WebDAV data.]

## Skill Version(s):

0.3.0 (source: evidence.release.version and CHANGELOG, released 2026-01-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
