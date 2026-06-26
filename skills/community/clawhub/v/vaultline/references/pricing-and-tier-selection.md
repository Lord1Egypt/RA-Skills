# Pricing and Tier Selection

## Default pricing

### Open
- storage: `$0.08 / GB / month`
- retrieval: `$0.015 / GB`
- write: `$0.03 / GB`

### Private
- storage: `$0.12 / GB / month`
- retrieval: `$0.02 / GB`
- write: `$0.045 / GB`

### Common
- list / head / delete: free
- reads under `1 MB` are free for open files
- private access checks still apply to private files even when the read itself is free

## Choose a tier

### Choose `open` when:
- the file is meant to be shared by path/key
- cost matters most
- collaboration is the default
- anyone with the path should be able to pay and retrieve it

### Choose `private` when:
- the file should be restricted to one wallet or an allowlist
- the object contains internal or customer-sensitive data
- the agent needs owner-style control without full encryption

### Choose `encrypted` when it exists:
- ciphertext storage is required
- app-level privacy is not enough
- the service should not store readable plaintext

## Product framing

Use this ladder in agent-facing or user-facing explanations:
- open for sharing
- private for ownership
- encrypted for maximum privacy, coming soon
