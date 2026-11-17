# Ambient Ride

### What if over 52,000+ NYC drivers were instantly accessible by your AI agent? Introducing 🚕 Ambient Hailing  Your AI agent can now hail a real taxi.

Not a simulation. Not a demo network. A real driver, in a real car, pulling up to your curb, booked and paid for by your agent while you finish your coffee.

**Ambient Hailing** is an open-source skill that connects AI agents to live ride-hailing fleets: **Throo in New York**, **TADA in Singapore**, **TADA in Cambodia** (Phnom Penh, Siem Reap, Sihanoukville, Kampot), and **TADA in Hong Kong**. Install it in Claude Code or OpenClaw, and your agent can search rides, compare fares, book, pay, chat with your driver, and tip, with your explicit approval at every step that matters.

```
You:    "Get me to JFK by 3pm."
Normal Agent:  "Found 3 cars nearby. Fastest is 4 min away, $52, arrives JFK 2:40pm. Book it?"
You:    "Yes."
Normal Agent:  "Booked. Marcus, white Camry, plate T7X-2041. He's 4 minutes out."
```

That's the whole UX. No app. No map-dragging. No surge-price roulette at 7am.

## Why this exists

Apps are just channels. In the agent era, your assistant won't open apps, it will talk to mobility infrastructure directly. We think ride-hailing is the perfect stress test for real-world agent commerce: it's real-time, safety-sensitive, and involves actual money. So we built it, open-sourced it, and connected it to fleets we actually operate.

This is what "agents doing things in the physical world" looks like when it's real.

## Overview

Book TADA/Throo rides through your AI agent — in Claude Code or OpenClaw (Telegram).

All runtime state (encrypted passphrase, ride DB, and wallet keys only if you choose built-in Privy) lives in `~/.amb/state/{data,keys}/` — independent of the skill's install directory since Phase 1. Installation preserves OpenClaw skill entries, Claude settings, and unrelated environment keys.

## Install

Ambient Ride ships through two package registries — pick the one matching your agent.

### Claude Code — via Claude Marketplace (recommended)

```bash
claude plugin marketplace add mvlchain/ambient-ride-plugin
claude plugin install ride@ambient-ride
```

Then, in any project, run `/ride:setup`. Installing a plugin only copies files —
Claude Code has no install-time hook — so `/ride:setup` is what installs the `amb`
CLI the skill drives. You can also skip it and just mention a ride; the skill
installs the CLI on first load.

Both commands install user-level by default. To scope the install to one project
instead, pass `--scope project` to each — it records the marketplace and plugin in
that project's `.claude/settings.json`, so the repo carries them:

```bash
claude plugin marketplace add mvlchain/ambient-ride-plugin --scope project
claude plugin install ride@ambient-ride --scope project
```

`--scope local` keeps the same declaration to your own checkout instead.

> **Internal/dev channel** (MVL operators only): the canonical local marketplace
> clone is `~/Project/easi6/ambient-ride-plugin-dev`, backed by
> `mvlchain/ambient-ride-plugin-dev`. Verify the source build and CLI → skill →
> plugin deployment plan with `scripts/deploy-dev.sh --dry-run`; dry-run never
> mutates a target repository.

### OpenClaw — via ClawHub (recommended)

```bash
openclaw skills install @ambprotocol/ride
```

