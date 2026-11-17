# Flowcharts, Sequence Diagrams & State Machines

Three diagram families live here. Pick by what the user wants to show:

| User intent | Endpoint | Grammar |
|---|---|---|
| Decision flow, algorithm steps, request branching | `/draw/mermaid` (`m=`) | Mermaid `graph`/`flowchart` |
| Time-ordered call chain, API handshake, actor interactions | `/draw/seq` | `n=`/`e=` node-edge |
| State machine, lifecycle, status transitions | `/draw/lifecycle` | `n=`/`e=` node-edge |

## 1. Flowchart — `/draw/mermaid?m=...`

### When to Use

Function-level logic, authentication flows, pipeline stages with branches, algorithm walkthroughs. Good when the answer is "what happens, in what order, and under which conditions".

> The `mermaid` endpoint renders **only** `graph`/`flowchart` (plus `gantt`, see `general-charts.md`). Other Mermaid dialects return 400: `only "graph/flowchart" and "gantt" are supported`. Sequence syntax belongs to `/draw/seq` below.

### URL Schema & Encoding Rule

```
https://x-cmd.com/draw/mermaid?m=<url-encoded mermaid graph>&title=...
```

- Put the whole Mermaid program in `m=` as **one line** (statements separated by `;`), or use `%0A` for newlines.
- **Confidentiality**: `m=` carries the entire flowchart program in the URL — for private codebases, genericize labels (e.g. `AuthService` → `auth`) or get user approval before rendering (see `SKILL.md` Step 4).
- Encoding beyond the common table (space `%20`, `&` `%26`, `#` `%23`, newline `%0A`): `[` `%5B`, `]` `%5D`, `{` `%7B`, `}` `%7D`, `?` `%3F`, `|` `%7C`, `>` in arrows may stay literal but `%3E` is safest when a label contains it.
- Shapes: `A[box]`, `A(text)`, `A{decision}`, `A((round))`. Edge labels: `-->|label|` or `-.->` dashed.

### Minimal Working Example

Raw:
```
graph TD; A[Start]-->B{Valid?}; B-->C[OK]; B-->D[Retry]
```
URL:
```
https://x-cmd.com/draw/mermaid?m=graph%20TD%3B%20A%5BStart%5D--%3EB%7BValid%3F%7D%3B%20B--%3EC%5BOK%5D%3B%20B--%3ED%5BRetry%5D&title=Minimal%20flow
```

### Production Repo Example

Token-verification flow with labelled branches:

```
https://x-cmd.com/draw/mermaid?m=graph%20TD%3B%20U%5BLogin%5D--%3EV%7Bvalid%20token%3F%7D%3B%20V--%3EG%5BGrant%20access%5D%3B%20V--%3ED%5BDeny%5D&title=Auth%20flow
```

### Anti-Patterns & Limits

- Do not paste `sequenceDiagram`/`erDiagram`/`classDiagram` into `m=` — 400. Use `/draw/seq`, `/draw/erd`, `/draw/class` instead.
- Labels containing `?` must be `%3F`, or the parser reads a new statement.
- Keep ≤ ~15 nodes per flowchart; split long pipelines into per-function charts.
- A literal `+` in a label must be `%2B`.

## 2. Sequence Diagram — `/draw/seq`

### When to Use

Request lifecycles, API handshakes, RPC call chains, anything where **time order and caller/callee** matter more than topology.

### URL Schema & Encoding Rule

Same `n=`/`e=` grammar as architecture diagrams (`references/architecture.md` for full field table), with `seq`-specific conventions:

```
https://x-cmd.com/draw/seq?n=<actor>[&n=<actor>...]&e=<msg>[&e=<msg>...]&title=
n=id;type;label[;sub]        # actors in left-to-right order (types: ext/fe/be/db/cloud/sec/bus/svc)
e=from;to;label              # message, top-to-bottom in call order
e=from;to;label;dash         # return message (dashed arrow)
```

### Minimal Working Example

```
https://x-cmd.com/draw/seq?n=c;fe;Client&n=s;be;Server&e=c;s;request&e=s;c;response;dash&title=Ping
```

### Production Repo Example

Order-creation handshake across four actors, with token verification and dashed returns:

```
https://x-cmd.com/draw/seq?title=API%20handshake&n=c;fe;Client&n=g;be;API%20Gateway&n=a;sec;Auth&n=s;be;Service&e=c;g;POST%20%2Forders&e=g;a;verify%20token&e=a;g;claims;dash&e=g;s;forward&e=s;g;201%20Created;dash
```

### Anti-Patterns & Limits

- Actors must be declared as `n=` first; an `e=` referencing an undeclared id fails.
- Message order = the order `e=` parameters appear in the URL — reorder parameters to reorder the lifeline.
- Keep ≤ ~12 actors and ≤ ~20 messages; a denser trace is better summarized as an `archmap` plus notes.

## 3. State Machine — `/draw/lifecycle`

### When to Use

Status transitions (order/payment/job state), protocol states, retry/rollback logic.

### URL Schema & Encoding Rule

Same `n=`/`e=` grammar; node types are `state`, `decision` (diamond), `terminal` (rounded end). Edge labels go in the third field of `e=`.

```
https://x-cmd.com/draw/lifecycle?n=<id>;state;<label>[&n=...]&e=<from>;<to>[;<label>]&title=
```

### Minimal Working Example

```
https://x-cmd.com/draw/lifecycle?n=a;state;Idle&n=b;state;Running&e=a;b;start&title=Minimal%20states
```

### Production Repo Example

Order lifecycle with a payment decision diamond and terminal states:

```
https://x-cmd.com/draw/lifecycle?title=Order%20flow&n=new;terminal;Created&n=paid;state;Paid&n=shipped;state;Shipped&n=done;terminal;Delivered&n=ok;decision;Payment%20OK%3F&e=new;ok&e=ok;paid;capture&e=paid;shipped;ship&e=shipped;done
```

### Anti-Patterns & Limits

- Every transition needs an explicit `e=`; unreachable states still render but signal a gap in your scan.
- Decision diamonds should have ≥2 outgoing edges — label each (`;capture`, `;retry`) so the branches are legible.
