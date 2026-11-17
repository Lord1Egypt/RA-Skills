## Description:

Find and fix leaked API keys, tokens and passwords in your AI agent's config, long/short-term memory and session transcripts (OpenClaw + Claude Code). Use when the user asks to check token or secret safety, scan for leaked credentials, audit agent memory, MEMORY.md, CLAUDE.md or chat history for secrets, move plaintext tokens in openclaw.json to env vars, or stop secrets from being written into memory. Also use after editing openclaw.json or when setting up a new OpenClaw instance. Secret values are never printed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maoisdamao](https://clawhub.ai/user/maoisdamao)

### License/Terms of Use:

MIT

## Use Case:

Developers using OpenClaw or Claude Code use this skill to find exposed credentials in configuration, memory, and transcripts, migrate OpenClaw configuration secrets, and reduce the chance of new leaks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Removing the OpenClaw Git guard can also delete existing pre-commit checks when hooks have been manually combined.

Mitigation: Save existing hooks before enabling the guard. If hooks were combined, remove only the guard command manually or use a corrected uninstaller.

Risk: Configuration migration handles sensitive credentials and creates a secrets file and backups.

Mitigation: Review the migration dry run and protect the resulting secrets file and backups.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/maoisdamao/skills/token-safety-checker)
- [Project source and documentation](https://github.com/maoisdamao/token-safety-checker)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown summaries with findings, file locations, remediation guidance, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Secret values are not printed; reports use paths, line numbers, detector names, lengths, and fingerprints.]

## Skill Version(s):

3.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
