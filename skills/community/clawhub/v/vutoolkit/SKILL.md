---
name: vutoolkit
description: Universal toolkit for Vanderbilt student life - OneVU SSO and
  passkey sessions, what-if grades, YES tools; built for AI agents first.
license: MIT
---

# vutoolkit

Use vutoolkit for an authorized student's Vanderbilt authentication, academic record, GPA projections, degree and schedule planning, and Microsoft Graph access. Prefer its existing session and API operations over rebuilding login flows.

## Runtime prerequisite

This skill supplies instructions, not the runtime or credentials. First check whether the host already exposes `vutoolkit_*` tools or the `vutoolkit` MCP server. If not, follow the [source installation guide](https://github.com/GoatInAHat/vutoolkit#quick-start-from-source); installing this skill alone does not register the plugin. Do not assume an npm or ClawHub plugin package exists merely because an install command was generated. Verify the chosen release and the host's registered tools before using it.

## Workflow

1. Use the current host's account and secret vault. Keep different people's accounts in separate host vaults and data directories. `setup.status` reports configuration/browser prerequisites, not live acceptance of a passkey. A structurally valid key may still be rejected by OneVU.
2. For GPA planning, call `record.fetch`, then pass the returned transcript to `gpa.verify`. Only describe a projection as verified when the official posted totals match; the default synthetic fixture does not verify a real student's record. Pass that same transcript to `grades.whatif` with the requested hypothetical grades.
3. For Microsoft data, use `graph.call` with the smallest read that answers the request. Confirm the account identity with `/me` when validating a new installation. Use POST, PATCH, PUT, or DELETE only for actions authorized by the account holder.
4. If authentication fails, report the typed error and the missing setup prerequisite. Do not claim a live check passed because a fixture or cached metadata call succeeded.
5. For degree planning, start from `degree.audit` or `degree.graph`, retrieve official alternatives with `degree.options`, and use catalog metadata with `planner.graph`. Preserve unknown prerequisites and truncation warnings; never equate a ranked path with official eligibility.
6. For scheduling, fetch live sections with `courses.sections`, then use `scheduler.solve`. Check TBA times, component compatibility, and term before using a result. `scheduler.cartPlan` only returns a diff; the YES extension applies user-selected cart changes, never enrollment.
7. For first-time setup, prefer one call to `setup.run({"confirm":true})` after the account holder authorizes connecting their account. If identity is missing, configure only non-secret email/VUnetID with `setup.identity`, then retry. The operation reuses authenticated browser state or deterministically submits identity and optional `VANDERBILT_PASSWORD` from the host vault; do not drive a custom login or cookie-harvest loop. Never ask for passwords or codes in chat.
8. Respect typed prerequisite errors. `PASSWORD_REQUIRED` means configure the named vault entry through a secure host UI or use `setup.prepare` for manual sign-in, then retry. `MFA_REQUIRED` means wait for the existing one-time approval, not generate repeated pushes. `BROWSER_UNAVAILABLE` means repair the selected compatible CDP browser/connection; never silently switch an explicit endpoint to another profile.
9. For an asleep/unavailable account holder use `allowInteractiveVerification:false`. It reuses existing authentication without submitting a password or initiating phone verification. If no authenticated session is available, preserve progress and report the blocker; do not wake the user or call cookie-only access complete.
10. A known-rejected toolkit key requires explicit recovery authorization and `recovery:true`; the rejected key is not retried and is preserved as `VANDERBILT_PASSKEY_PREVIOUS` only after a new credential is verified. A distinct pending credential blocks duplicate enrollment. `status:"partial"` is not full setup: check `microsoftSession` and repair that connection separately. Successful cached-session access alone does not independently test a passkey assertion.

## Boundaries

- Keep passkeys, cookie payloads, and tokens out of chat, logs, commits, and public test reports. `sessions.open` intentionally returns usable authentication material; pass it directly to the authorized client instead of quoting it.
- Default to read-only live verification. Do not send test email, change enrollment, or alter remote records merely to demonstrate access.
- Use the requested person's own Vanderbilt account. Installing the plugin does not configure their account or authorize reuse of another person's session.
- Consult the [feature acceptance record](https://github.com/GoatInAHat/vutoolkit/blob/main/docs/ACCEPTANCE.md) for evidence and remaining limits. Generated surface coverage does not establish live feature coverage. Fresh passkey creation and real cart writes are not part of the read-only live suite.

Report the operation, runtime version, whether the result was live or synthetic, and any unresolved limitation. Keep private records out of the summary.

<!-- tf:operations -->
## Operations

### courses.detail

Read official YES course description and prerequisite text, preserving ambiguous prose as unknown instead of guessing. Course ID and offer number come from courses.search or the official planner.

Arguments: `id`, `offerNumber`.

`vutoolkit courses.detail --json '<arguments>'` prints a JSON result. MCP tool `courses.detail` on server `vutoolkit` returns the same result as `structuredContent`.

### courses.search

Search the live YES catalog for course IDs, titles, schools and typical offerings. Vanderbilt's keyword search can return broad matches; select by returned course code.

Arguments: `keywords`.

`vutoolkit courses.search --json '<arguments>'` prints a JSON result. MCP tool `courses.search` on server `vutoolkit` returns the same result as `structuredContent`.

### courses.sections

Read live YES section alternatives with campus-local meeting times, professor, room, availability and lecture/lab component. Missing or TBA times are explicit. No cart/enrollment changes.

Arguments: `keywords`, `termCode`.

`vutoolkit courses.sections --json '<arguments>'` prints a JSON result. MCP tool `courses.sections` on server `vutoolkit` returns the same result as `structuredContent`.

### degree.audit

Read Vanderbilt's official degree-audit requirement groups, status, counters and existing planner courses. No audit refresh, enrollment or planner mutation; report timestamps are preserved.

`vutoolkit degree.audit --json '<arguments>'` prints a JSON result. MCP tool `degree.audit` on server `vutoolkit` returns the same result as `structuredContent`.

### degree.graph

Build a directed graph from the authenticated student's official YES audit, including all current requirement groups/lines, satisfying courses and optional planner courses. Official course alternatives load separately via degree.options; this does not invent degree rules.

`vutoolkit degree.graph --json '<arguments>'` prints a JSON result. MCP tool `degree.graph` on server `vutoolkit` returns the same result as `structuredContent`.

### degree.options

Read all official course satisfiers for one current degree-audit requirement line. Report and entry IDs come from degree.audit/degree.graph; the student identity is resolved internally from the authenticated audit.

Arguments: `reportSequence`, `entrySequence`.

`vutoolkit degree.options --json '<arguments>'` prints a JSON result. MCP tool `degree.options` on server `vutoolkit` returns the same result as `structuredContent`.

### gpa.verify

The golden anchor: recompute term and cumulative GPAs from posted marks and compare against Vanderbilt's independent posted totals. Missing cumulative anchors are explicitly unverified. Run before trusting any what-if output. Defaults to the synthetic fixture; pass a live transcript to verify the real YES mapping.

Arguments: `transcript`.

`vutoolkit gpa.verify --json '<arguments>'` prints a JSON result. MCP tool `gpa.verify` on server `vutoolkit` returns the same result as `structuredContent`.

### grades.whatif

Pure GPA projection: apply hypothetical grades onto a transcript (replaces posted grades, fills unposted ones) and report per-term and cumulative GPAs.

Arguments: `transcript`, `hypotheticals`.

`vutoolkit grades.whatif --json '<arguments>'` prints a JSON result. MCP tool `grades.whatif` on server `vutoolkit` returns the same result as `structuredContent`.

### graph.call

Call Microsoft Graph as the student with zero-step auth: the vaulted Microsoft session's Entra cookies silently mint a Graph token (no browser, no interaction; cached ~1h, re-minted on demand). path is a v1.0 path like /me or /me/mailFolders/inbox/messages; query carries OData parameters (for example {"$top": 10, "$select": "subject,from"}). GETs are reads; POST/PATCH/PUT/DELETE change the real mailbox and calendar - reserve them for approved actions.

Arguments: `method`, `path`, `query`, `body`.

`vutoolkit graph.call --json '<arguments>'` prints a JSON result. MCP tool `graph.call` on server `vutoolkit` returns the same result as `structuredContent`.

### planner.graph

Deterministically rank paths for supplied official requirement alternatives and/or course goals. Shared prerequisites count once; completed and planned work is factored in. Unknown prose, missing metadata, cycles and truncation remain explicit. A model-optimal result is exhaustive only for supplied inputs; degree.audit remains the official authority.

Arguments: `courses`, `completed`, `planned`, `goals`, `requirements`, `preferences`, `maxAlternatives`.

`vutoolkit planner.graph --json '<arguments>'` prints a JSON result. MCP tool `planner.graph` on server `vutoolkit` returns the same result as `structuredContent`.

### professors.search

Look up public Vanderbilt Rate My Professors candidates and ratings. Preserves namesake ambiguity; no Vanderbilt credentials leave the toolkit.

Arguments: `name`.

`vutoolkit professors.search --json '<arguments>'` prints a JSON result. MCP tool `professors.search` on server `vutoolkit` returns the same result as `structuredContent`.

### record.fetch

The YES academic record: posted terms plus in-progress unposted courses. Fixture mode for development and tests; live mode rides the cached vanderbilt session through the aai OIDC dance (mints one via the OneVU ceremony over CDP when the vault is empty) — zero manual steps.

Arguments: `fixturePath`.

`vutoolkit record.fetch --json '<arguments>'` prints a JSON result. MCP tool `record.fetch` on server `vutoolkit` returns the same result as `structuredContent`.

### scheduler.cartPlan

Pure cart-only add/remove diff for a selected schedule. Unselected or unrelated courses are retained by default. Does not execute any requests or alter enrollment.

Arguments: `currentIds`, `chosen`, `candidates`, `keepExcluded`, `preserveSectionIds`.

`vutoolkit scheduler.cartPlan --json '<arguments>'` prints a JSON result. MCP tool `scheduler.cartPlan` on server `vutoolkit` returns the same result as `structuredContent`.

### scheduler.solve

Enumerate conflict-free section combinations; include labs, multiple meetings, course exclusions and preferred break times. Deterministic preference ranking and explicit truncation/TBA uncertainty. Returns choices, never enrollment actions.

Arguments: `sections`, `excludedCourses`, `excludedSectionIds`, `blockedTimes`, `hidePreferenceConflicts`, `limit`, `maxSearchNodes`.

`vutoolkit scheduler.solve --json '<arguments>'` prints a JSON result. MCP tool `scheduler.solve` on server `vutoolkit` returns the same result as `structuredContent`.

### sessions.ensure

Zero-step auth: return the cached session for the IdP, or mint a fresh one over CDP and cache it — OneVU passkey ceremony for vanderbilt, Entra-carry (identifier-first + KMSI fallback) for microsoft. Secrets resolve from the OpenClaw vault (VANDERBILT_EMAIL, VANDERBILT_PASSKEY) or VUTOOLKIT_VU_EMAIL / VUTOOLKIT_PASSKEY_JSON / VUTOOLKIT_CDP_URL env overrides. The browser is driven in its own tab, so a shared managed browser is never disturbed.

Arguments: `idp`.

`vutoolkit sessions.ensure --json '<arguments>'` prints a JSON result. MCP tool `sessions.ensure` on server `vutoolkit` returns the same result as `structuredContent`.

### sessions.forget

Drop a cached session: removes its row (metadata and values) from the session vault.

Arguments: `idp`.

`vutoolkit sessions.forget --json '<arguments>'` prints a JSON result. MCP tool `sessions.forget` on server `vutoolkit` returns the same result as `structuredContent`.

### sessions.ingest

Ingest a harvested browser cookie export into the session vault: keeps only cookies in the IdP's domain scope, stores values under the tool data dir (0600), and reports metadata only. The harvest itself is produced by the host browser outside this toolkit.

Arguments: `idp`, `sourcePath`.

`vutoolkit sessions.ingest --json '<arguments>'` prints a JSON result. MCP tool `sessions.ingest` on server `vutoolkit` returns the same result as `structuredContent`.

### sessions.list

Cached Vanderbilt SSO and Microsoft sessions: metadata only (idp, acquired, expiry, health). Session values never leave the vault.

`vutoolkit sessions.list --json '<arguments>'` prints a JSON result. MCP tool `sessions.list` on server `vutoolkit` returns the same result as `structuredContent`.

### sessions.open

Injection payload for a stored session: raw Cookie header, CDP Network.setCookie params, or Playwright storageState. Values resolve from the session vault fed by sessions.ingest; never logged, never echoed anywhere else.

Arguments: `idp`, `format`.

`vutoolkit sessions.open --json '<arguments>'` prints a JSON result. MCP tool `sessions.open` on server `vutoolkit` returns the same result as `structuredContent`.

### sessions.refresh

Force re-mint: forget the cached session for the IdP and run its ceremony again (OneVU passkey over CDP, or the Microsoft Entra carry) — auth stays invisible even when a session goes stale or unhealthy.

Arguments: `idp`.

`vutoolkit sessions.refresh --json '<arguments>'` prints a JSON result. MCP tool `sessions.refresh` on server `vutoolkit` returns the same result as `structuredContent`.

### setup.enroll

Issue a toolkit passkey through OneVU's security-method enrollment. Requires authenticated managed-browser sign-in and explicit account-holder confirmation. For recovery only, replaceExisting=true stages and vault-verifies the newly issued credential, preserves the prior key in VANDERBILT_PASSKEY_PREVIOUS, then promotes the new key; use only after the account holder reports the current toolkit key was rejected and confirms the browser is signed into their own configured account. Never accepts secrets in arguments or revokes OneVU passkeys. Returns metadata only.

Arguments: `confirm`, `replaceExisting`, `timeoutSeconds`.

`vutoolkit setup.enroll --json '<arguments>'` prints a JSON result. MCP tool `setup.enroll` on server `vutoolkit` returns the same result as `structuredContent`.

### setup.identity

Configure the account's non-secret Vanderbilt email and/or VUnetID in the native host vault. A VUnetID alone supplies its Vanderbilt sign-in address. Never accepts passwords or passkeys. Refuses to change an identity while an existing passkey is bound to another account.

Arguments: `email`, `vunetId`.

`vutoolkit setup.identity --json '<arguments>'` prints a JSON result. MCP tool `setup.identity` on server `vutoolkit` returns the same result as `structuredContent`.

### setup.prepare

Prepare a dedicated OneVU tab for the account holder to sign in. Normal setup may load the configured toolkit passkey; recovery=true deliberately does not load or retry the rejected key and requires the holder to use their usual sign-in method. Does not issue or change credentials. The visible page must match the configured student's email before enrollment.

Arguments: `keepTab`, `recovery`.

`vutoolkit setup.prepare --json '<arguments>'` prints a JSON result. MCP tool `setup.prepare` on server `vutoolkit` returns the same result as `structuredContent`.

### setup.run

Deterministic one-call Vanderbilt setup or explicit passkey recovery. Uses this host's configured identity and optional vaulted VANDERBILT_PASSWORD, first reusing an authenticated browser session. On first-time setup it enrolls and vault-verifies a new OneVU passkey, then establishes Vanderbilt and Microsoft sessions. status=partial means Vanderbilt is ready but Microsoft is not; do not claim full setup. Existing valid keys are reused, never rotated. recovery=true skips a rejected key and preserves it as a vault backup. With allowInteractiveVerification=false, setup does not submit a password or click a verification factor; OneVU may still require step-up for enrollment. Returns no credentials. Typed errors tell the caller what prerequisite or one-time verification is missing.

Arguments: `confirm`, `recovery`, `allowInteractiveVerification`, `timeoutSeconds`.

`vutoolkit setup.run --json '<arguments>'` prints a JSON result. MCP tool `setup.run` on server `vutoolkit` returns the same result as `structuredContent`.

### setup.status

Check Vanderbilt account setup without returning credentials: configured identity, structural passkey validity, managed-browser availability and the next step. Structural validity does not prove OneVU accepts the key.

`vutoolkit setup.status --json '<arguments>'` prints a JSON result. MCP tool `setup.status` on server `vutoolkit` returns the same result as `structuredContent`.

### web

Open this tool's web app: serves the operations page and the MCP endpoint on a free local port, opens a browser there, and returns the URL.

`vutoolkit web --json '<arguments>'` prints a JSON result. MCP tool `web` on server `vutoolkit` returns the same result as `structuredContent`.

<!-- /tf:operations -->
