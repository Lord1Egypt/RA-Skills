# Cryptowerk API Notes

Known working curl-based flow:

1. `POST https://www.cryptowerk.com/api/issue-key`
   - may return `402` with x402 payment challenge
   - after successful paid retry, returns JSON with:
     - `apiKey`
     - `apiCredential`
     - `requesterId`
   - in some middleware configurations, may return `200` directly without x402

2. `POST https://aiagent.cryptowerk.com/platform/API/v8/register`
   - send `X-API-Key: <apiKey> <apiCredential>`
   - use query params `hashes` and optional `lookupInfo`
   - returns `documents[0].retrievalId`

3. `POST https://aiagent.cryptowerk.com/platform/API/v8/getseal`
   - send `X-API-Key: <apiKey> <apiCredential>`
   - use query params `retrievalId` and `provideVerificationInfos=true`
   - may return pending before a seal exists

4. `POST https://aiagent.cryptowerk.com/platform/API/v8/verifyseal`
   - send `X-API-Key: <apiKey> <apiCredential>`
   - use query params `verifyDocHashes` and `seals`

Important field note:
- issue-key returns `apiCredential`, not `credential`
- stored combined token format should be:
  - `apiKey apiCredential`

Operational note:
- `issue-key.sh` writes a fresh token only when you pass an output path
- `register-file.sh`, `get-seal.sh`, and `verify-file.sh` require `CRYPTOWERK_X_API_KEY`
- required local tools are `curl`, `python3`, and one SHA-256 provider (`shasum`, `sha256sum`, or `openssl`)
