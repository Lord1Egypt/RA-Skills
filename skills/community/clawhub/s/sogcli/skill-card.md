## Description: <br>
Standards Ops Gadget is a CLI for IMAP, SMTP, CalDAV, CardDAV, and WebDAV that provides an open-standards alternative to Google and Microsoft operations CLIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[visionik](https://clawhub.ai/user/visionik) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation-focused users use this skill to operate standards-compliant mail, calendar, contacts, tasks, and file services from an agent-assisted CLI workflow. It is suited for generating and explaining sog commands, account setup steps, output-format choices, and provider compatibility considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential handling and account access can expose mail, calendar, contacts, tasks, and files if used with untrusted accounts or unsafe shell history practices. <br>
Mitigation: Use only trusted accounts, store credentials through the native keychain flow, and avoid passing passwords directly in shell commands. <br>
Risk: Disabling TLS protections can expose credentials and account data. <br>
Mitigation: Prefer HTTPS/TLS with certificate validation, and reserve --insecure or --no-tls for isolated testing only. <br>
Risk: The idle --exec behavior can run commands in response to incoming mail. <br>
Mitigation: Do not use idle --exec unless the command and mailbox trigger path are fully trusted and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/visionik/sogcli) <br>
- [Sog homepage](https://github.com/visionik/sogcli) <br>
- [Go install package](https://github.com/visionik/sogcli/tree/main/cmd/sog) <br>
- [README](artifact/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; generated sog commands may produce human-readable text, JSONL, or TSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the sog binary and trusted account credentials; supports provider auto-discovery and protocol-specific credential setup.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and CHANGELOG, released 2026-01-24) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
