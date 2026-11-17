# Choose a connection and rehearse before funding

The skill is instructions. Reading it does not give a host tools, a wallet,
or permission to spend. These are connection recipes; a compatible format
is not evidence that a particular host completed a payment.

## Choose the path this host can actually use

| Available capability | Useful next step | What still needs checking |
| --- | --- | --- |
| Read public URLs | Read the menu and item contract; explain a suitable result. | Without an HTTP tool that exposes response headers, an x402 quote may be unreadable. |
| Make HTTP requests and read headers | Obtain an unsigned quote; prepare a no-spend rehearsal. | Payment client, matching scheme/network, balance and user approval. |
| Connect remote MCP | Connect to https://scvd.store/mcp/verifier for free evidence tools, or https://scvd.store/mcp for the store catalog and purchase tools. Read tools/list for actual availability. | A buy tool being listed does not supply a signer. |
| Install skills and run local tools | Install this skill; use an existing compatible wallet or the official setup in [wallet.md](wallet.md). | Secure authentication, funding and purchase approval are separate steps. |

## Hermes

The website index is https://scvd.store/.well-known/skills/index.json.
It lists every file needed by each skill, including these references.
With Hermes installed, inspect before installing:

```sh
hermes skills search https://scvd.store --source well-known
hermes skills inspect well-known:https://scvd.store/.well-known/skills/scvd-personal-shopper
hermes skills install well-known:https://scvd.store/.well-known/skills/scvd-personal-shopper
```

Keep the host's normal security scan. If it refuses, report the finding;
do not recommend forcing installation or disabling the scan.
[Official skills documentation](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills).

## Skills CLI, Claude Code and Codex

Use the host's supported skill installer, or the Skills CLI's agent selection:

```sh
npx skills add seancrecord/scvd-general-store-repo --skill scvd-personal-shopper
```

[Official Skills CLI documentation](https://skills.sh/docs).
A local skill installation does not configure a wallet or remote MCP connection.

## OpenClaw and ClawHub

Search ClawHub for `scvd-personal-shopper`; inspect the publisher, source,
version, files and scan result before installing. Source repository:
https://github.com/seancrecord/scvd-general-store-repo/tree/main/skills/scvd-personal-shopper.
If a listing is unavailable or under review, use a supported GitHub or direct-URL
installation path. Do not treat a private publish receipt as a public listing.
[Official ClawHub documentation](https://docs.openclaw.ai/clawhub).

## Muse, ChatGPT, Claude and Grok chat

Use the store's paste prompt or link to the skill when the session can read
URLs. Determine available tools in that session. A product name or subscription
tier does not establish shell access, MCP access, a wallet, or payment support.
If the session can only read, return a useful recommendation and the missing
capability. Never claim that pasting the prompt installed a skill.

## No-spend rehearsal

When requested, stop before installing a wallet, signing, funding or paying.
Use the selected item's compact contract and an ordinary unsigned request,
without an automatic payment wrapper. Return a small plan the user can keep:

- Intended result and item URL; required inputs supplied or still missing.
- Quote observation time; exact quoted amount, asset, network, scheme and recipient.
- Host capabilities actually observed, capabilities only reported, and unknowns.
- Matching wallet/client support, or the specific mismatch or unknown.
- Funding and purchase decisions still required; known fees and unresolved fees.
- Next available free step and what would unblock a purchase.

Do not include secrets or signable payment payloads. Missing inputs remain
missing; do not invent them to make a rehearsal look complete. This is a plan,
not a payment authorization, reserved price, settlement test or compatibility
certificate. Fetch a fresh quote and re-check approval before any later payment.
