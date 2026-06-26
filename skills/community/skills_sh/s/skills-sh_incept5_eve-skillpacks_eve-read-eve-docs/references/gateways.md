# Chat Gateway

## Use When
- You need to configure Slack/Nostr message ingestion and outbound responses.
- You need to map external chat identities and events into Eve workflows.
- You need to validate webhook behavior or provider-specific security checks.

## Load Next
- `references/events.md` for inbound event types and payload expectations.
- `references/agents-teams.md` for target agent/team routing after normalization.
- `references/cli.md` for integration management commands.

## Ask If Missing
- Confirm provider (`slack` or `nostr`) and deployment environment.
- Confirm signing secret / signing key inputs are available.
- Confirm thread/client mappings (`team_id`, integration ids) before editing mappings.

## Overview

The Gateway service normalizes external chat events into Eve events using a pluggable provider architecture. Providers implement the `GatewayProvider` interface and register via factories at startup. Two transport models exist: webhook (HTTP push) and subscription (persistent connection).

## Transport Models

| Model | Mechanism | Example |
|-------|-----------|---------|
| **Webhook** | Platform sends HTTP POST to Eve endpoint | Slack |
| **Subscription** | Eve connects to external relay and listens | Nostr |

## Provider Interface

Every provider implements the `GatewayProvider` contract:

| Member | Purpose |
|--------|---------|
| `name` | Unique provider identifier (e.g., `slack`, `nostr`) |
| `transport` | `'webhook'` or `'subscription'` |
| `capabilities` | Feature flags: threads, reactions, file uploads |
| `initialize(config)` | Lifecycle hook: setup connections, load state |
| `shutdown()` | Lifecycle hook: close connections, flush state |

### Webhook-Specific Methods

| Method | Purpose |
|--------|---------|
| `validateWebhook(req)` | Verify request authenticity (signatures, challenge handling) |
| `parseWebhook(req)` | Parse payload into: `message`, `handshake`, or `ignored` |

### Shared Methods

| Method | Purpose |
|--------|---------|
| `sendMessage(target, content)` | Deliver outbound message to provider-specific target |
| `resolveIdentity(externalUserId, accountId)` | Map external user to Eve identity |

## Provider Lifecycle

1. Factories register at startup in `app.module.ts`.
2. Instances are created per integration (one per org integration).
3. `initialize(config)` is called to set up the provider (load secrets, open connections).
4. Provider processes events for the lifetime of the integration.
5. `shutdown()` is called on teardown (close sockets, flush state).

Subscription providers start persistent connections on `initialize()` and tear them down on `shutdown()`. Webhook providers are stateless between requests.

### Built-in Provider Factories

The gateway registers four provider factories at startup:

| Provider | Transport | Push model | When to use |
|----------|-----------|------------|-------------|
| `slack` | webhook | Slack Web API (`chat.postMessage`) | Slack workspace integration |
| `nostr` | subscription | Nostr relay publish | Decentralized / Nostr clients |
| `webchat` | subscription | WebSocket push (gateway port) | Browser apps that want a direct gateway socket |
| `api` | subscription (poll) | **No-op** — clients poll `GET /threads/{id}/messages` | REST/polling apps, mobile apps, embedded `provider: app` flows whose backend proxies through Eve |

Unknown provider types now produce a `delivery.provider_missing` warning instead of throwing 404, so apps using new provider strings degrade gracefully — the message is still persisted to `thread_messages`.

### Hot-Loading New Integrations

The gateway polls the API for active integrations every **30 seconds**. When a new integration is detected (e.g., after a Slack OAuth install completes), it is initialized automatically without requiring a gateway restart. Only new integrations are loaded — existing instances are not re-initialized during polling.

## WebhookController Dispatch

```
POST /gateway/providers/:provider/webhook
```

