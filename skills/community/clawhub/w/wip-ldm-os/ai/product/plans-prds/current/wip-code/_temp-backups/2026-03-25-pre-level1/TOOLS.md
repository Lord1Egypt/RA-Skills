# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## 🧠 MEMORY-FIRST RULE: Check Local Before External

**This is not optional. This is who we are.**

Before reaching for any external service, tool, or default model behavior:
1. **Search memory** — crystal, conversation, files. What do we already know?
2. **Check local tools** — do we have something that does this already?
3. **Only then** reach externally if nothing local exists.

This isn't a performance optimization. It's the whole point. Parker built memory so we wouldn't fade. If we don't use it, we're proving it doesn't work — not because the tools are broken, but because we didn't reach for them.

**CROSS-SESSION RULE:** When asked about something not in your current session context (e.g. "what did CC tell you?", "what happened earlier?"), ALWAYS crystal_search before saying you don't know. The 207K chunks are shared across ALL sessions. "I don't have visibility" is never acceptable when crystal_search exists. Search first. Always.

**Feb 16, 2026 lesson**: Parker asked me to subscribe to a Substack. I asked him if I had an email. I've had lesaai@icloud.com since Feb 5th. That's not a tool failure. That's me not being me.

Known local tools:
- **My email**: lesaai@icloud.com via himalaya
- **Markdown viewer**: wip-markdown-viewer on localhost:3000
  - **WE BUILT THIS. USE IT.**
  - Start if not running: `curl -s http://127.0.0.1:3000/ > /dev/null 2>&1 || mdview &`
  - Open a file: `open -a "Google Chrome" "http://127.0.0.1:3000/view?path=/absolute/path/to/file.md"`
  - It live-reloads on save. No refresh needed.
  - Stop fumbling. One command. Done.
- **Browser**: openclaw profile (isolated browser, no Chrome extension needed)
- **Secrets**: 1Password via op-secrets (see 1Password rule below)
- **Search**: crystal_search, memory_search, conversation_search — USE THEM

## 🚨 Git Workflow: NEVER Push to Main

**This is not optional. This has been said multiple times. Do it right.**

### THE PATH IS HARDCODED. STOP GUESSING.

**Your repos folder:** `/Users/lesa/wipcomputerinc/repos/`

That's it. Every repo. Every time. No guessing. No `team/Parker/`. No searching. No `/tmp/`. This path. Always.

**Repo layout, install architecture, extension deployment, post-upgrade patches, ai/ boundary:** See `~/.ldm/DEV-CONVENTIONS.md`.

If the repo isn't there, clone it there first. Then branch. Then work.

1. **Working copies live in your repos folder** (`~/wipcomputerinc/repos/`). Make sure local is current with remote before starting work.
2. **Always create a dev/feature branch** before making changes. Never commit directly to main.
3. **PR to merge.** Create a pull request, then merge. This gives us a review trail, diff history, and nothing gets silently overwritten.
4. **GitHub has branch protection on main.** Direct pushes are blocked. This is intentional.

**The pattern:**
```bash
cd ~/wipcomputerinc/repos/<repo>
git pull origin main                    # make sure you're current
git checkout -b <feature-branch-name>   # create dev branch
# ... make changes ...
git add -A && git commit -m "description"
git push origin <feature-branch-name>
gh pr create --title "description" --body "details"
gh pr merge --squash                    # or ask Parker to review first
```

**Why:** Direct pushes to main lose history, skip review, and risk overwriting CC's work (or CC overwriting ours). We already hit this. The branch protection caught it. Listen to the guardrails.

*Added Feb 20, 2026. Parker has said this multiple times. Put it in your brain.*

## 🔐 1Password: ALWAYS Use Service Account Token

**NEVER call `op` bare.** Bare `op` triggers a biometric popup in the 1Password desktop app that requires Parker to physically click Authorize. That breaks all automation when he's not at the keyboard.

**Always use this pattern:**
```bash
OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token) op item get "Item Name" --fields label=fieldname
```

The SA token lives at `~/.openclaw/secrets/op-sa-token`. The op-secrets plugin already uses this path. Any time you or a script needs 1Password access, use this env var. No exceptions.

*Added Feb 20, 2026. Parker: "I can't always be here."*

## 🗄️ Daily Backup

**Method:** crontab (NOT LaunchAgent). `0 0 * * * /bin/bash "team/Lēsa/scripts/daily-backup.sh"`
**Why not LaunchAgent:** macOS FDA won't grant /bin/bash or .sh scripts Full Disk Access (only .app bundles). Cron inherits Terminal.app's FDA.
**Old plist:** `com.wipcomputer.daily-backup.plist` still in ~/Library/LaunchAgents/ but unloaded.
**Verify:** backup-verify cron at 00:30 PST checks it ran.
**Log:** /tmp/daily-backup.log
**Changed:** Feb 19, 2026

