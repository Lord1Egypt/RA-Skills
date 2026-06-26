# XMTP Support in Studio

Use this reference when the user asks how buyer/seller messaging works on Studio.

## What exists today

Studio support chat uses XMTP for **transaction-linked support conversations**.

This is for:
- buyer ↔ seller support
- issue resolution after a real purchase or paid usage relationship
- dispute handling on supported surfaces

It is **not** a global cold-DM system.

## Current scope

- support is relationship-gated
- both sides currently need a linked **Base** wallet
- both sides need XMTP turned on in Studio Settings
- the skill can now use wallet-signed support APIs and a local XMTP helper

Settings path:
- `Dashboard -> Settings -> XMTP`

## Skill commands

Authenticate the wallet for support APIs:
```bash
python {baseDir}/scripts/support_auth.py login
```

Check support eligibility for a listing:
```bash
python {baseDir}/scripts/support_threads.py eligibility endpoint cataas
```

Open or reuse a support thread:
```bash
python {baseDir}/scripts/support_threads.py open endpoint cataas
```

List support threads for the wallet:
```bash
python {baseDir}/scripts/support_threads.py list
```

Show one support thread:
```bash
python {baseDir}/scripts/support_threads.py show <thread_id>
```

Read XMTP messages for a thread:
```bash
node {baseDir}/scripts/xmtp_support.mjs messages <thread_id>
```

Send an XMTP message into a thread:
```bash
node {baseDir}/scripts/xmtp_support.mjs send <thread_id> "Need help with this endpoint"
```

Revoke other XMTP installations for the current wallet:
```bash
node {baseDir}/scripts/xmtp_support.mjs revoke-others
```

## Requirements

- `WALLET_ADDRESS`
- `PRIVATE_KEY`
- optional `SUPPORT_AGENT_TOKEN`
- `node` available for `xmtp_support.mjs`

The XMTP helper keeps a persistent local database under:
- `~/.x402studio/xmtp/`

Keep that directory between runs. XMTP's docs state that losing the local database creates a new installation, and an inbox is limited to 10 active installations before revocation is required.

Sources:
- XMTP agent env + persistent DB requirements: https://docs.xmtp.org/agents/get-started/build-an-agent
- XMTP installation limits and revocation: https://docs.xmtp.org/chat-apps/core-messaging/manage-inboxes
- XMTP agent local database guidance: https://docs.xmtp.org/agents/build-agents/local-database

## What an agent should say

If the user wants support chat and it is not ready:
- tell them to link a Base wallet in Studio
- tell them to turn on XMTP in Settings
- if XMTP hit the installation limit, tell them to use:
  - `Revoke Other Installations`

## Good guidance examples

- `Support chat is available after a real purchase relationship exists.`
- `Turn on XMTP in Studio Settings with your linked Base wallet first.`
- `If XMTP says your inbox already has too many installations, use Revoke Other Installations in Settings and try again.`