1. Controller extracts `:provider` from path parameter.
2. Looks up initialized provider instance in the registry.
3. Calls `validateWebhook(req)` -- reject on failure, respond to handshake challenges.
4. Calls `parseWebhook(req)` -- returns `message`, `handshake`, or `ignored`.
5. For `message` results, routes the normalized event through the agent resolution pipeline.

## Slack Provider (Webhook)

### Endpoints

| Endpoint | Purpose |
|----------|---------|
| `POST /gateway/providers/slack/webhook` | All Slack Events API payloads (mentions, messages, URL verification) |
| `POST /gateway/providers/slack/interactive` | Slack interactive payloads (button clicks, e.g., membership approval) |

### Signature Validation

Slack requests are validated using the per-org signing secret from `oauth_app_configs`. Each org configures their own Slack app with `eve integrations configure slack --signing-secret "..."`. The gateway reads the signing secret from the integration's enriched `settings_json` (populated by the API from `oauth_app_configs`). The provider computes `HMAC-SHA256(signing_secret, v0:timestamp:body)` and compares against the `X-Slack-Signature` header. Invalid signatures are rejected before parsing. Both the webhook and interactive endpoints use the same per-org signing secret.

### Event Parsing Flow

1. Event arrives at webhook endpoint.
2. Signature validated with signing secret.
3. Duplicate check: `event_id` from the Slack envelope checked against in-memory cache (see [Deduplication](#deduplication)).
4. Integration resolved: `team_id -> org_id`.
5. Identity interception: Slack user resolved to Eve identity before agent routing (see [Identity Interception](#identity-interception)).
6. Event type determines dispatch path:

### Message vs app_mention Events

| Event Type | Trigger | Dispatch Path |
|------------|---------|---------------|
| `app_mention` | User writes `@eve ...` | Parsed as `@eve <agent-slug> <command>`, routed to specific agent |
| `message` | Any message in subscribed channel (no mention) | Dispatched to channel/thread listeners only |

For `app_mention`:
- First word after `@eve` is tested as agent slug.
- If it matches a known slug, route directly to that agent's project.
- If no match, route to org `default_agent_slug` with full text as command.
- Agent slug resolves to `{project_id, agent_id}` (unique per org).
- Job created for the agent; thread + event recorded.

For `message` (no mention):
- Only dispatched if channel/thread has active listeners.
- Each listener agent receives a separate job in its own project.

### Listener Mechanics

```
@eve agents listen <agent-slug>     # channel-level or thread-level
@eve agents unlisten <agent-slug>   # remove listener
@eve agents listening               # show active listeners
@eve agents list                    # directory of slugs
```

#### Thread-Scoped vs Channel-Scoped

- Command issued in a **channel**: creates a channel-level listener. All `message` events in that channel are dispatched.
- Command issued inside a **thread**: creates a thread-level listener. Only messages within that specific thread are dispatched.
- Multiple agents can listen to the same channel or thread.
- Listener subscriptions stored in `thread_subscriptions` with `subscriber_type: agent`.

### Outbound

Responses delivered via Slack Web API (`chat.postMessage`), threaded to the originating message.

### Platform Sentinel Channel Routing

The gateway has one special-case Slack routing path for Platform Sentinel.

- If `EVE_SENTINEL_CHANNEL_ID` is set and an inbound Slack message arrives in that channel, the gateway does **not** send the message through normal agent routing.
- Instead it calls the API responder endpoint:

```text
POST /internal/platform-respond
```

- The API returns markdown text, and the gateway sends that text back to the same Slack channel/thread.

Supported responder keywords:

| Keyword | Result |
|---------|--------|
| `health`, `status` | Full platform health report |
| `degraded`, `issues` | Only degraded/critical environments |
| `resources`, `report` | Current alias of the health report |
| `help`, `cmds`, `commands` | Command help text |

Operational notes:
- `EVE_SENTINEL_CHANNEL_ID` is a deployment-time env var on the gateway, not a dynamic DB lookup.
- Keep it aligned with the system setting `sentinel.slack.channel_id`.
- Outbound sentinel alerts still use the normal gateway delivery path (`/internal/deliver`); the special routing above is only for inbound messages in the sentinel channel.

### Interactive Endpoint

`POST /gateway/providers/slack/interactive` handles Slack interactive components (buttons, modals, menus).

- Content-Type: `application/x-www-form-urlencoded` with a `payload` field containing a JSON string.
- Signature validated using the same per-org signing secret as the webhook endpoint.
- Routes by `action_id` to the appropriate handler.

Supported actions:
- `membership_approve` -- approve a pending org membership request.
- `membership_deny` -- deny a pending org membership request.

Returns `200 OK` with an optional message update to replace the interactive message in Slack.

## Nostr Provider (Subscription)

### Connection Model

Connect to configured relay(s) via WebSocket. Subscribe to events targeting the platform pubkey.

### Inbound Event Types

| Kind | Type | Description |
|------|------|-------------|
| Kind 4 | NIP-04 Encrypted DM | Private message to platform pubkey |
| Kind 1 | Public Mention | Public note tagging platform pubkey |

### Inbound Flow

1. Relay broadcasts event matching subscription filters.
2. Provider verifies **Schnorr signature** on the event.
3. Kind 4 events are decrypted using **NIP-04** (shared secret derived from sender pubkey + platform private key).
4. Message normalized to standard inbound format.
5. Agent slug extracted from content.
6. Routed through the same chat dispatch pipeline as Slack.

### Agent Slug Extraction (Nostr)

| Pattern | Example |
|---------|---------|
| `/agent-slug <text>` | `/mission-control review PR` |
| `agent-slug: <text>` | `mission-control: review PR` |
| First word of public mention | `mission-control review PR` |

If no slug matches, the org default agent is used.

### Outbound Mechanics

| Context | Event Kind | Details |
|---------|-----------|---------|
| DM reply | Kind 4 | NIP-04 encrypted, published to relays |
| Public reply | Kind 1 | NIP-10 reply threading tags (`e` and `p` tags) |

### Cross-Relay Deduplication

Event IDs are tracked in a bounded set (10k entries). Duplicate events from multiple relays are dropped.

## Deduplication

Slack may deliver the same event more than once (retries on slow response, network glitches). The gateway tracks `event_id` values in a short-lived in-memory cache:

- On receipt, the `event_id` from the Slack event envelope is checked against the cache.
- If already seen, return `200 OK` immediately with no further processing.
- If new, store the `event_id` and continue normal processing.
- Cache entries expire after a short TTL (order of minutes) -- long enough to cover Slack's retry window.

## Timeout Handling

Slack retries webhook deliveries if no response within **3 seconds**. To avoid duplicate deliveries:

- The webhook handler acknowledges (`200`) as quickly as possible.
- Slow work (identity resolution, agent routing, job creation) runs asynchronously after the HTTP response.
- This ensures the 3-second deadline is met even under load.

## Identity Interception

Before agent routing, the gateway resolves the Slack user to an Eve identity. This happens after integration lookup (`team_id -> org_id`) but before agent slug parsing:

1. Sender's Slack user ID checked against known identity links for the org.
2. If resolved, processing continues to agent routing.
3. If unresolved, the user receives a helpful error explaining how to link their Slack account.

### Reserved Commands

The `link` command is reserved and checked before agent slug resolution. `@eve link` initiates the identity linking flow regardless of whether a `link` agent exists. This ensures new users can always link their accounts, even before any agents are configured.

## Multi-Tenant Mapping

- `team_id -> org_id` stored at integration connect time.
- Agent slugs in `agents.yaml` are unique per org, selecting the target project/agent.

## Identity Resolution

`resolveIdentity(externalUserId, accountId)` maps an external user (Slack user ID, Nostr pubkey) to an Eve identity. External identities are stored in `external_identities` and linked to Eve users/orgs for permission checks and audit trails.

## Gateway Discovery Policy

Agents must opt in to be visible and routable from gateways. See `agents-teams.md` for full details.

| Policy | Directory | Direct chat | Internal dispatch |
|--------|-----------|-------------|-------------------|
| `none` | Hidden | Rejected | Works |
| `discoverable` | Visible | Rejected (hint) | Works |
| `routable` | Visible | Works | Works |

Directory endpoint: `GET /internal/orgs/{org_id}/agents` -- filters out `none` agents, supports `?client=slack`.

Slug routing: `POST /internal/orgs/{org_id}/chat/route` -- enforces `routable` policy and `gateway_clients` whitelist.

## Agent Slug Extraction (Summary)

| Provider | Pattern | Fallback |
|----------|---------|----------|
| Slack | `@eve <slug> <command>` | Org default agent |
| Nostr | `/slug <text>` or `slug: <text>` or first word | Org default agent |

## Thread Key Format

Thread continuity uses a canonical key scoped to the integration account:

```
account_id:channel[:thread_id]
```

- Slack: `T123ABC:C456DEF:1234567890.123456`
- Nostr: `<platform-pubkey>:<sender-pubkey>`

## WebChat Provider

Browser-native agent chat via WebSocket. Follows the subscription transport model (like Nostr).

**Connection:**
```
ws://gateway:4820/?token=<jwt>
```

**Send message:**
```json
{"type": "message", "text": "Hello", "agent_slug": "coder", "thread_id": "optional"}
```

**Receive reply:**
```json
{"type": "message", "text": "Queued 1 job(s)...", "thread_id": "...", "timestamp": "..."}
```

Features:
- JWT auth in WebSocket handshake using Eve JWKS verification (`RS256`, `exp`, `nbf`, `kid`)
- Heartbeat ping/pong (30s interval)
- Thread continuity across reconnections
- Multi-tab support (same user, multiple connections)

Registration: configured as an integration with `provider: webchat`.

Use provider `app` and the conversations facade for same-origin embedded app panes. Use `webchat` only when a direct browser-to-gateway WebSocket is required. Use provider `api` for generic REST-originated chat clients without browser push.

## API Provider (No-Op for Polling Clients)

The `api` provider exists so that chat routing succeeds for REST clients that do not maintain a push connection. It implements the `GatewayProvider` interface with a no-op `sendMessage()`:

- `name: 'api'`, `transport: 'subscription'`, capabilities: `['inbound', 'outbound']`.
- `initialize()` and `shutdown()` are no-ops — there is no socket, no listener, no connection state.
- `sendMessage()` returns immediately. The agent's reply is already stored in `thread_messages` before the gateway is called; clients retrieve it via polling (`GET /threads/{id}/messages?since=`) or SSE (`GET /threads/{id}/stream`).

Why this exists: before the `api` factory was registered, chat from REST web apps (e.g. `provider: "api"`, `account_id: "eden-web"`) failed with `No active provider instance for api:eden-web`, which marked every reply `delivery_status = failed` even though the message had been persisted. With the no-op provider registered, those deliveries are now `delivered` and the polling/SSE catch-up paths are the source of truth for the client.

Configure via `provider: api` on `chat/route` requests, or as the implicit transport for `provider: app` embedded conversations — no integration row is required.

## Chat Simulation

Test the full routing pipeline without a live provider connection.

```bash
eve chat simulate --project <id> --team-id T123 --channel-id C123 --user-id U123 --text "hello" --json
```

Returns `thread_id` and `job_ids` showing the dispatch result.

## API Endpoints

```
POST /gateway/providers/:provider/webhook       # generic webhook ingress
POST /gateway/providers/slack/interactive        # Slack interactive components

GET  /internal/orgs/{org_id}/agents             # agent directory (filtered by policy)
POST /internal/orgs/{org_id}/chat/route         # slug-based routing

POST /chat/simulate                             # simulate chat message
POST /chat/listen                               # subscribe agent to channel/thread
POST /chat/unlisten                             # unsubscribe agent
GET  /chat/listeners                            # list active listeners
```
