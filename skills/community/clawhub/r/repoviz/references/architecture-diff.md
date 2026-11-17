# Architecture Diff — Change-Impact Diagrams (`impact` scan mode)

Read this when the user asks what a PR/branch/commit *changes* architecturally:
"what does this PR affect", "impact of this refactor", "before/after the dependency
cleanup", "which modules does this touch". The output is a **delta diagram** plus a
`+`/`-`/`~`/`→` summary — built from `git diff`, not from a fresh full scan.

## Workflow

```text
git diff --name-status <base>...HEAD        # or: git diff for the working tree
        ↓
map changed files → modules (reuse the IR node inventory when one exists)
        ↓
classify each affected module/node:  + added   - removed   ~ modified   → moved
        ↓
re-scan only the changed files + their direct neighbors (token-cheap)
        ↓
emit: 1) text delta summary   2) one delta diagram   3) quality report
```

Steps for the agent:

1. **Scope the diff.** `git diff --name-status $(git merge-base HEAD main)..HEAD`
   (fall back to `git diff --name-status` for uncommitted work, or `git diff
   <base>...<head>` when the user names a base). Deleted files are `D`, added `A`,
   modified `M`, renamed `R`.
2. **Map files to modules** using the manifests and tree (Step 2 of `SKILL.md`).
   A module is *affected* when one of its files changed, or when a changed import/
   route/config edge points at it.
3. **Classify.** `A` → new node (+). `D` → removed node (-). `M` → modified (~) —
   split into `~ interface` (exported API/route/schema changed) vs `~ internals`.
   `R` → moved (→) — keep the same identity, note the new path.
4. **Re-scan the delta only.** Read just the changed files (and their importers for
   `~ interface`) to confirm which *relationships* changed: new edges (→), removed
   edges, or weight changes worth noting.
5. **Render** one diagram + the summary. Run L1/L2 validation before delivering
   (`bash scripts/validate.sh <url>`), and apply the confidentiality rule — the
   labels are the change description itself, which is often the most sensitive part.

## Diagram Encoding Conventions

Use the node/edge grammar from `references/architecture.md` with these conventions:

- **Label prefix marks the delta**: `+ Payment Service` (added), `- Legacy Pay API`
  (removed), `~ Order Service` (modified). Untouched neighbors stay bare so the
  diagram reads as "change in context", not as a full re-architecture.
- **Edge style carries the change**: `main` = new/primary flow, `dash` = removed or
  legacy flow, unstyled = unchanged context.
- Keep the diagram to the affected modules + their immediate neighbors (~15 nodes).
  If the blast radius is bigger, emit a second "impact neighborhood" diagram rather
  than one dense map.
- Grid positions (`r0c1`, …) are optional — auto-layout is fine for small deltas.

## Text Summary Template

```text
Architecture Changes — <repo> (<base>...<commit>, N files)

+ Added:      Payment Service        (src/pay/ — new)
~ Modified:   Order Service          (src/order/api.ts — new outbound call)
- Removed:    Legacy Payment API     (src/legacy/pay.ts)
→ New relationship:  Order Service → Payment Service
→ Dropped:           Order Service → Legacy Payment API

Blast radius: 4 modules · 2 relationships changed
```

## Worked Example (live-tested)

PR: replace a legacy in-process payment call with a new Payment Service behind Kafka.

```text
n=client;fe;Client;;r0c0
n=order;be;~ Order Service;;r0c1
n=paynew;be;+ Payment Service;;r0c2
n=payold;be;- Legacy Pay API;;r1c1
n=kafka;bus;Kafka;;r1c2
n=db;db;PostgreSQL;;r2c1
e=client;order
e=order;paynew;calls;main
e=order;payold;calls;dash
e=paynew;kafka;publishes
e=kafka;db;writes;main
```

URL:

```
https://x-cmd.com/draw/arch2?t=shadcn&title=Order%20flow%20%E2%80%94%20PR%20delta&n=client;fe;Client;;r0c0&n=order;be;~%20Order%20Service;;r0c1&n=paynew;be;%2B%20Payment%20Service;;r0c2&n=payold;be;-%20Legacy%20Pay%20API;;r1c1&n=kafka;bus;Kafka;;r1c2&n=db;db;PostgreSQL;;r2c1&e=client;order&e=order;paynew;calls;main&e=order;payold;calls;dash&e=paynew;kafka;publishes&e=kafka;db;writes;main
```

## Anti-Patterns & Limits

- **Don't re-scan the whole repo** — the point of `impact` mode is to spend tokens
  only on the delta and its neighborhood.
- Don't invent removals: a file that moved (`R`) is `→`, not `-` + `+`.
- Don't draw the delta without context — at least the direct neighbors of changed
  modules, or the diagram is unreviewable.
- `+`/`-` in labels: `+` must be `%2B` in URLs (bare `+` decodes to a space); `-`
  is safe literal.
- The delta classification (`verified`/`inferred`/`unknown`) applies per usual —
  "this PR adds a service" should be verified from the added files, not assumed.
