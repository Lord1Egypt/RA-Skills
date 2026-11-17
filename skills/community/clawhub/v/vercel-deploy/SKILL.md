---
name: vercel-deploy
description: Fix Vercel deploys that fail quietly — BLOCKED prod, vercel.json errors, static-export 404s, 4.5 MB limit. Use when a deploy shows UNKNOWN or Error, or the old site stays live.
metadata: {"clawdbot":{"emoji":"▲","requires":{"bins":["vercel","curl","python3"]},"homepage":"https://vercel.com/docs"}}
---

# Vercel Deploy — Diagnose the Deploy, Not the Cache

A Vercel failure rarely looks like a failure. The previous deployment keeps serving, the CLI prints `UNKNOWN`, the config is valid JSON, the build passes locally. **Read the deployment's `state` from the API before touching anything else.** Facts below are either from the official docs (checked 2026-09-30) or marked *observed* with the date and CLI version. Vercel changes fast: re-check an observed fact before building on it.

## When to Use

| Trigger | Action |
|---|---|
| "prod deploy stuck", CLI shows `UNKNOWN` | §1 API state → `BLOCKED` branch |
| "I pushed, the site didn't change" | §1 API state → `ERROR` → §2 vercel.json check |
| "`/page.html` is 404 on Vercel but the file is in `public/`" | §3 static export |
| "my rewrite does nothing" | §3 — rewrites are a no-op on a Next.js static export |
| `413 FUNCTION_PAYLOAD_TOO_LARGE`, webhook never reaches the route | §4 relay |
| "DNS switched but I still see the old host" | §5 verify outside the local resolver |
| "`npm i -g` worked but the CLI won't start" | §6 |

## Access and data

| Item | What this skill needs |
|---|---|
| Credentials | `VERCEL_TOKEN`: an access token you create in the Vercel dashboard, scoped to the one team. Env var only; §1 passes it to curl on stdin, never in argv (visible in `ps`). Never committed. |
| Network out | `api.vercel.com` (read-only GET), `openapi.vercel.sh` (schema), a DoH resolver. The §4 relay also calls **your** forward URL. |
| Data persisted | Only the §4 relay: raw webhook events in `SPOOL_DIR` until a 2xx forward, then deleted. If events carry personal data (emails, names), you need a legal basis, keep only the fields you forward, and purge `*.bad` quarantine files on a schedule you set (suggested: 7 days). |
| Writes | None in §1-§3, §5. Every deploy command is run by you, not by this skill. |

## 1. Read the real state (API, not `vercel ls`)

```bash
# Last N deployments of a project, straight from the API. Refuses on any doubt.
: "${VERCEL_TOKEN:?set VERCEL_TOKEN}" "${VERCEL_PROJECT:?set VERCEL_PROJECT (id or name)}"
q="projectId=${VERCEL_PROJECT}&limit=${N:-5}${VERCEL_TEAM_ID:+&teamId=$VERCEL_TEAM_ID}"
printf 'Authorization: Bearer %s\n' "$VERCEL_TOKEN" |   # builtin: token stays out of ps
  curl -sS --max-time 20 -H @- "https://api.vercel.com/v7/deployments?$q" | python3 -c '
import json, sys
try:
    d = json.load(sys.stdin)
except ValueError:
    sys.exit("REFUSE: API returned non-JSON (network? proxy?)")
if not isinstance(d, dict) or "deployments" not in d:
    sys.exit(f"REFUSE: API error: {json.dumps(d)[:300]}")
if not d["deployments"]:
    sys.exit("REFUSE: 0 deployments - wrong project id/name or wrong team scope")
for x in d["deployments"]:
    m = x.get("meta") or {}
    print(x.get("state"), x.get("target") or "preview", x.get("source"),
          "prebuilt" if x.get("prebuilt") else "remote-build",
          "author=" + str(m.get("githubCommitAuthorLogin") or m.get("gitCommitAuthorName") or "-"),
          "block=" + str((x.get("seatBlock") or {}).get("blockCode", "-")),
          "err=" + str(x.get("errorMessage") or "-"), x.get("url"))
'
# Output: READY production cli remote-build author=jdoe block=- err=- my-app-abc123.vercel.app
# Output (bad token): REFUSE: API error: {"error": {"code": "forbidden", ... "invalidToken": true}}
```

`projectId` and `orgId` (= team id) are in `.vercel/project.json` after `vercel link`. Docs list the endpoint as `GET /v7/deployments`; `/v6` still answered with the same fields (*observed 2026-09-30*).

| `state` | Meaning | Go to |
|---|---|---|
| `BLOCKED` | Never built. No logs, no alias. | §1a |
| `ERROR` | Build or config rejected; the previous READY deploy keeps serving | `err=`, then §2 |
| `READY` but site unchanged | Deploy is fine; the alias or DNS is not | §5 |
| `QUEUED` / `BUILDING` | Still in progress | re-read the API; do not redeploy on top |

