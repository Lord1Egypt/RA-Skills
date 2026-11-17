## Description:

Builds Telegram inline-button file browsers and menu-style navigators for browsing directories, paging lists, previewing files, returning to parent views, closing menus, and exposing copyable file paths from an agent workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[just-cj](https://clawhub.ai/user/just-cj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a Telegram-based file browser to OpenClaw workflows, with inline navigation, file action menus, previews, copyable paths, and downloads. It is intended for workspace file browsing where the operator understands which local files may be exposed through Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Callback handling and file-transfer paths can expose local files or run unsafe commands.

Mitigation: Review before normal use; pass callbacks as safely quoted arguments or argv, bind callback tokens to the active session and version, and require clear user intent before downloading files.

Risk: Preview or download actions can operate on paths that no longer match the intended browser root, especially around resolved paths and symlinks.

Mitigation: Revalidate preview and download paths against the configured root immediately before use, including symlink-safe checks.

Risk: The skill has a suspicious security verdict in ClawHub evidence.

Mitigation: Install only if the operator is comfortable granting the skill access to browse and send files from the OpenClaw workspace through Telegram, and fix the security guidance items before normal use.

## Reference(s):

- [Telegram File Browser Interaction Patterns](references/interaction-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/just-cj/skills/telegram-file-browser)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with Python and shell command examples, plus JSON-style Telegram message payloads and file delivery actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegram menu messages, inline button matrices, preview text, copyable paths, and file-send actions; button arrays must remain two-dimensional.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