ClawHub publishes a security audit for each released version. Treat **Pass**,
**Review**, and **Blocked** as distinct outcomes: Review asks the operator to
inspect the findings and is not the same as Pass or a malware verdict; Blocked
must not be bypassed. Installation success alone does not prove that the exact
version passed its audit. Read the public
[security audit](https://clawhub.ai/ambprotocol/skills/ride/security-audit)
before use, because this skill can book physical rides and spend money.

If installation stops on a version-specific policy check, follow the recovery
instruction printed by the installed OpenClaw CLI instead of copying a flag
from documentation for another release.

Restart the gateway:
```bash
openclaw gateway restart
```

Installing only unpacks the bundle — OpenClaw has no post-install hook — so the
skill installs the `amb` CLI itself on first use.

Useful flags: `--version <version>` pins a published version, `--global` installs
into the shared managed skills directory instead of the agent workspace, and
`--agent <id>` targets a specific agent workspace.

### Other agents, or a pinned/manual install

Clone the skill bundle directly and run its installer when a registry install does
not fit — for example:

- you run an agent with no registry of its own (Codex, Hermes, ...), which loads a
  skill from a plain directory;
- you need a specific commit rather than the latest published version.

(A project-scoped Claude Code install does **not** need this — use `--scope project`
above.)

**Claude Code (local checkout)**
```bash
git clone https://github.com/mvlchain/ambient-ride-skill.git .claude/skills/ride
node .claude/skills/ride/scripts/install.js
```

**OpenClaw (manual)**
```bash
git clone https://github.com/mvlchain/ambient-ride-skill.git ~/.openclaw/skills/ride
node ~/.openclaw/skills/ride/scripts/install.js
```

**Any other agent**
```bash
git clone https://github.com/mvlchain/ambient-ride-skill.git <your-agent-skills-dir>/ride
node <your-agent-skills-dir>/ride/scripts/install.js
```

After install completes, restart the agent/runtime so it picks up the new skill.

## What `install.js` does

L1 bootstrap (skill side): fetches the `amb` CLI binary and puts it on `$PATH`. Depending on the build, the CLI is installed one of two ways:

**git builds (dev/staging):**

1. Verifies `~/.local/bin` is on `$PATH` before any bootstrap or migration
   mutation (fatal exit with guidance if not).
2. Creates a transaction-owned sibling staging directory named
   `~/.amb-cli-bootstrap-*` and clones `mvlchain/ambient-ride-cli`
   (dev/staging branch) into its `cli/` child. The live `~/.amb/cli` is not
   updated in place.
3. Runs `npm install --omit=dev` in the staged clone — the CLI's native
   dependencies (`better-sqlite3` and friends) live outside the bundled binary
   and must be resolved separately. (The skill bundle itself has no dependencies
   — its scripts import nothing outside Node's builtins, so nothing is installed
   inside the skill directory.)
4. Verifies the staged binary. On a SHA mismatch, its one automatic retry runs
   `git fetch + reset --hard` only inside that staged clone.
5. After the staged binary has successfully run `amb install`, temporarily moves
   any existing `~/.amb/cli` and `~/.local/bin/amb` symlink to transaction-owned
   `.replaced-*` paths, promotes the staged CLI into `~/.amb/cli`, and creates the
   managed symlink.
6. Verifies that `amb` on `$PATH` resolves to the promoted managed binary.
7. Commits by removing the private transaction marker
   and recursively cleaning only the validated bootstrap and owned replacement
   paths. An interrupted transaction retains a private marker; a later installer
   run validates it and attempts to resume forward when the recorded state can
   be reconciled safely. Unreconcilable, invalid, or mismatched recovery state is
   preserved and fails closed instead of being used.

**npm builds (prod):**

1. Runs `npm i -g @ambprotocol/ride-cli@latest` — npm registers the `amb` binary in its own global bin dir (`npm config get prefix` appended with `/bin`), which is normally already on `$PATH`.
2. Verifies `amb` actually resolves on `$PATH` (fatal exit with guidance to add npm's global bin dir if not).

Then, regardless of mode:

- Calls `amb --version` and checks the baked expected version matches (git: `git_sha`; npm: semver against the baked minimum CLI version) — on mismatch, retries the staged git checkout (`git fetch + reset --hard` inside the bootstrap clone) or `npm i -g` once automatically.

L2 delegation (`amb install`):

1. Creates `~/.amb/state/{data,keys}/`.
2. Generates (if absent) or preserves (if present) `AMB_RIDE_PASSPHRASE`, writing it to `~/.amb/state/data/.env` (mode `0600`). **Existing passphrase is never overwritten** — losing it would brick wallet keys.
3. Migrates legacy state into `~/.amb/` with a validated, backup-first transaction. A completed clean break preserves the legacy tree as `~/.tada.bak`.
4. Preserves OpenClaw skill entries, Claude settings, unrelated environment keys, and secret values while mapping approved legacy runtime values into Ambient state.

No new entries are added to platform config files. Every step is idempotent — re-running skips anything already in place.

On success, stdout emits a single-line JSON: `{"status":"installed" | "already_installed", ...}`. On failure, stderr emits a single-line JSON: `{"error":"<CODE>","message":"..."}`.

## Requirements

- Node.js 22.22.0 or newer (`>=22.22.0`); contributors should use the pinned 22.22.0 runtime via `.node-version` or `nvm install 22.22.0 && nvm use 22.22.0`
- `npm` (ships with Node — git builds invoke `npm install --omit=dev` inside the staged `~/.amb-cli-bootstrap-*/cli/`; npm builds invoke `npm i -g @ambprotocol/ride-cli@latest`)
- `git` — needed to clone this skill bundle for a manual/project-scoped install, and by Claude Code to fetch the plugin marketplace repository; git builds additionally use it to clone `mvlchain/ambient-ride-cli` (npm builds don't)
- The `amb` binary must end up on `$PATH`:
  - **git builds**: `~/.local/bin` must be on `$PATH` — usually automatic on modern Linux/macOS; otherwise add `export PATH="$HOME/.local/bin:$PATH"` to your shell profile and open a new shell
  - **npm builds**: npm's global bin dir (`npm config get prefix` + `/bin`) must be on `$PATH` — normally automatic for any working npm install; otherwise add it to your shell profile and open a new shell

If `better-sqlite3` install fails (corporate proxy / missing build tools):
- If the prebuilt binary cannot be downloaded, build from source: install `apt install build-essential python3` on Linux, Xcode Command Line Tools on macOS, or Visual Studio Build Tools on Windows, then re-run `install.js`.
- Or set an internal mirror: `npm config set better_sqlite3_binary_host_mirror <internal_mirror>` then retry.

For ABI mismatch (`Error: ... NODE_MODULE_VERSION`): make sure a supported Node.js version is active (`node --version`), then `rm -rf ~/.amb/cli && node <SKILL_DIR>/scripts/install.js` (re-clone + re-install). `~/.amb/cli` holds only the CLI itself — your database, keys, and passphrase live under `~/.amb/state/`, which this leaves untouched.

If `npm i -g @ambprotocol/ride-cli` fails with `EACCES`, npm's global prefix is not writable by your user. Do **not** re-run it under `sudo`: the CLI deliberately skips state initialisation when it detects a sudo invocation (it reports `status: "skipped_sudo"`), because root-owned `~/.amb` state would lock you out of your wallet keys. Point npm at a user-writable prefix instead (`npm config set prefix ~/.local`) and make sure that prefix's `bin` directory is on your `$PATH`.

## Install error codes

When `install.js` fails it exits non-zero and writes a single-line JSON to stderr: `{"error":"<CODE>","message":"..."}`. Each code maps to a specific recovery action:

| Code | Meaning | Recovery |
|---|---|---|
| `SSH_KEY_MISSING` | (git builds only) `git clone`/`fetch` failed with an SSH public-key rejection (`Permission denied (publickey)`) | Register your GitHub SSH key (`ssh-add ~/.ssh/id_*`); verify access to the `mvlchain` org with `ssh -T git@github.com`; then re-run `install.js`. |
| `SYMLINK_FAILED` | Cannot write to `~/.local/bin/amb` | `mkdir -p ~/.local/bin` then check write permission (`ls -la ~/.local/bin`); re-run `install.js`. |
| `PATH_MISSING` | `amb` did not resolve on `$PATH` after install. **git builds**: `~/.local/bin` is not on `$PATH`. **npm builds**: npm's global bin dir (`npm config get prefix` + `/bin`) is not on `$PATH` | **git builds**: add `export PATH="$HOME/.local/bin:$PATH"` to your shell profile (`.bashrc` / `.zshrc` / `.profile`). **npm builds**: add npm's global bin dir instead — run `npm config get prefix`, append `/bin`, and add `export PATH="<that dir>:$PATH"` to your shell profile. Either way, open a new shell, then re-run `install.js`. |
| `SHA_MISMATCH` | `amb --version`'s `git_sha` doesn't match the sha baked into this skill bundle, even after one `git fetch + reset --hard` retry | The skill bundle expects a newer CLI than what `mvlchain/ambient-ride-cli` has on its dev/staging branch — usually a transient state during a deploy. Wait a moment and re-run; if it persists, the CLI push lagged or failed and needs operator attention. |
| `VERSION_MISMATCH` | (`'npm'` mode only) `amb --version`'s `version` is below the baked minimum CLI version after one `npm i -g` retry | Run `npm i -g @ambprotocol/ride-cli@latest` manually and re-run `install.js`. If it still fails, your npm prefix may differ — check `npm config get prefix` and verify the registered `amb` binary. |
| `AMB_INSTALL_FAILED` | The `message` field disambiguates: the Node.js runtime is older than 22.22.0, native dependencies did not install, the global npm install failed, `amb install` exited non-zero, or a `git clone`/`fetch` failed for a reason other than an SSH key rejection | Read the `message`: it carries git's own stderr verbatim, including the remedy git suggests (for example `git config --global --add safe.directory <path>` on an ownership mismatch). Otherwise upgrade Node.js when the message reports an unsupported runtime, or check the reported npm/network/native dependency error, then run the installer again. |

`install.js` is idempotent. After fixing the underlying issue, simply re-run it.

## Updating the skill

**Claude Marketplace**: use the fully qualified id (the short name `ride` fails with
`Plugin "ride" not found`):

```bash
claude plugin update ride@ambient-ride
```

Restart Claude Code afterwards — the CLI says so, and it is required for the new bundle
to load. If you installed with `--scope project` (or `local`), pass the same scope here:
`claude plugin update ride@ambient-ride --scope project`.

**ClawHub**: use `skills update` — a plain `skills install` will not overwrite an
already-installed skill (that needs `--force`).

```bash
openclaw skills update @ambprotocol/ride
```

`skills update` runs the same version-specific verdict check as `skills install`.
If the installed OpenClaw CLI requires an acknowledgement for a particular
release, follow the recovery instruction it prints instead of copying a stale
flag from this README.

```bash
openclaw skills update --all
```

updates every tracked ClawHub skill. Add `--global` if you installed into the
shared managed skills directory.

**Pinned/manual install** (see "Other agents, or a pinned/manual install" above):

```bash
cd <install_dir>
git pull
node scripts/install.js   # idempotent — stages/promotes CLI + preserves passphrase + DB + keys
```

`install.js` is safe to re-run and never regenerates an existing passphrase. Git builds verify a fresh staged clone and promote it into `~/.amb/cli`; only a staged SHA-mismatch retry uses `git fetch + reset --hard` inside the transaction-owned bootstrap clone.

## Account modes (TADA/Throo member vs crypto wallet)

After install, the skill operates in one of two account modes. Day to day you don't run these commands yourself — the agent drives onboarding from your answers (see `SKILL.md`) — but this is what happens underneath.

Check the current mode at any time:

```bash
amb whoami     # JSON: { "mode": "tada" | "wallet" | null, "member_available": <bool>, ... }
```

- `mode: "tada"` — signed in to a **TADA/Throo member account**; rides are paid with your registered card and no wallet is required.
- `mode: "wallet"` — **crypto wallet** mode; rides are paid from the wallet.
- `mode: null` — not onboarded yet.

`member_available` reports whether this build ships TADA/Throo member support. When it is `false`, only crypto wallet mode is offered (member commands return `status: "unavailable"`).

`amb install` is non-interactive and does **not** pick a mode or create a wallet. On first use the agent asks whether to use TADA/Throo member card payment, crypto wallet payment, or decide later. Member sign-in goes directly to `amb login --no-wait`; the crypto path asks you to choose Privy or MetaMask before creating or connecting anything.

### Sign in to a TADA/Throo member account

Member sign-in uses the TADA/Throo app (device-flow); there is no CLI password and no wallet is created or required:

```bash
amb login      # interactive: prints an approval link, then prompts for the 4-digit code
```

Open the printed link in the TADA/Throo app, approve it, and the app shows a 4-digit code; enter it when prompted. `amb whoami` then reports `mode: "tada"`.

For non-interactive / agent use, the same flow is split into two calls:

```bash
amb login --no-wait             # → { "status": "auth_required", "approval_url": "…" }
amb login-verify --code <code>  # → { "status": "logged_in" | "invalid_code" | "session_expired" }
```

Sign out of the member account (wallet state is untouched):

```bash
amb logout
```

For crypto wallet setup (Built-in Privy via `amb wallet-setup`, or MetaMask via
`amb wallet-connect-metamask`) and the full ride/tip/chat command surface, see
`SKILL.md` and `references/`.

## State Layout

All skill runtime state lives under `~/.amb/` — independent of the skill install directory since Phase 1:

```
~/.amb/
└── state/
    ├── data/
    │   ├── ambient-ride.db   SQLite (wallet metadata, ride state, saved places, ...)
    │   └── .env              AMB_RIDE_PASSPHRASE (created/preserved by install.js)
    └── keys/
        └── <wallet_id>_private.enc, <wallet_id>_public.pem
                              Encrypted Privy keys (decryptable only with the passphrase)
```

⚠️ **This directory is wallet material.** The passphrase sits beside the keys it decrypts, so whoever can read the directory can move your funds. Treat it the way you would treat a password manager's data file: do not put it in a shared folder, a synced drive, or a repository, and do not paste it into a chat.

The same layout is what makes a wallet portable, so `cp -r ~/.amb /target/.amb` does move it (`k_i_key_path` is a relative path, so there are no absolute-path conflicts) — but that copy carries the keys and the passphrase with it. Copy it only to a machine you control, and delete the copy when you are done with it.

Old locations (`~/.tada-ride-agent/`, `<SKILL_DIR>/.tada-state/`) are auto-migrated on the first `loadConfig()` call (backup-first, idempotent).

## Optional runtime overrides

The defaults work without any env vars. Only override in special cases.

| Env var | Default | Purpose |
|---|---|---|
| `AMB_RIDE_STATE_DIR` | `~/.amb` | State root. Holds the local database and wallet keys (under `state/`) plus runtime and diagnostic files. |
| `AMB_RIDE_PASSPHRASE` | (generated by `install.js`) | Wallet-key encryption passphrase. If you move state without moving this, the keys can no longer be decrypted. |
| `AMB_RIDE_LOG_LEVEL` | `info` | Runtime log verbosity. |
| `AMB_RIDE_OPENCLAW_CLI` | `openclaw` | Path to an executable named `openclaw` (custom installation directories and symlinks supported). Invalid explicit paths fail without selecting another installation. |
| `AMB_RIDE_RPC_URL_<NETWORK>` | build default | Per-network RPC override (for example, `AMB_RIDE_RPC_URL_BASE_SEPOLIA`). |
| `AMB_TELEMETRY_SERVICE_URL` | baked build URL | Development-only proxy override for telemetry E2E/local service checks. Staging and production reject a different endpoint. |
| `AMB_RIDE_NOTIFY_WEBHOOK_URL` | (unset) | Optional webhook for out-of-band ride alarms; ride-relay POSTs each alarm as JSON. See `SKILL.md` → "Out-of-band ride alarms" for webhook secret and Telegram configuration. |
| `AMB_RIDE_NOTIFICATION_V2_ENABLED` | `false` | Internal rollout gate for the route-aware notification foundation. Keep disabled until the notification redesign activation release. |

## Repository layout

- `scripts/`, `references/`, `SKILL.md`, `package.json` — the skill itself
- Runtime state lives under `~/.amb/` — see State Layout above

## License

Two artifacts, two licenses:

| Artifact | License |
| --- | --- |
| **Skill bundle** — `SKILL.md`, `references/`, `scripts/` (this repo) | **MIT-0** — see `LICENSE`. No attribution required. |
| **CLI** — `@ambprotocol/ride-cli` (installed separately) | **Proprietary** — install and run only; no redistribution, modification, or reverse engineering. See the `LICENSE` file inside the npm package, or run `amb --version` |

Using the CLI to access TADA/Throo services is additionally governed by the TADA/Throo Terms of Service.
