## Description:

Normalize a public HTTPS audio file to a bounded 128 kbps MP3 with measured loudness, duration, and SHA-256 evidence through Utilia's wallet-funded x402 service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohamedkuch](https://clawhub.ai/user/mohamedkuch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to normalize user-approved public HTTPS audio for podcast leveling, voice-note cleanup, transcription preparation, and consistent agent-generated audio, saving a bounded MP3 and reporting loudness, duration, and digest evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a remote paid audio-normalization service and sends approved public audio URLs to Utilia.

Mitigation: Approve only public audio URLs intended for Utilia, and use the service only when the remote processing and retained route, request, network, payer, and transaction metadata are acceptable.

Risk: The workflow requires Solana wallet credentials to be available to a downloaded npm client.

Mitigation: Use a dedicated low-balance Solana wallet with no unrelated authority, prefer a keypair file over an environment private key, and never paste private keys into chat or commands.

Risk: The npm client initiates a paid USDC transaction during normalization.

Mitigation: Run the doctor check first, verify the package and payment destination independently, and rely on the documented hard maximum of $0.01 per call before approving execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohamedkuch/skills/utilia-audio-normalization)
- [Utilia MCP endpoint](https://api.utilia.ink/mcp)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Markdown with shell commands and concise status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a local MP3 file path plus reported input/output loudness, duration, and SHA-256 evidence; payment requires local Solana credentials.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
