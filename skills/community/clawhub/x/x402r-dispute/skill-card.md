## Description:

Pay merchants and file payment disputes on the x402r refundable payments protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vraspar](https://clawhub.ai/user/vraspar)

### License/Terms of Use:

MIT

## Use Case:

External developers and agents use this CLI to make escrow payments, file refund disputes, check dispute status, view submitted evidence, and replay arbiter rulings for the x402r refundable payments protocol.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet credentials and payment state can put funds at risk if reused with valuable wallets or stored insecurely.

Mitigation: Use a low-value dedicated test wallet, avoid passing private keys in shell commands, prefer managed secrets where possible, and restrict permissions on ~/.x402r.

Risk: Payment and dispute data may be sent to arbiter, court, Pinata, merchant, RPC, and on-chain endpoints.

Mitigation: Verify endpoint URLs before use and avoid submitting sensitive evidence or payment data that should not be shared with those services.

Risk: Evidence pinning can fall back to a placeholder CID, which can weaken or invalidate a dispute record.

Mitigation: Configure real evidence pinning, confirm the returned CID before filing disputes, and avoid valuable disputes until fail-closed evidence handling is in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vraspar/skills/x402r-dispute)
- [x402r homepage](https://x402r.org)
- [x402r support](https://github.com/x402r/x402r-arbiter-eigencloud/issues)

## Skill Output:

**Output Type(s):** [shell commands, configuration, text, JSON, files, guidance]

**Output Format:** [Markdown guidance with shell commands, CLI text output, JSON-parseable command results, and local state files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can save payment and dispute state under ~/.x402r and can write response bodies to user-selected files.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
