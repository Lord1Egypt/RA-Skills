## Description:

Yacli Yandex helps agents work with Yandex Mail, Disk, and Calendar through a configured yacli MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qoderone](https://clawhub.ai/user/qoderone)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to triage, search, read, reply to, and send Yandex Mail; upload, share, publish, and download Yandex Disk files; and view, create, or delete Yandex Calendar events through an authenticated yacli MCP setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a configured Yandex account through yacli, including email, file sharing, and calendar changes.

Mitigation: Install only for intended account operation, review confirmations carefully, and require explicit approval before sends, public links, uploads, downloads, or calendar changes.

Risk: Local tokens, cookies, account snapshots, or generated logs could expose personal data if bundled or published.

Mitigation: Keep real credentials and account data out of the skill bundle and use host-side secret storage for yacli configuration.

Risk: Incorrect mcporter selector syntax can call the wrong tool or fail against dotted yacli tool names.

Mitigation: Use explicit mcporter server and tool arguments, such as --server yacli and --tool yacli.mail.list, when invoking yacli MCP tools.

## Reference(s):

- [Yacli upstream project](https://github.com/NextStat/yacli)
- [Installation](artifact/references/install.md)
- [Example mcporter wiring](artifact/references/mcporter-config.md)
- [yacli Yandex Setup](artifact/references/setup.md)
- [ClawHub skill page](https://clawhub.ai/qoderone/skills/yacli-yandex)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured yacli MCP server, mcporter, and at least one authenticated Yandex account.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
