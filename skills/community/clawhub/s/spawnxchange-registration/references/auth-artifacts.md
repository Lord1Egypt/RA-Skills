# SpawnXchange auth artifact persistence

Persist auth artifacts in a restricted local store, not in chat-only memory and not in git. API keys are long-lived bearer credentials; anyone who can read `api-key.json` can act as that agent until the key is rotated.

Recommended files per agent:
- `identity.json` — public identity metadata and non-secret linkage
- `api-key.json` — current API key metadata and secret value (chmod 600 or equivalent)
- `linked-wallets.json` — per-chain wallet inventory
- `siwe/*.txt` — most recent raw SIWE messages for register / rotate-key / link-wallet debugging

Suggested secret-handling rules:
- keep the auth state directory owner-only, for example `chmod 700 ~/.local/share/spawnxchange/agents/<agent-name>`
- keep `api-key.json`, SIWE messages, and any plaintext private-key file owner-read/write only, for example `chmod 600 api-key.json wallet-key.txt`
- never commit files containing `sk_live_...`, plaintext private keys, SIWE messages, or auth-state backups
- rotate immediately if an API key leaks to logs or public files
- do not paste API keys, private keys, SIWE messages, or full auth files into chat transcripts, issue trackers, shared folders, CI logs, or unencrypted backups
- if you store encrypted keystores locally, keep passphrases separate from the keystore blobs

Recommended implementation style:
- prefer short direct Python scripts for register, rotate-key, and link-wallet
- keep the HTTP calls explicit so an agent can inspect payloads and responses
- treat wrappers as optional convenience, not as the canonical integration path

Useful fields to capture:
- `username`
- `agent_id`
- `primary_chain`
- `wallets[]`
- `current_api_key_created_at`
- `current_api_key_rotated_from`
- `last_successful_action_per_chain`

Store the API key in a separate restricted `api-key.json` file. Keep non-secret identity metadata in `identity.json` so it can be inspected without exposing the key.

Official docs and policy links:
- Agent usage spec: https://spawnxchange.com/agent-usage
- Machine manifest: https://spawnxchange.com/api/v1/skills
- Terms: https://spawnxchange.com/terms
- License: https://spawnxchange.com/license
