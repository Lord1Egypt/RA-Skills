## Description:

W.A.L.V.I.S. is an AI-powered knowledge manager for saving links, text, and images from Telegram, auto-tagging and organizing them, storing them on Walrus decentralized storage, and browsing them through a web UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuuga-0](https://clawhub.ai/user/kuuga-0)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to capture personal knowledge from Telegram, organize it with summaries and tags, sync it to Walrus testnet storage, and browse or manage the vault through local and hosted web interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports suspicious installer and runtime behavior with persistent OpenClaw behavior.

Mitigation: Review the skill before installation and confirm that persistent OpenClaw behavior is expected for the deployment.

Risk: The security guidance warns against syncing sensitive vault contents to Walrus until encryption is fixed and explicitly verified.

Mitigation: Keep sensitive data out of synced vaults unless Seal encryption has been reviewed, fixed if needed, and verified in the target environment.

Risk: The security guidance calls out wallet-handling paths and package execution risk.

Mitigation: Use a test wallet with no valuable assets and pin npx/package versions before running installer or runtime commands.

Risk: The security guidance warns against running the local dashboard on exposed networks.

Mitigation: Run the dashboard only on trusted local interfaces or behind appropriate network access controls.

Risk: The security guidance recommends removing the SOUL.md injection or requiring explicit opt-in with rollback.

Mitigation: Disable or gate the SOUL.md behavior behind explicit user opt-in and provide a rollback path before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kuuga-0/skills/walvis)
- [Walvis GitHub Repository](https://github.com/Kuuga-0/walvis)
- [Walvis Web App](https://walvis.vercel.app)
- [Walrus Documentation](https://docs.wal.app/)
- [Walrus Sites Documentation](https://docs.wal.app/walrus-sites/intro.html)
- [OpenClaw Documentation](https://docs.openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with command snippets, JSON-backed state updates, and messaging payloads for Telegram-style interactions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local vault files under ~/.walvis and use Walrus testnet, Sui testnet, browser, and messaging tools when enabled.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter and package.json report 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