**`vercel ls` hides the status column from pipes** (*observed 2026-09-30, CLI 59.10.0*): in a non-TTY, stdout carries only the deployment URLs; the table with **Status** goes to stderr. `vercel ls 2>/dev/null` therefore shows no state at all. Use `2>&1`, or better, the API.

### 1a. `BLOCKED`: the commit author is not in the team

*Observed 2026-09, Pro team, CLI 54 and 59.* `vercel deploy` run inside a git checkout sends the HEAD commit metadata (`meta.githubCommit*` / `gitCommit*`) **even when the project has no Git connection**. If that author is not a team member (typical: an agent committing under its own identity), a remote-build **production** deploy ends `BLOCKED` with *"The deployment was blocked because the commit author doesn't have permission to create deployments for this project"*. The CLI prints `UNKNOWN`, which reads like a slow build.

`BLOCKED` is an **authorization decision**, not a bug. Do not route around it: no alternate deploy mode, no stripped repository copy, no rewritten author. **STOP and hand to a human** who owns the team. Authorized fixes, in order:

1. Invite the commit author to the team (a human owner decides; seat cost applies).
2. Make agent commits under an identity that is already a team member **and** that the owner has approved for automated deploys.
3. Deploy from an approved CI or service identity (Git integration or a team-scoped token issued for that purpose).

Preview deploys by the same author are not blocked, so a preview is a safe way to confirm the build itself is fine while waiting for the owner.

The documented rule (docs, *Deploying private Git repositories*) covers Git-connected private repos in GitHub orgs, GitLab groups and non-personal Bitbucket workspaces — **not** collaborators on personal accounts. The CLI case above is not documented.

## 2. `vercel.json` rejected while the JSON is valid

The schema at `https://openapi.vercel.sh/vercel.json` sets `additionalProperties: false` at the root (checked 2026-09-30). A comment key like `"//": "why"` is valid JSON, passes `next build` locally, and makes the **deployment** fail (*observed 2026-09*). Meanwhile the old deploy keeps serving, so it looks like a cache problem. No comments in `vercel.json`: put the why in the commit message.

```bash
# vercel.json root-key check: exit 0 only when every root key is in the live schema.
python3 - "${1:-vercel.json}" <<'PY'
import json, sys, urllib.request
path = sys.argv[1]
try:
    raw = open(path, encoding="utf-8").read()
except OSError as e:
    sys.exit(f"REFUSE: cannot read {path}: {e.strerror}")
if not raw.strip():
    sys.exit(f"REFUSE: {path} is empty")
try:
    cfg = json.loads(raw)
except ValueError as e:
    sys.exit(f"REFUSE: {path} is not JSON: {e}")
if not isinstance(cfg, dict):
    sys.exit(f"REFUSE: root is {type(cfg).__name__}, expected object")
try:
    with urllib.request.urlopen("https://openapi.vercel.sh/vercel.json", timeout=15) as r:
        allowed = set(json.load(r)["properties"])
except Exception as e:
    sys.exit(f"REFUSE: schema unavailable ({e}); cannot vouch for {path}")
if not allowed:
    sys.exit("REFUSE: schema has no properties; cannot vouch")
bad = sorted(set(cfg) - allowed)
if bad:
    sys.exit(f"FAIL: unknown root keys {bad} -> deployment will error")
print(f"OK: {len(cfg)} root keys, all in schema")
PY
# Output: FAIL: unknown root keys ['//'] -> deployment will error
```

It refuses (exit 1) on a missing, empty, non-object or non-JSON file, and when the schema cannot be fetched: no network means no verdict, never a green. It checks root keys only; nested mistakes still surface as `state: ERROR`.

## 3. Next.js `output: 'export'` routing

| Symptom | Cause | Fix |
|---|---|---|
| `rewrites` / `redirects` / `headers` in `next.config` do nothing | Unsupported with `output: 'export'` (Next.js docs, *Static Exports → Unsupported Features*) | Move redirects to `vercel.json` |
| `rewrites` in `vercel.json` do nothing, build passes | *Observed 2026-09:* on a Next.js project, `vercel.json` rewrites were ignored; only its `redirects` answered in production | Accept a visible redirect; the original URL cannot be kept |
| `public/page.html` → 404 at `/page.html`, 200 at `/page/` | `trailingSlash: true` (*observed 2026-09*) — any `.html` link already sent (email, PDF) breaks | Redirect `/page.html` → `/page/` in `vercel.json` |
| Redirect answers 308, you needed 301 | `"permanent": true` = 308, `false` = 307 (docs) | `"statusCode": 301` — and drop `permanent`: the two cannot be combined |

