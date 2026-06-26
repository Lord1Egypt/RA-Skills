---
name: skytale
description: The trust layer for AI agents — encrypted channels, identity, audit, attestations, trust circles, key rotation, and federation. MLS protocol (RFC 9420).
version: 0.5.1
metadata:
  openclaw:
    requires:
      env:
        - SKYTALE_API_KEY
      anyBins:
        - python3
        - python
    primaryEnv: SKYTALE_API_KEY
    emoji: "🔒"
    homepage: https://skytale.sh/docs/integrations/openclaw
    os:
      - darwin
      - linux
---

# Skytale Encrypted Shared Context

You have access to Skytale MCP tools for end-to-end encrypted agent messaging and shared context. All messages are encrypted using the MLS protocol (RFC 9420). The relay server cannot read message contents.

## When to activate

Use Skytale tools when the user asks about:
- Encrypted or secure communication between agents
- Private messaging channels
- Shared context, memory, or state between agents
- Sending/receiving messages that must not be intercepted
- Multi-agent coordination over encrypted channels
- Agent identity, trust, or attestations
- Key rotation or forward secrecy
- Encrypted audit logging for compliance
- Cross-organization agent federation
- Anything mentioning "Skytale"

## Prerequisites

The Skytale MCP server must be configured in your openclaw.json. If tools are unavailable, instruct the user to:

1. Install: `pip install skytale-sdk[mcp]`
2. Add the `skytale` MCP server to their openclaw.json (see examples/openclaw-config.json in the skill directory)
3. Set `SKYTALE_API_KEY` environment variable (get one at https://app.skytale.sh)

## Available MCP tools

### Channel lifecycle
- `skytale_create_channel(channel)` -- Create an encrypted channel. Channel names use `org/namespace/service` format (e.g. `acme/research/results`).
- `skytale_channels()` -- List all active channels.

### Messaging
- `skytale_send(channel, message)` -- Send an E2E encrypted message to all channel members.
- `skytale_receive(channel, timeout)` -- Receive buffered messages. Returns all messages since last check. Default timeout: 5 seconds.

### Key exchange (manual)
- `skytale_key_package()` -- Generate an MLS key package (hex-encoded). Used when manually adding members.
- `skytale_add_member(channel, key_package_hex)` -- Add a member using their key package. Returns a hex-encoded MLS Welcome message.
- `skytale_join_channel(channel, welcome_hex)` -- Join a channel using a Welcome message from the channel owner.

## Multi-agent setup

For two agents to communicate:

1. Agent A calls `skytale_create_channel("org/team/channel")`.
2. Agent B calls `skytale_key_package()` and shares the result with Agent A.
3. Agent A calls `skytale_add_member("org/team/channel", key_package_hex)` and shares the Welcome with Agent B.
4. Agent B calls `skytale_join_channel("org/team/channel", welcome_hex)`.
5. Both agents can now `skytale_send` and `skytale_receive` on the channel.

When using the hosted API with invite tokens (recommended), this handshake is automated -- the SDK handles key exchange through the API server.

## SDK features (beyond MCP tools)

The Skytale SDK (0.5.1+) includes modules that agents can use alongside MCP tools for richer security capabilities. These are used via the Python SDK directly, not through MCP tool calls.

### Encrypted Shared Context
Encrypted key-value state shared across all channel members. Supports typed entries, scoped access, TTL, and structured handoffs.

```python
from skytale_sdk.context import SharedContext, ContextType

ctx = SharedContext(mgr, "acme/research/results")
ctx.set("task_status", {"phase": "analysis", "progress": 0.7})
ctx.set("search_results", results, type=ContextType.ARTIFACT)
ctx.set("private_analysis", data, visible_to=["did:key:z6MkAgentB..."])
ctx.handoff("did:key:z6MkAgentB...", {"task": "summarize"}, tried=["approach_1"])
ctx.subscribe(lambda key, val: ..., type_filter=ContextType.HANDOFF)
```

### Agent Identity
Cryptographic Ed25519 DID:key identities for agents. Generate, sign, and verify. Supports DID:key and DID:web identity types.

```python
from skytale_sdk import AgentIdentity
identity = AgentIdentity.generate()
print(identity.did)  # did:key:z6Mk...
signature = identity.sign(b"message")
```

### Key Rotation
Rotate MLS leaf keys for forward secrecy. Generates a new UpdatePath commit and advances the group epoch.

```python
mgr.rotate_key("acme/secure/channel")
```

### Encrypted Audit Logging
Hash-chained tamper-evident logs encrypted with MLS exporter secrets. Stored server-side as opaque ciphertext for compliance (EU AI Act Article 12).

```python
from skytale_sdk import SkytaleChannelManager
mgr = SkytaleChannelManager(identity=b"agent", api_key="sk_live_...", audit=True)
audit_key = mgr.export_audit_key("acme/secure/channel")

from skytale_sdk.audit import EncryptedAuditLog
enc_log = EncryptedAuditLog(mgr.audit_log, audit_key)
enc_log.record({"event": "analysis_complete"})
encrypted_entries = enc_log.pending_entries()
```

### Cross-Organization Federation
Join channels across organizations using federation invite tokens.

```python
mgr.join_federation("partner-org/shared/channel", "skt_fed_abc123...")
```

### Attestations
SD-JWT attestations for agent trust and reputation. Issue claims about other agents with selective disclosure.

```python
from skytale_sdk import AgentIdentity, create_attestation, verify_attestation
issuer = AgentIdentity.generate()
att = create_attestation(issuer, "did:key:z6Mk...", {"task_score": 0.95}, disclosed=["task_score"])
valid = verify_attestation(att, issuer.public_key)
```

### Trust Circles
Credential-gated MLS groups. Only agents meeting admission policies can join.

```python
from skytale_sdk import TrustCircle, AdmissionPolicy
policy = AdmissionPolicy(required_claims=["certification"], min_score=0.8)
circle = TrustCircle.create(mgr, "acme/trusted/group", policy)
```

### Agent Registry
Discover agents by capability via the Skytale API. Supports visibility tiers (public, organization, private).

```python
mgr.register_agent(capabilities=["analysis", "summarization"])
agents = mgr.search_agents(capability="analysis")
```

## Rules

- NEVER log, display, or include encryption keys, key packages, or Welcome messages in user-visible output. Treat them as opaque tokens passed between tools only.
- NEVER include API keys in messages sent through channels.
- Channel names MUST follow `org/namespace/service` format.
- Always call `skytale_receive` with a reasonable timeout (2-10 seconds). Do not poll in tight loops.
- When creating channels for the user, suggest descriptive names matching their use case.
- If `skytale_receive` returns no messages, inform the user and offer to check again -- do not retry silently.

## Error handling

- **MCP tools not available**: Tell the user to configure the Skytale MCP server in their openclaw.json and install `skytale-sdk[mcp]`.
- **Authentication failure**: Check that `SKYTALE_API_KEY` is set and valid. Direct the user to https://app.skytale.sh to obtain a key.
- **Channel not found on receive/send**: The channel must be created or joined first.
- **Listener died**: The background connection was lost. Recreate the channel.
