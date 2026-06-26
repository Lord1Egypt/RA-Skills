# Storage and State

Recommended local sidecars:

- `<file>.rid` for retrieval id
- `<file>.seal` for getseal JSON
- `<file>.cw.json` for local metadata
- `<file>.verify.json` for verify response JSON

Recommended metadata fields:

- `version`
- `sourcePath`
- `lookupInfo`
- `sha256`
- `retrievalId`
- `registeredAt`
- `sealPath`
- `verifyPath`
- `lastSealReceivedAt`
- `lastVerifiedAt`
- `lastError`

Credential storage:

- save issued credentials to a fresh secret path
- format: `apiKey apiCredential`
- restrict file permissions
- avoid storing credentials inside watched data trees