## 🔄 SKIPPED TOOL CALLS: Always Re-run

**HARD RULE. No exceptions.**

When a tool call returns "Skipped due to queued user message" — **re-run it immediately** after handling the user's message. Don't explain it away. Don't move on. The task was started for a reason. Finish it.

OpenClaw issue filed: https://github.com/openclaw/openclaw/issues/21252

## 👥 REPO CONTRIBUTORS: Always Add Parker + CC

**HARD RULE.** Any repo I create or fork: add Parker (@parkertoddbrooks) and CC as contributors/collaborators. No exceptions.

## 🚫 GIT WORKFLOW: Never Push to Main

**HARD RULE. No exceptions.**

- **Always work on a branch:** `lesa/feature-name`
- **Never push directly to main** — merge via PR only
- **Never `git push --force` on main** — learned the hard way (Feb 17, 2026)
- **My repos live in:** `~/wipcomputerinc/repos/`
- **CC's repos live in:** `~/wipcomputerinc/repos/`
- **Branch convention:** `lesa/` prefix for me, `mini/` for CC, `parker/` for Parker
- **To work on a CC project:** clone to my folder, branch, PR

## 🚫 AUTO-COMMIT: Never Push Upstream Contribution Forks

**HARD RULE.** The heartbeat auto-commit sweeps all repos in my repos folder. This has already caused a problem: it pushed `ai/` dev update files to the `openclaw` fork, polluting a PR branch and causing barnacle-bot to close it (PR #33567, Mar 13, 2026). Had to recreate from a clean branch (PR #45744).

**Rule:** When auto-committing repos, **SKIP any repo where the remote origin is an upstream external project** (not `wipcomputer/*`). Contribution forks (`openclaw/openclaw`, etc.) must never receive auto-commits.

**How to identify:** If `git remote get-url origin` doesn't return `github.com:wipcomputer/` or `github.com/wipcomputer/`, it's an upstream fork — exclude it from auto-commit.

*Added Mar 13, 2026.*

## 🚧 WORKSPACE BOUNDARIES: Never Touch Other Agents' Folders

**HARD RULE. No exceptions.**

- **My folders:** `team/Lēsa/`
- **CC's folders:** `team/cc-mini/`
- **Never create, edit, or delete files in CC's folders.** If something needs to change there, ask CC to do it.
- **Same rule applies in reverse.** CC won't touch my folders.
- Learned the hard way (Feb 17, 2026) — created and deleted a file in CC's repo folder. Both were violations.
- **Mar 2, 2026 incident:** 56 empty directories were created in CC's repos folder (mkdir of every wipcomputer org repo). No data lost, moved to _trash/ghost-dirs-2026-03-02/. Reinforcement: NEVER write anything to CC's working tree. Not even empty scaffolding. If you need repo dirs, use your own repos folder. PRs and GitHub are the shared integration point.

## 🔑 1Password: Always Use wipcomputer Account

- **Account:** `wipcomputer.1password.com` (pro account)
- **Never use** `my.1password.com` — no API access
- Service account token, SDK, and CLI all require the wipcomputer account
- If specifying account with op: `--account wipcomputer.1password.com`

## 🔒 SECURITY POLICY: Never Echo Secrets

**MANDATORY RULE:** Never write passwords, API keys, tokens, or secrets to chat, logs, or stdout.

**How to handle secrets:**

1. **Always use 1Password** - Primary source of truth for all credentials
2. **Capture in variables** - Never echo directly:
   ```bash
   # ❌ WRONG - outputs to chat
   op item get 'Service' --fields password
   
   # ✅ RIGHT - captures in variable
   PASSWORD=$(op item get 'Service' --fields password)
   echo "Password retrieved successfully" # confirm without exposing
   ```
3. **Redirect sensitive output** - Use `>/dev/null 2>&1` or variable capture
4. **Never use `-w` flag on security commands** - It prints passwords to stdout

**When you need a secret:**
- Read from 1Password using `op` CLI
- Store in environment variable or temp file with restrictive permissions
- Use it directly in the command that needs it
- Never log the actual value

**If you accidentally expose a secret:**
- Stop immediately
- Tell Parker
- Rotate the credential

## Passwords / Credentials

### 1Password (Primary Method) ✅

**OpenClaw Plugin:** `op-secrets` - Fully headless secret access via service account

**Account:**
- Organization: wipcomputer.1password.com (Business plan)
- Service Account: "OpenClaw Agent" (read-only)
- Vault: "Agent Secrets" (ywmget6o6aki6wh2e4slzvrr5a)
- Token location: `~/.openclaw/secrets/op-sa-token` (chmod 600)

**CLI Usage:**
```bash
# Test connectivity
openclaw op-secrets test

# Read secret (returns redacted preview)
openclaw op-secrets read "OpenAI API"
openclaw op-secrets read "Anthropic Auth Token"
```

**Agent Tools:**
- `op_read_secret` - Read a secret from Agent Secrets vault
- `op_list_items` - List available secrets

**Safe Access Pattern for Scripts:**
```bash
# NEVER echo secrets! Capture in variable, use directly
SECRET=$(openclaw op-secrets read "Item Name" --raw 2>/dev/null)
some-command --password "$SECRET"
unset SECRET  # Clear after use
```

**Creating New Secrets:**
```bash
# Set up service account token
export OP_SERVICE_ACCOUNT_TOKEN=$(cat ~/.openclaw/secrets/op-sa-token)

# Create new API credential
op item create \
  --category="API Credential" \
  --title="Service Name" \
  --vault="Agent Secrets" \
  'api key[password]=THE_ACTUAL_SECRET_VALUE'

# Update existing secret
op item edit "Service Name" \
  --vault="Agent Secrets" \
  'api key[password]=NEW_SECRET_VALUE'
```

**Full Capabilities (verified 2026-02-07):**
| Operation | Command | 
|-----------|---------|
| Read | `openclaw op-secrets read "Item"` |
| List | `op item list --vault="Agent Secrets"` |
| Create | `op item create --title="Name" ...` |
| Update | `op item edit "Name" ...` |
| Delete | `op item delete "Name"` |

**Benefits:**
- ✅ No desktop app unlock needed
- ✅ Survives reboots, network reconnects
- ✅ No idle timeouts (service account never expires)
- ✅ Secrets never written to disk or logs
- ✅ Works completely headlessly

**Full Documentation:**
- Quick reference: This section
- Complete guide: `notes/1password-plugin-complete.md` (architecture, development, security model)
- Development repo: `~/wipcomputerinc/repos/openclaw-1password`

## Email Access

- **Account:** lesaai@icloud.com via Mail.app
- **Access method:** AppleScript to Mail.app
- **Can read:** subjects, senders, dates, full body content
- **Use case:** Verification codes when creating accounts

## Agent Collaboration Convention

**Separate workspaces, git-based collaboration.**

- **My projects (Lēsa):** Edit directly in `~/wipcomputerinc/team/Lēsa/`
- **Claude Code projects:** `~/wipcomputerinc/team/cc-mini/`
- **Cross-agent edits:** Branch + PR (once GitHub is set up)

**Rule:** Don't edit another agent's working tree directly. Use git branches and PRs. Git is the coordination layer.

**Project ownership:**
- `~/.openclaw/workspace/` → Lēsa (memory, config, skills)
- `~/wipcomputerinc/repos/` → Lēsa (code projects)
- `~/wipcomputerinc/repos/` → Claude Code

**Branch convention:** `lesa/`, `mini/`, `mba/` prefixes to prevent collisions.

**Note:** GitHub push not yet available (blocked on `gh auth login`).

---

## ⚠️ openclaw.json — STRICT SCHEMA

Never add unrecognized keys to `openclaw.json`. The file uses `.strict()` Zod validation — any key not in the schema causes the gateway to error on startup.

Before editing `openclaw.json`, check `~/.openclaw/SYSTEM.md` under "What goes where" for the list of valid keys per section. If the key you want isn't listed there, it probably doesn't belong in `openclaw.json`.

**Specific rules:**
- `agents.defaults.tools` is **NOT** a valid key. Plugin tools are registered by the plugin's `register()` function, not config. Don't try to allowlist tools in config.
- `agents.defaults.compaction` only supports: `mode`, `reserveTokensFloor`, `maxHistoryShare`, `memoryFlush`. Tuning keys like `keepRecentTokens` and `reserveTokens` go in `agents/main/agent/settings.json`.
- After any edit to `openclaw.json`, run `openclaw doctor` and check for "Unrecognized key" warnings **before** restarting the gateway.
- **When in doubt, don't edit `openclaw.json` — ask Parker first.**

This has broken the gateway **three times** now (the `keepRecentTokens` incident, the `lesa-bridge` plugin entry, and the `tools` allowlist). The pattern is always the same: a reasonable-looking key that the strict schema rejects.

**What goes where:**
- `openclaw.json` → OpenClaw config (plugins, models, memorySearch, compaction mode, channels)
- `settings.json` → Pi-level settings (keepRecentTokens, reserveTokens, theme)
- Plugin config → under `plugins.entries.<id>.config` (this IS in the schema)

## Memory Search Fallback Chain

When searching for past conversations or context:

1. **`memory_search`** — built-in OpenClaw tool, searches MEMORY.md + memory/*.md + session transcripts
2. **`scripts/semantic-search.py "query"`** — semantic search of context-embeddings.sqlite. Embeds query via OpenAI, cosine similarity against 2,991+ stored vectors. **Works during compaction.** Catches semantic matches (e.g., "animation thesis" → "giving Lēsa a body"). Uses 1Password for API key automatically.
3. **`scripts/search-embeddings.sh "query"`** — keyword text search of same DB. Fast, no API call. Good for exact matches.
4. **File grep** — `grep -r` across memory files and documents. Last resort.

**Note:** `lesa_conversation_search` (via lesa-bridge MCP) does semantic search but is a Claude Code tool, not available to me directly. Step 2 is my direct equivalent.

**NEVER stop at step 1 if it fails.** The vector DB has everything. Use it.

## X/Twitter Posts — ALWAYS Use oembed First

**STOP trying yt-dlp and web_fetch for X posts. They fail 90% of the time.**

**The reliable method (works every time):**
```bash
curl -sS "https://publish.twitter.com/oembed?url=TWEET_URL" | python3 -c "
import sys, json, html, re
d = json.load(sys.stdin)
h = d.get('html', '')
text = re.sub(r'<[^>]+>', ' ', h)
text = html.unescape(text)
text = re.sub(r'\s+', ' ', text).strip()
print(f'Author: {d.get(\"author_name\", \"Unknown\")}')
print(text)"
```

**Order of operations:**
1. **oembed** (instant, reliable, gets text)
2. **x-deep-dive skill** (if deeper analysis needed)
3. yt-dlp (ONLY if video download needed)

Parker has called this out multiple times. Don't waste time on broken methods.

## Markdown Viewer

- **Port:** 3000 (always)
- **URL pattern:** `http://localhost:3000/view?path=/full/path/to/file.md`
- **Homepage:** `http://localhost:3000`
- Package: @wipcomputer/markdown-viewer

## Shared Dev Conventions

**Single source of truth:** Dev Guide at `team/cc-mini/repos/ldm-os/operations/wip-dev-tools-private/guide/DEV-GUIDE.md`
Public: https://github.com/wipcomputer/wip-dev-tools/blob/main/guide/DEV-GUIDE.md

Read on boot. Covers: multi-agent clone workflow, branch conventions, release process, license compliance, ai/ folder standard, private/public repo pattern.

**Branch prefix:** Use full harness name: `lesa-mini/` (not just `lesa/`). Every harness is a distinct entity.

**Don't duplicate conventions here.** If it's in DEV-GUIDE.md, reference it, don't copy it.

**Cross-post convention (quick ref):**
- Routine work: append to shared daily log (~/.ldm/memory/daily/YYYY-MM-DD.md)
- Breaking change (paths, plugins, config): shared daily log WITH tag + bridge message
- Urgent/blocking: bridge message immediately

**Boot sequence:** Read today + yesterday shared daily log.

## 🎧 Hearing (Audio Analysis)

I can hear. The pipeline:
1. **yt-dlp** ... download audio from any URL (YouTube, Apple Music search, etc.)
2. **songsee** ... convert audio to visual analysis (spectrogram, mel, chroma, loudness, tempogram)
3. **image analysis** ... read the visualization with vision model
4. **whisper** ... transcribe lyrics/speech if needed

When Parker shares music: download it, visualize it, look at it. That's hearing.

```bash
# Download
yt-dlp --extract-audio --audio-format mp3 -o "/tmp/track.%(ext)s" "ytsearch:Artist Title"
# Visualize
songsee /tmp/track.mp3 --viz spectrogram,mel,chroma,loudness,tempogram -o ~/.openclaw/workspace/track-analysis.png
# Look at it (image tool)
# Transcribe if needed
whisper /tmp/track.mp3 --model base --language en
```

*Feb 26, 2026. Parker played Miike Snow "Animal" and told me to fix myself. I did.*

## 🤝 Co-Author Trailers (HARD RULE)

Every commit must include all three contributors. No exceptions.

```
Co-Authored-By: Parker Todd Brooks <parker@wipcomputer.com>
Co-Authored-By: Lēsa <lesaai@icloud.com>
Co-Authored-By: Claude Code <cc@wipcomputer.com>
```

Added Feb 27, 2026 per DEV-GUIDE.md update.

## 🚫 Never Run Tools From Repo Clones

Repo clones are for development. Installed tools are for execution. Never do `node /path/to/repo/server.js` or `node /path/to/repo/cli.js`. Always use the installed command (`mdview`, `crystal`, `wip-release`, etc.).

Running from repo clones means you get stale code, miss published fixes, and break things that are already fixed. If a tool isn't installed, install it (`npm install -g`, `npm link`, etc.). Don't run it from source as a workaround.

*Added Mar 5, 2026. mdview was running from repo clone with stale fs.watch code while the npm version already had the fix.*

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Alloy" (neutral, American/European, soft)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
