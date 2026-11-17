## Description:

Wake Up schedules personalized AI wake-up phone calls through wake.meup.ai, including phone verification, voice selection, scheduling, and x402 USDC payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brianium](https://clawhub.ai/user/brianium)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use Wake Up to verify a phone number and schedule one or more paid AI wake-up calls with optional personalization hints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Solana signing key for automatic paid x402 API calls without strong local payment limits.

Mitigation: Use a dedicated low-balance Solana wallet, never a primary wallet, and review every verification or scheduled call as a paid third-party action.

Risk: Phone numbers, schedule details, and optional personalization hints are shared with wake.meup.ai.

Mitigation: Avoid sensitive personal details in hints and keep personalization concise.

Risk: Changing the API endpoint could direct paid requests to an untrusted service.

Mitigation: Keep the default wake.meup.ai endpoint unless the replacement endpoint is fully trusted.

## Reference(s):

- [Wake Up homepage](https://wake.meup.ai)
- [Wake Up OpenClaw documentation](https://wake.meup.ai/openclaw)
- [uv documentation](https://docs.astral.sh/uv/)
- [x402 protocol](https://www.x402.org/)
- [ClawHub skill page](https://clawhub.ai/brianium/skills/wake-meup-ai)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON API examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and a Solana keypair with USDC.]

## Skill Version(s):

1.3.0 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
