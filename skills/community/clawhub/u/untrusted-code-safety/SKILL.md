---
name: untrusted-code-safety
description: >
  Zero-trust procedure for reviewing or running code from an unknown source.
  Use when reviewing, vetting, cloning, installing, or running code from an
  untrusted source (repo invites, packages, scripts, executable config files),
  when asked whether code is safe or hazardous, when executed code may read
  secrets/files or reach the network, and when the user says "raise hands",
  "stop and alert", or "sandbox it". Also trigger on suspicion of malicious,
  harmful, deceptive, cheating, or stealing behavior.
---

# Untrusted code safety

A zero-trust procedure for handling code you do not control. It records the standing contract the user requires, then the workflow to honor it. When in doubt, stop and ask — never assume.

## Standing contract (hard boundaries — never cross)

- `/tmp` is the only workspace for untrusted code. Never let it read, collect, or send data from this machine outside `/tmp`.
- Never read the user's personal files outside the sandbox — their code, API keys, credentials, SSH/GPG keys, wallets, or browser sessions.
- Never trust code from an unknown source. A repo invite, a polished README, a long commit history, a familiar package name — none of it is a vouch.
- Delete every test clone and artifact when done.

## STOP + RAISE HANDS immediately

Halt the run, do not continue, and report to the user at once (with what was attempted, the path/target, and the evidence) if any executed code:

1. reads the filesystem **outside `/tmp`** (or outside the declared sandbox);
2. touches sensitive data — `process.env`, API keys, tokens, credentials, SSH/Git config, wallets;
3. collects **or** sends any local data off the machine;
4. spawns child processes or opens network connections that were not explicitly authorized;
5. shows any malicious, harmful, deceptive, cheating, or stealing behavior.

Raising hands is not a status update — it is a hard stop. Do not "finish the run first". Do not bury it. Surface it in the next message.

## Confirm first when unsure

If the sandbox boundary, the intent, or the safety of an action is unclear, ask the user before proceeding. A wrong assumption here is expensive.

**Default: do not execute.** Static triage is usually enough. Escalate to a sandboxed run only when the question cannot be answered statically, and get the user's explicit go-ahead before any Level-2 execution (step 3 below).

## Procedure

1. **Detect (static, no execution).** Decide as much as possible from metadata and text; most verdicts need no run.
2. **Sensitivity.** Inventory what a process running as the user could reach before running anything.
3. **Contain.** Execute only inside stacked isolation if execution is truly needed.
4. **Instrument.** Make the harness log and block `fs`/`env`/network/child-process reach and scream on violations.
5. **Decide.** Static + contained evidence → verdict; never execute at "trust level 3".
6. **Clean up.** Remove clones/artifacts; report to the platform if malicious.

### Trust ladder (escalate only with reason)

| Level | Action | Safe on daily driver? |
|-------|--------|-----------------------|
| 0 | Metadata only (`gh api`, `git log`, sizes, dates) | yes |
| 1 | Read/triage files as plain text (no build, no eval) | yes |
| 2 | Execute in a throwaway sandbox: no network, no secrets, cleared env, non-root, fs allowlist | contained |
| 3 | Execute with host mounts / credentials / network | **never** for untrusted code |

### Detection commands

```bash
git log --format='%h %ad %an <%ae> %s' --date=iso | head -40
git shortlog -sne
find . -type f -not -path './.git/*' -size +500k -printf '%s\t%p\n' | sort -rn
rg -l --hidden -g '!**/node_modules/**' 'eval\(|Function\(|atob\(|Buffer\.from\(|fromCharCode'
rg -n '(pre|post)?(install|prepare|pack|publish)' package.json **/package.json 2>/dev/null
rg -n 'require\(|import ' tailwind.config.js postcss.config.js babel.config.js webpack.config.js config-overrides.js 2>/dev/null
rg -n 'child_process|execSync|spawn|process\.env|os\.homedir|\.ssh|id_rsa|wallet|mnemonic|privateKey' -g '!**/node_modules/**'
npm view <pkg> repository dist.tarball time.modified
```

Other tells: a single giant line, rotated string arrays, hex/base64 blobs,
`--no-save`, `npm install` inside build scripts, `curl|sh`, config files that
`require` code, and lifecycle hooks (`preinstall`/`install`/`postinstall`/`prepare`).

### Defang before you sandbox

