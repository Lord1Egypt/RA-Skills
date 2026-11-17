# Editorial Extensions (R7 · UX1 · Anti-over-flag)

These are **maintainer additions** on top of the twelve book-grounded risks. Use the same Iron Law.  
For Source line prefer `Editorial — Release Safety` / `Editorial — First-paint UX` unless a classic book truly fits.

## R7 — Release / Supply-chain Safety

**Diagnostic:** Could this change let a user or attacker run untrusted code, leak credentials, or ship an insecure update path *today*?

### Symptoms (non-exhaustive)

- Secrets in repo or scripts: cloud AK/SK, private signing keys, tokens in plaintext.
- Updater / installer: signature verification skipped, missing pubkey, artifacts unsigned while “auto-update” is on.
- Production DevTools / debug features left enabled in release builds.
- CSP `null` / wildly open `connect-src` / `unsafe-eval` in production without documented need.
- Remote download pipelines that pass content directly to a shell in docs/scripts aimed at end users.
- Dependency or plugin allowlists that effectively disable sandboxing for convenience.

### Severity guide

- **Critical** — plaintext cloud/signing secrets; updater skip-verify in shipped config; release build with interactive DevTools.
- **Warning** — CSP missing or far too open; unsigned release channel “temporarily”; debug flags gated poorly.
- **Suggestion** — docs still showing insecure sample commands; dual unused pubkeys causing foot-guns.

### What not to flag

- Local `tauri:dev` / debug feature flags clearly scoped to development.
- Test fixtures with fake keys labeled as such.
- Security work tracked but intentionally deferred with a visible ticket — note tradeoff, don’t Critical-spam.

---

## UX1 — First-paint / Status Clarity

**Diagnostic:** In the first seconds after open (or primary state change), does the user see a coherent status — or empty chrome / lying copy?

### Symptoms

- Splash or loading UI stuck to a corner / zero-height flex parent; solid brand-color empty window for seconds.
- “Loading / 校验中” state that can never appear (dead field always false).
- Status label disagrees with enforcement (UI says licensed; gates treat as free — or the reverse).
- Blocking modal that appears before any readable context.

### Severity guide

- **Critical** — rare; only if users cannot proceed at all with no feedback (hard stuck blank).
- **Warning** — empty first paint lasting seconds; loading/status lies systematically.
- **Suggestion** — minor mis-centering; copy polish.

### What not to flag

- Intentionally minimal splash with centered content that works.
- Skeleton loaders that are clearly loading.

---

## Anti-over-flag (apply before raising R1 especially)

1. Line-count / nesting thresholds are **hints** — require mixed abstraction levels or branch density for Warning+.
2. **UI markup** (large JSX/SwiftUI view bodies that are mostly layout): default Suggestion or skip unless business rules are embedded.
3. **Generated / obfuscated / vendor** paths: skip (note in Scope).
4. One-off scripts and installers: prefer R7 over R1 style nits.
5. If unsure between Warning and Suggestion, choose Suggestion and state the uncertainty once.
