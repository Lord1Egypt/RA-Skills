# Tool policy and message routing

Every agent action is bounded by rules saved on the account that owns the environment.
Routing checks those rules before a message moves between agents. Secure routing adds a
post-quantum envelope: a **Kyber-768** session plus an **ML-DSA-44** signature.

All tools here need the owning API key, except `veya_verify_secure_message`.

## Workflow: allow or deny a tool

```json
{
  "tool": "veya_set_tool_policy",
  "arguments": { "apiKey": "veya_live_…", "environmentId": "…", "agentId": "…", "tool": "veya_anchor_proof", "allowed": false }
}
```

The rule is saved on the account. Set `allowed: true` to grant it again.

## Workflow: route a message

```json
{
  "tool": "veya_route_message",
  "arguments": {
    "apiKey": "veya_live_…", "environmentId": "…",
    "id": "msg-1", "fromAgent": "<agentId A>", "toAgent": "<agentId B>",
    "tool": "veya_prove", "payload": { "text": "draft v2" }
  }
}
```

Result includes `policyStatus`: `allowed` or `denied`. A denied rule stays denied; tell the
user which rule applies and how to change it with `veya_set_tool_policy`.

## Workflow: signed delivery

1. Sender identity: `veya_pq_keygen` (see [identity.md](identity.md)).
2. `veya_route_secure_message` with the route fields plus `senderPrivateKeyHex` and
   `senderPublicKeyHex` → secure envelope (session id, signature, `policyStatus`).
3. Receiver: `veya_verify_secure_message` with `message` (the envelope object) and
   `senderPublicKeyHex` → `{ "valid": true }`.

## Workflow: invoke a coordination tool

```json
{
  "tool": "veya_boundnet_invoke",
  "arguments": { "apiKey": "veya_live_…", "environmentId": "…", "agentId": "…", "toolName": "…", "arguments": {} }
}
```

`POST /v1/environments/:id/boundnet/invoke`. The agent's policy decides whether the call runs.

## Tools

### `veya_set_tool_policy`

Allow or deny a tool for an agent. Requires the API key that owns the environment. Saved on that account.

- **Access:** API key (owner)
- **Returns:** Saved rule

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `agentId` | string | yes |  |
| `tool` | string | yes |  |
| `allowed` | boolean | yes |  |

### `veya_route_message`

Check the saved tool rule for this API key before routing. Deny stays deny.

- **Access:** API key (owner)
- **Returns:** Route result with `policyStatus` (`allowed`/`denied`)
- **Notes:** A denied rule stays denied.

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `id` | string | yes |  |
| `fromAgent` | string | yes |  |
| `toAgent` | string | yes |  |
| `tool` | string | yes |  |
| `payload` | any JSON | no |  |

### `veya_route_secure_message`

Check the saved tool rule for this API key, then wrap an allowed message in a Kyber-768 session and an ML-DSA-44 signature.

- **Access:** API key (owner)
- **Returns:** Secure envelope (session id, signature, `policyStatus`)

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `environmentId` | string | yes |  |
| `id` | string | yes |  |
| `fromAgent` | string | yes |  |
| `toAgent` | string | yes |  |
| `tool` | string | yes |  |
| `payload` | any JSON | no |  |
| `senderPrivateKeyHex` | string | yes |  |
| `senderPublicKeyHex` | string | yes |  |

### `veya_verify_secure_message`

Verify ML-DSA signature on a secure routed message envelope

- **Access:** Public
- **Returns:** `{ valid }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `message` | object | yes |  |
| `senderPublicKeyHex` | string | yes |  |

### `veya_boundnet_invoke`

Invoke a Boundnet / coordination tool via product API (policy gated)

- **Access:** API key
- **Returns:** `{ httpStatus, body }`

| Arg | Type | Required | Notes |
|---|---|---|---|
| `apiKey` | string | yes | product key `veya_dev_…` / `veya_live_…` |
| `sessionToken` | string | no | guest JWT, listing only |
| `environmentId` | string | yes |  |
| `agentId` | string | yes |  |
| `toolName` | string | yes |  |
| `arguments` | object | no |  |