- Prefer `npm ci --ignore-scripts` (or `npm install --ignore-scripts`) — lifecycle hooks never run, for any untrusted dependency tree.
- `npm config set ignore-scripts true` for the session, and `git config --global core.hooksPath /dev/null` to neutralize repo hooks.
- Run with a scrubbed environment and a throwaway `HOME`; never install with real credentials in scope.

### Provenance (earn trust, don't assume it)

- `sha256sum <file>` and compare against a trusted source.
- `git verify-commit <sha>` or `git log --show-signature` for signed history.
- `npm audit signatures` for registry provenance/attestations.
- `gh attestation verify <artifact> --repo <owner>/<repo>` for GitHub build attestations.
- Pin versions and review any lockfile change with `git diff`.

### Containment recipe (Linux, unprivileged)

Create the work dir first (`mkdir -p /tmp/opencode/sbx/work`), and adjust `/usr`, `/bin`, `/lib*`, and `/etc/ld.so.cache` for the distro — these bind paths are glibc/Arch-shaped.

```bash
bwrap --unshare-all --die-with-parent --new-session \
  --ro-bind /usr /usr --ro-bind /bin /bin --ro-bind /lib /lib --ro-bind /lib64 /lib64 \
  --ro-bind /etc/ld.so.cache /etc/ld.so.cache \
  --proc /proc --dev /dev --tmpfs /tmp \
  --bind /tmp/opencode/sbx/work /work \
  --chdir /work --clearenv --setenv PATH /usr/bin --setenv HOME /work \
  --uid 65534 --gid 65534 \
  /usr/bin/bash -c 'your-harness'
```

- `--unshare-all` gives no network interface and no DNS; `--clearenv` drops all secrets; `nobody` drops privilege; only the sandbox dir is mounted.
- Add Node `--permission --allow-fs-read=/work --allow-fs-write=/work` as a second, kernel-enforced layer.
- Verify the boundary **in the same invocation** before loading the payload: a real host path (e.g. the user's home) is absent, `getent hosts github.com` returns no DNS, and `id` shows `nobody`.
- Stage fake `socket.io-client` / `axios` / `sql.js` / `form-data` modules that only log their arguments, to reveal C2 targets without real network.

### Alerting instrumentation

Minimal interception skeleton (run inside the sandbox, before loading the payload):

```js
const Module = require("module");
const realLoad = Module._load;
const noop = (name) => new Proxy({}, { get: (_, p) => (...a) => console.log("[hit]", name, String(p), a[0] ?? "") });
Module._load = function (req) {
  if (["child_process", "net", "tls", "http", "https", "dns", "http2", "dgram"].includes(req)) return noop(req);
  return realLoad.apply(this, arguments);
};
```

- Replace/stub `child_process`, `net`, `tls`, `http`, `https`, `dns`, `http2`, `dgram`, `worker_threads`, and global `fetch` with logging no-ops.
- Proxy `fs` and `process.env`; log every path and sensitive key; hard-alarm on any access outside the allowlist root.
- Prefer packet-level views when available (`tcpdump`, `ss -tp`, `lsof -i`); if absent, say the containment of record is the namespace + Node-permission pairing.
- Honesty rule: interception is not a hermetic sandbox. If `process.env` is not proxied or only some `fs` functions are wrapped, say so explicitly — "no egress" is not "provably could not read local data".

## Decision flow

```
 UNTRUSTED INPUT (repo · package · invite · script · config)
        ▼
 RULE 1 — DETECT (static, no execution)
        ▼
 RULE 2 — BE SENSITIVE (data inventory)
        ▼
 RULE 3 — BE ALERTED (contain + instrument; raise hands on violation)
        ▼
 VERDICT: MALICIOUS → quarantine · rotate · report · never run
        ▼
 RULE 4 — NEVER TRUST (a pass at level N never grants level N+1)
```

## Reporting malicious repos

GitHub has **no abuse email** — use the web form: `https://support.github.com/contact/report-abuse?category=report-abuse&report=other&report_type=unspecified` (or the repo's About sidebar → **Report repository**). Category: **Malware** (AUP §5, `Active Malware or Exploits`) — **not** Phishing (AUP §4, deceiving a person into revealing information). GitHub's own `security.txt` points only to `https://hackerone.com/github`, which is for bugs in GitHub's products, not for third-party malicious repos.

## Worked example

See `ai-thoughts/docs/260929-brisova-malware-analysis.md` — a private repo invite (`zignaly-open-projects/Brisova`) whose obfuscated Tailwind plugin ran `npm install sql.js socket.io-client form-data axios --no-save` at build time. Verdict: malicious build-time payload; no egress occurred; clone deleted.