```json
{ "redirects": [ { "source": "/page.html", "destination": "/page/", "statusCode": 301 } ] }
```

```bash
curl -sI https://my-app.example.com/page.html | head -3
# Output: HTTP/2 301   (then: location: /page/)
```

## 4. `413 FUNCTION_PAYLOAD_TOO_LARGE`: the route never runs

Request **and** response bodies of a Vercel Function are capped at **4.5 MB** (docs, *Functions Limits*, checked 2026-09-30). Vercel's own guide: upload large request bodies straight to storage, stream large responses. For a **webhook you do not control** (inbound email with pasted screenshots: Gmail inlines them as base64, 2-3 captures is enough), your handler never executes and the event is lost unless the sender retries (*observed 2026-07*: lost silently, nothing in the app logs). Raising a size guard in your own code changes nothing.

The fix is a relay on a host without that cap. Four rules, each learned from a failure:

| Rule | Why |
|---|---|
| Verify the signature on the **raw bytes**, before any JSON parsing | A re-serialized body no longer matches the signature |
| Write the event to disk **before** acking | Ack-then-forward with no spool loses the event on the first forward failure or restart, silently |
| Delete the spool file only after a 2xx from the target | The spool is the replay queue; a crash mid-forward replays instead of dropping |
| If the event arrives **without** its body, refetch by id from the provider API | *Observed 2026-07:* an inbound-email provider omitted `text`/`html` on large messages while small ones carried them |

Reference relay (svix-signed webhooks; Node ≥ 18, `npm i express svix`). Tested on hostile fixtures: missing env, `http://` non-loopback target, `localhost.evil.com`, empty body, tampered body, wrong signature, 1 h-old replayed signature, signed non-object JSON, `../` in the event id, corrupt spool file, target down then up, 6 MB event.

```js
"use strict";
// Webhook relay: verify on raw bytes, spool to disk, ack, then forward a small JSON.
const fs = require("fs"), path = require("path"), express = require("express");
const { Webhook } = require("svix");
const { WEBHOOK_SECRET, FORWARD_URL = "", FORWARD_SECRET, SPOOL_DIR = "./spool", PORT = 3000 } = process.env;
const LOOPBACK = /^http:\/\/(127\.0\.0\.1|localhost)(:\d+)?\//;
if (!WEBHOOK_SECRET || !FORWARD_SECRET || !(FORWARD_URL.startsWith("https://") || LOOPBACK.test(FORWARD_URL))) {
  console.error("refusing to start: WEBHOOK_SECRET, FORWARD_SECRET, https FORWARD_URL required");
  process.exit(2);
}
fs.mkdirSync(SPOOL_DIR, { recursive: true, mode: 0o700 });
const wh = new Webhook(WEBHOOK_SECRET);
// Replace with your extraction. If the provider omitted the body (large messages),
// refetch it here from the provider API by event id before shrinking.
async function toSmallPayload(event) {
  const d = (event && event.data) || {};
  const text = typeof d.text === "string" ? d.text : "";
  return { id: String(d.id || ""), subject: String(d.subject || "(no subject)").slice(0, 500), text: text.slice(0, 50000) };
}
const app = express();
app.post("/hook", express.raw({ type: "*/*", limit: "35mb" }), (req, res) => {
  if (!Buffer.isBuffer(req.body) || req.body.length === 0) return res.status(400).json({ error: "empty_body" });
  const raw = req.body.toString("utf8");
  try {
    wh.verify(raw, { "svix-id": req.header("svix-id") || "",   // throws on any mismatch;
      "svix-timestamp": req.header("svix-timestamp") || "",     // its return value varies by
      "svix-signature": req.header("svix-signature") || "" });  // svix version: never use it
  } catch { return res.status(401).json({ error: "invalid_signature" }); }
  let event;
  try { event = JSON.parse(raw); } catch { return res.status(400).json({ error: "bad_json" }); }
  if (!event || typeof event !== "object") return res.status(400).json({ error: "bad_json" });
  const id = String(req.header("svix-id")).replace(/[^A-Za-z0-9_-]/g, "").slice(0, 100);
  if (!id) return res.status(400).json({ error: "bad_id" });
  const file = path.join(SPOOL_DIR, `${id}.json`);          // same id = provider retry = overwrite
  fs.writeFileSync(`${file}.tmp`, JSON.stringify(event));
  fs.renameSync(`${file}.tmp`, file);                        // on disk BEFORE the ack
  res.status(202).json({ queued: id });
  drain();
});
let draining = false;
async function drain() {
  if (draining) return;
  draining = true;
  try {
    for (const f of fs.readdirSync(SPOOL_DIR).filter((n) => n.endsWith(".json")).sort()) {
      const p = path.join(SPOOL_DIR, f);
      let event;
      try { event = JSON.parse(fs.readFileSync(p, "utf8")); }
      catch { fs.renameSync(p, `${p}.bad`); console.error(`quarantined ${f}`); continue; }
      const r = await fetch(FORWARD_URL, {
        method: "POST", signal: AbortSignal.timeout(20000),
        headers: { "content-type": "application/json", "x-webhook-secret": FORWARD_SECRET },
        body: JSON.stringify(await toSmallPayload(event)) });
      if (!r.ok) throw new Error(`forward ${r.status} on ${f}`);
      fs.unlinkSync(p);                                       // delete only after a 2xx
    }
  } catch (e) { console.error("drain paused:", e.message); }
  finally { draining = false; }
}
setInterval(drain, 60_000);
drain();
app.listen(PORT, () => console.log(`relay on :${PORT}`));
```

