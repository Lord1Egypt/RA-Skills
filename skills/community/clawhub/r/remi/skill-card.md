## Description:

Manage Apple Reminders via CLI with section support and iCloud sync. Use when the user asks to create, list, complete, search, or organize reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattheworiordan](https://clawhub.ai/user/mattheworiordan)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent create, list, update, complete, delete, search, and organize Apple Reminders through the remi CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may execute an unpinned third-party remi CLI through npx when remi is not already installed.

Mitigation: Use a preinstalled or pinned trusted remi binary and avoid runtime package downloads in managed environments.

Risk: Delete operations can remove reminders, lists, or sections and changes may sync through iCloud.

Mitigation: Require explicit confirmation with the exact list, reminder, or section identifier before any delete command.

Risk: Programmatic JSON mode bypasses the CLI's interactive delete confirmation behavior.

Mitigation: Implement agent-level confirmation before invoking delete commands with --json.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mattheworiordan/skills/remi)
- [Publisher profile](https://clawhub.ai/user/mattheworiordan)
- [npm package: @mattheworiordan/remi](https://www.npmjs.com/package/@mattheworiordan/remi)
- [Homebrew tap: mattheworiordan/tap/remi](https://github.com/mattheworiordan/homebrew-tap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers remi --json for programmatic use and may invoke npx @mattheworiordan/remi when remi is not on PATH.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
