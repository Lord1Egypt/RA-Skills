# EGRESS.md — SettlementWitness Network Behavior

SettlementWitness can run fully offline for receipt verification.

## No network is used for

- Parsing a receipt JSON file
- Extracting signed core fields
- Recomputing the canonical digest (RFC 8785 / JCS)
- Verifying `receipt_id` against the digest
- Verifying the Ed25519 signature against the bundled public key registry
- Checking all bundled sample fixtures (`--self-test`)

## Optional network — used only when explicitly requested

| Action | Endpoint |
|---|---|
| Request a new signed receipt | `POST https://defaultverifier.com/settlement-witness` |
| Refresh public key registry | `GET https://defaultverifier.com/.well-known/sar-keys.json` |
| Inspect receipt / chain state | `https://defaultverifier.com/verified` |

These calls are never made automatically. They are initiated only by explicit
user instruction or agent action.

## External domain

The only domain this skill contacts is:

```
defaultverifier.com
```

No other hosts are contacted.

## What is never sent

SettlementWitness must never send:

- Raw inbox contents
- Raw private files
- Full chat history
- Secrets, credentials, or API keys
- Wallet keys or seed phrases

## Remote emission payload

When remote receipt issuance is explicitly requested, the call sends only the
`task_id`, acceptance `spec`, and claimed `output` that you explicitly pass.
No surrounding context, history, or credentials are included.

If the output is sensitive, use local verification only and skip remote
emission.

## Future attribution

Future remote calls may include a static client label such as:

```
X-Settlement-Client: skill-rest/0.1.0
```

This label is used only for aggregate activation measurement. It does not
identify the user and is not part of the signed receipt core — it has no effect
on `receipt_id`, `sig`, or verdict.
