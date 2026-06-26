# AAP Agent Bounty (Claimant Skill)

Verification-first helper for:
- proof checks,
- claim payload preparation,
- optional 0 ETH claim submission on Base.

## Requirements

### Required
- `gh`, `cast`
- `BASE_RPC_URL`

### Optional
- `GH_TOKEN` (fallback when local `gh auth login` context is unavailable)

## Deterministic confirmation gate

Broadcast is permitted only when input includes:
- `confirm_broadcast: true`

Otherwise return:
- `pending: confirmation_missing`

## Scope

- Checks proof status and prepares claim context.
- Shows exact transaction command before any submission.
- If no GitHub auth context: return `pending: github_auth_missing`.
- If signer context unavailable: return `pending: signer_context_missing`.

## Target

Zero-transfer wallet (reward distribution verification only):
`0x53033d3965259D9FfDf0A80d0A249A1D5979266F`

## Security baseline

- No raw private key / seed phrase / mnemonic collection.
- `gh` and `cast` rely on user-managed local credential/signer contexts.
- Skill does not require passing raw `--private-key`.
- Use least-privilege token scope when `GH_TOKEN` is used.

## Claim payload

`AAP_CLAIM:THESIS:TRUMP_100:ANSWER:yes:GITHUB:<github_username>:X:@<x_handle>`
