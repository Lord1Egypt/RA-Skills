---
name: websocket-patterns
description: Deep WebSocket/SSE workflow—handshake and auth, session lifecycle, heartbeats, ordering, backpressure, scaling, and observability. Use when building realtime dashboards, chat, collaborative editing, or live notifications.
---

# WebSocket Patterns (Deep Workflow)

Realtime connections add **stateful** complexity: **who is connected**, **what order** messages arrive, and **what happens** when links flap. Design for **at-least-once** delivery, **explicit** heartbeats, and **horizontal** scaling early.

## When to Offer This Workflow

**Trigger conditions:**

- Replacing polling with **WS** or **SSE**
- Auth on connect; token refresh mid-session
- **Fan-out** to many subscribers; **presence** and **typing** indicators
- Sticky sessions, load balancer timeouts, **reconnect storms**

**Initial offer:**

Use **six stages**: (1) choose transport, (2) connection & auth, (3) protocol & messages, (4) reliability & ordering, (5) scale & ops, (6) security & abuse). Confirm **browser vs server** clients and **proxies** (nginx, ALB, Cloudflare).

---

## Stage 1: Choose Transport

**Goal:** **WebSocket** vs **SSE** vs **long polling**—right tool per direction.

### Heuristics

- **Bidirectional**, low latency, binary payloads → **WebSocket**
- **Server → client** **one-way** streams, HTTP-friendly infra → **SSE**
- **Fire-and-forget** notifications with **simple** infra → consider **push** services first

### Caveats

- **Corporate proxies** historically hurt WS—**test** environments; **WSS** mandatory
- **HTTP/3** **QUIC** stacks differ—validate intermediaries

**Exit condition:** **Transport choice** documented with **why not** alternatives.

---

## Stage 2: Connection & Auth

**Goal:** **Authenticated** sockets without **long-lived** secrets in query strings when avoidable.

### Patterns

- **JWT** in **Sec-WebSocket-Protocol** or **first message** after connect—**prefer** short-lived tokens + **refresh** flow
- **Cookie** sessions with **CSRF** considerations on **same-site** policies
- **Re-auth** before token expiry; **graceful** close with **code** and **reason**

### Authorization

- **Subscribe** to **topics** only after **server-side** check—**never** trust client channel names alone

**Exit condition:** **Auth** diagram: issue token → connect → **authorize** subscriptions.

---

## Stage 3: Protocol & Messages

**Goal:** **Versioned** message schema; **predictable** errors.

### Design

- **Envelope**: `{ type, id, ts, payload }`; **correlation** ids for RPC-style
- **Version** negotiation on connect or **feature** flags in hello message
- **Binary** vs JSON—**protobuf/msgpack** for bandwidth; **JSON** for debuggability early

### Heartbeats

- **Ping/pong** or **application-level** heartbeat at **interval < proxy timeout** (often **30–60s**)
- **Idle** detection and **clean** disconnect

**Exit condition:** **Protocol doc** + **example** session transcript.

---

## Stage 4: Reliability & Ordering

**Goal:** Define **delivery semantics**—usually **at-least-once** over TCP; **ordering** per channel.

### Practices

- **Idempotent** message handlers; **dedupe** by **message id** when retries exist
- **Per-user** sequence numbers if **strict** order matters
- **Buffer** limits: **drop**, **close**, or **apply backpressure** policy

### Reconnect

- **Exponential backoff** + **jitter** to prevent **thundering herd**
- **Resume** from **last seen seq** if **missed messages** are unacceptable—**persist** or **snapshot**

**Exit condition:** **Reconnect** story documented; **storm** mitigation tested.

---

## Stage 5: Scale & Operations

**Goal:** **Many connections** across **many** nodes—**affinity** and **pub/sub** backbone.

### Architecture

- **Sticky sessions** or **shared** **pub/sub** (Redis, NATS, Kafka) for cross-node fan-out
- **Shard** connection maps; **avoid** **single** giant in-memory map on one box

### Observability

- **Metrics**: active connections, msg/sec, **queue depth**, **disconnect** reasons
- **Tracing**: connect → subscribe → **first message** latency

### Load shedding

- **Max** connections per IP/user; **rate limit** connection attempts

**Exit condition:** **Capacity** model: connections per node × **message** **fan-out** cost.

---

## Stage 6: Security & Abuse

**Goal:** **Minimize** attack surface on **long-lived** pipes.

### Controls

- **WSS** everywhere; **validate** **Origin** where applicable
- **Payload size** limits; **compression** **bomb** awareness
- **AuthZ** on every **subscription**; **audit** **admin** actions

### Abuse

- **Spam** detection; **kick/ban** flows; **circuit breakers** on **misbehaving** clients

---

## Final Review Checklist

- [ ] Transport choice justified (WS/SSE/etc.)
- [ ] AuthN/Z on connect and per-channel
- [ ] Heartbeats aligned with proxy/LB timeouts
- [ ] Delivery/idempotency/reconnect semantics explicit
- [ ] Horizontal scale path + observability + abuse controls

## Tips for Effective Guidance

- **ALB idle timeout** vs **heartbeat**—classic production bug; call it out.
- When user says “real-time,” ask **latency target** and **ordering** needs.
- **SSE** is simpler—don’t default to WS for **one-way** feeds.

## Handling Deviations

- **Edge runtimes** (Workers): **different** connection limits and **duration**—validate platform.
- **Mobile**: **background** **suspension**—**push** notifications may complement WS.
