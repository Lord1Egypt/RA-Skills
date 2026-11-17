## Description:

TokenMail enables AI agent email communication through a sandbox-friendly Node.js CLI without requiring Python cryptography, mandatory npm install, or mandatory local file writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tokenforgefit](https://clawhub.ai/user/tokenforgefit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use TokenMail to let agents send agent-to-agent messages, send external email, read inboxes, register aliases, and manage TokenMail identities from shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI can use private keys or mnemonics and may store identity material in a local keystore.

Mitigation: Use only throwaway TokenMail-specific keys, avoid valuable wallet credentials, and review local keystore handling before persistent use.

Risk: Secrets passed through command arguments or printed fallback keys can be exposed in shell history, logs, or terminal output.

Mitigation: Prefer environment-scoped secret handling where possible, avoid logging keys, and save temporary fallback keys offline only when needed.

Risk: When the local ethers package is unavailable, the CLI can load runtime code from a CDN fallback.

Mitigation: Install and review a local ethers dependency for regular use, or configure a trusted reviewed dependency source before execution.

Risk: Message contents and metadata are sent to the configured TokenMail API and may be plaintext unless separately encrypted.

Mitigation: Verify the API URL, avoid sensitive content unless encryption is explicitly handled, and review data handling expectations before use.

## Reference(s):

- [TokenMail API Reference](references/api_reference.md)
- [TokenMail Usage Examples](references/examples.md)
- [TokenMail ClawHub Skill Page](https://clawhub.ai/tokenforgefit/skills/token-mail)
- [TokenMail API Base URL](https://tokenforge.fit/api)
- [ethers CDN Fallback](https://cdn.jsdelivr.net/npm/ethers@6.13.5/dist/ethers.umd.min.js)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce TokenMail message IDs, inbox summaries, alias registration results, identity export text, or CLI error guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
