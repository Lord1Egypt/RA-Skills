## Description:

Monitor and interact with SOLO.ro accounting platform via CLI or TUI (summary, revenues, expenses, queue, e-factura, company). Use when a user asks to check their accounting data, view invoices, expenses, or e-factura documents, or translate a task into safe solo-cli commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rursache](https://clawhub.ai/user/rursache)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect SOLO.ro accounting summaries, invoices, expenses, e-Factura records, company profile data, uploads, and queue actions through safe solo-cli commands or TUI guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install an unpinned third-party CLI before accessing accounting data.

Mitigation: Install only if the `rursache/tap/solo-cli` Homebrew tap is trusted and verify the CLI source or package before use.

Risk: The CLI stores SOLO.ro credentials and cached session cookies on the local filesystem.

Mitigation: Protect `~/.config/solo-cli/config.json` and `~/.config/solo-cli/cookies.json` with owner-only permissions and avoid shared or cloud-synced locations.

Risk: Queue deletion can remove accounting workflow items.

Mitigation: Require explicit user confirmation before running `solo-cli queue delete <ID>` or alias deletion commands.

## Reference(s):

- [solo-cli help man page](references/help-man-page.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that read, upload, or delete SOLO.ro accounting records; users should review commands before execution.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
