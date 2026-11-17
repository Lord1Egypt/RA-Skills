## Description:

Use Utilia's wallet-funded x402 client for live Solana mainnet priority fees, transaction diagnosis, token-risk inspection, unsigned transaction simulation, PDF-to-Markdown conversion, and audio normalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohamedkuch](https://clawhub.ai/user/mohamedkuch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need paid, machine-readable Solana preflight evidence, including priority-fee estimates, transaction analysis, token-risk inspection, and unsigned transaction simulation. It can also route authorized public PDFs and audio files to Utilia for Markdown extraction or bounded MP3 normalization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run downloaded third-party wallet and payment clients, including an unpinned AgentCash command path.

Mitigation: Use a dedicated low-balance wallet, prefer pinned or pre-reviewed package versions, and avoid SOLANA_PRIVATE_KEY when a narrowly scoped keypair path is sufficient.

Risk: Persistent MCP mode can leave wallet-funded paid calls available to an agent session.

Mitigation: Configure MCP with a dedicated low-balance keypair, review the environment passed to the server, and disable the integration when persistent access is not needed.

Risk: Requested signatures, mints, transactions, account addresses, public PDFs, and public audio files are sent to Utilia for processing.

Mitigation: Submit only data the user is authorized to share, avoid private documents or recordings, and confirm approval before media calls.

Risk: Unsigned transaction simulation can become stale as block state and balances change.

Mitigation: Present simulation as preflight evidence rather than a guarantee of future execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohamedkuch/skills/utilia-solana-preflight)
- [Utilia priority fees endpoint](https://api.utilia.ink/v1/fees/priority)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration, structured evidence summaries, and optional file outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include settled price, transaction receipt details, JSONL fee-feed entries, page-delimited Markdown, or a normalized MP3 file depending on the selected command.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