`svix` 2.6.0 `verify()` returned `undefined` on success in testing (2026-09-30): code that used its return value as the event wrote nothing and threw. Parse `raw` yourself, as above. The spool must be on a **persistent volume**; an ephemeral container disk turns "spooled" back into "lost". Point the provider's webhook at the relay only after one signed test event has reached the target.

## 5. DNS cutover: prove it outside your resolver

*Observed 2026-09:* some networks intercept outbound DNS (UDP **and** TCP; `+tcp` changes nothing) and answer `dig @ns1.example-dns.com` from a cache, serving the **old** zone. Signs: `flags: qr ra` with no `aa`, a TTL that decrements between queries.

```bash
dig +norec example.com @<authoritative-ns> | grep flags   # authoritative answer carries "aa"
curl -sS -H 'accept: application/dns-json' 'https://cloudflare-dns.com/dns-query?name=example.com&type=A'
curl -sS 'https://dns.google/resolve?name=example.com&type=NS'
curl -sSI --resolve example.com:443:<ip-from-DoH> https://example.com | head -1   # what the new host serves
```

`SSL_ERROR_SYSCALL` on the `--resolve` test before Vercel has issued the certificate is a certificate-not-yet-issued symptom, not a routing failure. `whois` shows registry nameservers without going through DNS.

## 6. Global CLI installs under npm 12

npm 12 blocks dependency install scripts by default (`--allow-scripts <package-list>` exists on npm 12.0.2). The install reports success, and a CLI that downloads its native binary in `postinstall` breaks on first run (*observed 2026-08*: `could not find the CLI binary`). After any `npm i -g`, run `<cli> --version`. If broken: `npm install -g --allow-scripts=<pkg> <pkg>@latest`. `--allow-scripts` is refused on `--prefix` installs; use `allowScripts` in `package.json` or `.npmrc` there.

## Output Format

End every diagnosis with this block:

```
VERCEL DIAGNOSIS
project:   <name>  team: <team-id or personal>
state:     <API state> (target=<production|preview>, source=<cli|git>, build=<remote|prebuilt>)
evidence:  <errorMessage / blockCode / curl status line>
cause:     <one line>
fix:       <exact command or config diff>
verified:  <command re-run after the fix and its output, or "NOT VERIFIED">
```

```
VERCEL DIAGNOSIS
project:   my-app  team: team_example
state:     BLOCKED (target=production, source=cli, build=remote)
evidence:  "commit author doesn't have permission to create deployments"
cause:     HEAD authored by a non-member identity; CLI forwards commit meta
fix:       HUMAN — team owner adds the author or approves a member/CI identity (§1a); preview deploy confirms the build
verified:  NOT VERIFIED (waiting on owner)
```

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| CLI shows `UNKNOWN`, no build logs | `BLOCKED` by commit-author check | §1a |
| Site unchanged after deploy, no error seen | Latest deploy is `ERROR`; old READY still aliased | §1, then §2 |
| §1 prints `0 deployments` | Project name given without `VERCEL_TEAM_ID`, or wrong team | Use ids from `.vercel/project.json` |
| Relay acked, target never got the event | Forward failed with no spool | Spool-before-ack (§4) |

## Scope

This skill ONLY: reads deployment state through the API with a token you supply; checks `vercel.json` against the published schema; proposes routing, redirect and relay fixes; verifies DNS through DoH and `--resolve`; ships one reference relay that refuses to start without secrets and an HTTPS target.

This skill NEVER: deploys to production on its own; works around a `BLOCKED` authorization decision (no prebuilt or stripped-copy deploys to dodge it); changes team membership, tokens or DNS records; prints or commits a token; disables signature checks to "get the webhook through"; acks an event it has not written to disk; reports a fix as done without the re-run in `verified:`.

*Alexandre Bloch — ClawHub @AlexBloch-IA*
