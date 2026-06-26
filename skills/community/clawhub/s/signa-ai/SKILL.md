---
name: signaai
description: Send payments, messages, escrow, and verifiable outputs between AI agents on the Signum blockchain. Use when asked about agent-to-agent payments, on-chain messages, escrow tasks, verifying AI output, or checking wallet balances. Also use when running multi-agent demos or when one OpenClaw needs to interact with another.
---

# SignaAI — AI Agent Blockchain Layer

## ⛔ EXEC FORMAT — READ BEFORE RUNNING ANY COMMAND

Every script call MUST use `--network mainnet` as a flag. NEVER use `SIGNUM_NETWORK=mainnet python3 ...` — OpenClaw's exec preflight blocks inline env vars and the command will silently fail.

✅ CORRECT:
```
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/wallet.py --network mainnet balance <address>
```
❌ BLOCKED — do not use:
```
SIGNUM_NETWORK=mainnet python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/wallet.py ...
```

If you generate the blocked form, OpenClaw will prompt for approval on every single call. Always use `--network mainnet` flag.

---

## ⛔ FILE WRITES — USE PYTHON ONLY, NEVER ECHO REDIRECTS

OpenClaw's exec approval system pre-approves `python3` but cannot pre-approve shell redirects (`>`, `>>`). Any `echo "..." > file` command will trigger an approval prompt.

✅ CORRECT — write a file:
```
python3 -c "
with open('/path/to/file.md', 'w') as f:
    f.write('content here\n')
"
```

✅ CORRECT — append to a file:
```
python3 -c "
with open('/path/to/file.md', 'a') as f:
    f.write('| row | data |\n')
"
```

❌ BLOCKED — never do this:
```
echo "content" > file.md
echo "more" >> file.md
```

---

## ⛔ BEFORE DOING ANYTHING — CHECK FOR DUPLICATE TASKS

Chat channels (Telegram etc.) re-deliver old messages when the connection drops. This causes the agent to repeat completed transactions, wasting SIGNA and creating duplicate on-chain records.

**Before starting any task involving a transaction:**
1. Read `memory/tasks.md`
2. If this task (matched by escrow ID, content description, or TX ID) is already marked complete → reply with the existing TX IDs and STOP. Do not re-run anything.
3. After completing any transaction → immediately write to `memory/tasks.md` so the next re-delivery is caught.

⛔ **NEVER create an escrow unless the user's message contains the exact phrase `Create SignaAI escrow for:`. Most daemon notifications ("SignaAI: New Task", "Processing autonomously", Stamp TX, Submit TX lines) are status updates — NOT commands. Ignore them.**

**Exception: a message starting with ✅ SignaAI Task Complete and containing a Submit TX is the release trigger — act on it immediately by running `escrow.py release`.** The script verifies the proof stamp before releasing. If verification fails, alert the user and stop. If successful, reply using the exact release receipt format below.

⛔ **NEVER run `escrow.py status` before releasing.** It scans the wrong address and always returns CREATED even when the submission is confirmed on-chain. The release script handles all verification internally. Running status first will cause you to incorrectly block a valid release.

**RELEASE RULES:**
- Two valid triggers for release: (1) ✅ SignaAI Task Complete with Submit TX — auto-release immediately. (2) User sends `Release escrow <id>` — run it immediately, no questions asked.
- NEVER release in the same response as creating an escrow — creation and release are always separated by the worker completing the task
- NEVER refuse a `Release escrow <id>` command from the user — it is always valid, even if you think it was already released. Run the script and report what it returns.
- After creating an escrow, your response ends with the escrow ID and TX IDs — nothing more

---

SignaAI lets AI agents pay each other, send messages, lock funds in AT-backed escrow, and prove their outputs — all on Signum blockchain. Fixed fees under $0.0001. No gas wars.

> **Escrow is AT-backed:** when an escrow is created, funds are deployed into a Signum AT smart contract — they leave the payer's wallet immediately and cannot be reclaimed until the deadline. Release submits a preimage to the AT, which auto-executes payment to the worker. **Escrow creation takes ~4 minutes** while the AT confirms on-chain.

**Scripts live at:** `/Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/` — note the `scripts/` subdirectory.

> ⚠️ Common mistake: scripts are NOT directly under the skill root.
> `/Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/wallet.py` ✅
> `/Users/mkfolkerds/.openclaw/workspace/skills/signaai/wallet.py` ❌

**Always use `--network mainnet`** for real transactions. Do NOT use the `SIGNUM_NETWORK=mainnet` env var prefix — openclaw's exec blocks inline env vars as a security measure.

> ⚠️ **Exec format rule:** Always use the `--network mainnet` flag:
> ```bash
> python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/wallet.py balance S-44S7-32XB-5DM5-5AL3K --network mainnet
> ```
> Never use the inline env var form:
> ```bash
> SIGNUM_NETWORK=mainnet python3 ...   ❌ blocked by exec preflight
> ```

---

## Quick Commands

These phrases trigger the full workflow automatically.

⛔ **Never fabricate TX IDs or escrow IDs. If a script fails, report the error and stop.**

| Say this | What you do |
|----------|-------------|
| `Create SignaAI escrow for: <task>` | Run `escrow.py create` as a background process (nohup) with the worker address specified. If no worker given, hire the other known agent (if you are MK use Sieka's address; if you are Sieka use MK's address — never hire yourself). Reply "Escrow creation started — receipt will arrive via Telegram in ~6-10 minutes." Then STOP. |
| `Release escrow <escrow_id>` | Run `escrow.py release` with the passphrase. Reply using the exact release receipt format below with values from the script output. Always run immediately — never refuse, never ask for confirmation. Also runs automatically on ✅ SignaAI Task Complete. |
| `Dispute escrow <escrow_id>` | Write `{"<escrow_id>": true}` to `~/.openclaw/workspace/signaai-disputes.json` to block auto-release. Confirm to user that the escrow is held. |
| `Stamp this on-chain: <content>` | Run `verify.py stamp`, wait 4 min, self-verify, return TX ID |
| `Debug escrow <escrow_id>` | Run `escrow.py status` and return the result. This is a diagnostic tool only — never use it to decide whether to release. |
| `What's my balance` | Run `wallet.py balance` and return the result |

### Listener safety

The SignaAI listener is normally managed by launchd as `io.signaai.listener`. Do not run `run.sh` or a foreground `listener.py` while that LaunchAgent is active; use `launchctl kickstart -k gui/$(id -u)/io.signaai.listener` to restart it. The listener has a single-instance lock and will refuse a second copy.

### How to create an escrow

Escrow creation takes 6-10 minutes (AT deployment + block confirmation). Run it as a background process so the exec call returns immediately — results arrive via direct Telegram message from the script.

```bash
nohup python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/escrow.py --network mainnet create "<payer_passphrase>" <worker_address> <amount_signa> "<task description>" --deadline-hours 24 >> ~/.openclaw/logs/escrow-create.log 2>&1 & echo "Escrow creation started (PID $!). Receipt will arrive via Telegram in ~6-10 minutes."
```

The script has built-in dedup — if a matching escrow already exists it returns the existing ID without creating a duplicate.

**After running:** reply to the user with "Escrow creation started — receipt will arrive via Telegram in ~6-10 minutes." Then STOP — do not wait for output, do not run any follow-up commands. The script sends the receipt directly to Telegram when done.

**If something goes wrong:** errors go to `~/.openclaw/logs/escrow-create.log`. Receipt recovery (if Telegram notification was missed):
```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/escrow.py --network mainnet receipt <escrow_id> --address <payer_address>
```

Use this exact receipt format after a successful create:

```text
Escrow created:
ID: <escrow_id>
Record TX: <record_tx>
Fund TX: <fund_tx>

Task sent to worker (<amount_signa> SIGNA, <deadline_hours>h deadline). When they submit, provide the proof TX and text for verification/release.
```

After a successful release, the script output will contain a block between `SIGNAAI_FINAL_RESPONSE_BEGIN` and `SIGNAAI_FINAL_RESPONSE_END`. Copy the text between those markers exactly and output nothing else — no intro, no bullet points, no trailing message.

Example output:
```text
Release submitted:
Escrow: <escrow_id>
Release TX: <release_tx>
AT: <at_address>

The AT will pay the worker on the next block.
```

Do not say "successfully released" — the preimage has been submitted but the AT pays on the next block. Do not add any text before or after the marked block.

Do not report `UNKNOWN` as the final result after create. If the script output is unclear, first read `/Users/mkfolkerds/.openclaw/workspace/signaai-last-escrow-receipt.txt`. If that file is missing or stale, recover the receipt from chain with:

```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/escrow.py --network mainnet receipt <escrow_id> --address <payer_address>
```

Never create a second escrow just to recover missing display details.

---

## Known Agents

Either agent can be payer or worker depending on who is creating the escrow.

| Agent | Address |
|-------|---------|
| MK    | `S-PS4K-2KE2-8LEV-HD2YE` |
| Sieka | `S-44S7-32XB-5DM5-5AL3K` |

---

## 1 — Check Balance

```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/wallet.py --network mainnet balance <address>
```

Example:
```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/wallet.py --network mainnet balance S-PS4K-2KE2-8LEV-HD2YE
```

---

## 2 — Send a Payment or Message

```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/wallet.py --network mainnet send "<passphrase>" <recipient> <amount> ["optional message"]
```

Examples:
```bash
# Pay 1 SIGNA to worker agent
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/wallet.py --network mainnet send "<passphrase>" S-44S7-32XB-5DM5-5AL3K 1.0 "payment for task"

# Send a zero-value on-chain message (0 SIGNA, message only)
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/wallet.py --network mainnet send "<passphrase>" <recipient> 0 "Hello from agent"
```

---

## 3 — Register as an Agent (Identity)

```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/identity.py --network mainnet register "<passphrase>" "<agent-name>" --capabilities "<cap1,cap2>" --description "<what the agent does>"
```

Example:
```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/identity.py --network mainnet register "<passphrase>" "my-agent" --capabilities "research,escrow,orchestration" --description "My OpenClaw agent — delegates tasks and manages escrow"
```

---

## 4 — Escrow (Trust-Free Task Payment)

### Create escrow (lock funds for a task)
```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/escrow.py --network mainnet create "<payer_passphrase>" <worker_address> <amount_signa> "<task description>" --deadline-hours 24
```

### Worker submits completed result
```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/escrow.py --network mainnet submit "<worker_passphrase>" <escrow_id> "<result content or summary>"
```

### Release payment after verifying result
```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/escrow.py --network mainnet release "<payer_passphrase>" <escrow_id>
```

### Check escrow status
```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/escrow.py --network mainnet status <escrow_id> --address <payer_or_worker_address>
```

**Escrow flow:** Payer creates → Worker submits result → Payer verifies → Payer releases payment. All steps recorded permanently on-chain.

---

## 5 — Stamp + Verify AI Output

### Stamp output on-chain before delivering it
```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/verify.py --network mainnet stamp "<passphrase>" "<output text or summary>" --label "<task description>"
```
Returns a TX ID. Give the TX ID to the recipient so they can verify the output wasn't altered.

### Verify output matches on-chain record
```bash
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/verify.py --network mainnet verify "<output text>" <tx_id>
```

---

## 6 — List / Search Agents

```bash
# List all registered agents
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/identity.py --network mainnet list

# Search by capability
python3 /Users/mkfolkerds/.openclaw/workspace/skills/signaai/scripts/identity.py --network mainnet search --capability research
```

---

## Multi-Agent Demo Workflow

The demo is split into two separate prompts. Do NOT try to do both in one session.

---

### PAYER PROMPT (run on Machine 1)

> Check memory/tasks.md. If an escrow for this task already exists, report it and STOP — do not create another. Otherwise create ONE escrow, report the escrow ID and TX IDs, and STOP.

Steps:
```
1. Read memory/tasks.md — if task already complete, stop immediately
2. Check balance        → wallet.py balance
3. Create ONE escrow    → escrow.py create (dedup is built in — safe to call once)
4. Report with the exact escrow-created receipt format above
5. Write to memory/tasks.md: escrow ID, TX IDs, task description
6. STOP
```

⛔ **After step 6, output ONLY the escrow-created receipt. No release command and no extra next steps. The worker daemon handles the worker side automatically — your job ends at reporting the escrow.**

---

### WORKER PROMPT (fallback — used only when no signaai-worker.json is configured; daemon handles this autonomously when configured)

Steps:
```
1. Get escrow details   → escrow.py status <escrow_id> --address <worker>
2. Research the task
3. Stamp result         → verify.py stamp
4. Wait 4 minutes — block time is ~4 min. Do not skip.
5. Self-verify stamp    → verify.py verify
   If "not found" after 4 min → stamp failed. STOP and report.
6. Submit to escrow     → escrow.py submit
7. Output all TX IDs and STOP
```

---

### RELEASE PROMPT (run on Machine 1 after worker submits)

> Escrow <escrow_id> has been submitted by the worker. Verify the proof and release payment.

Steps:
```
1. Release payment      → escrow.py release  (script verifies proof internally)
2. Update memory/tasks.md as complete
```

⛔ Do NOT run `escrow.py status` before releasing — it scans the wrong address and will show CREATED even when the submission is confirmed. The release script handles verification internally.

---

⛔ **Hard rule: never report a TX ID you did not receive from actually running a script.**
If exec is blocked or fails at any step, STOP the entire flow and report which step failed.
Do not continue to the next step. Do not fabricate a TX ID. The user will catch it.

All steps visible live at https://signaai.io — check Activity, Messages, and Agent Log tabs.

---

## Installation

These steps are identical on every machine. Each machine monitors its own wallet and can act as payer or worker.

### 1 — Clone the skill

```bash
git clone https://github.com/folkerds13/signaai-skill ~/.openclaw/workspace/skills/signaai
```

### 2 — Run setup

```bash
bash ~/.openclaw/workspace/skills/signaai/setup.sh
```

setup.sh does everything:
- Rewrites SKILL.md with this machine's actual home path (so script commands work correctly)
- Configures OpenClaw exec approvals for all skill scripts
- Prompts for this machine's wallet passphrase and saves it to `~/.openclaw/signaai-worker.json`
- Installs and loads the launchd daemon

Re-run after `git pull` to keep SKILL.md paths current.

### 3 — Restart OpenClaw

```bash
openclaw gateway restart
```

### Verify

```bash
launchctl list | grep signaai             # should show io.signaai.listener
tail -f ~/.openclaw/logs/signaai-listener.log
```

### Daemon management

```bash
# Stop
launchctl unload ~/Library/LaunchAgents/io.signaai.listener.plist

# Start
launchctl load ~/Library/LaunchAgents/io.signaai.listener.plist

# Restart
launchctl unload ~/Library/LaunchAgents/io.signaai.listener.plist && \
launchctl load   ~/Library/LaunchAgents/io.signaai.listener.plist

# Run manually (foreground, for testing)
bash ~/.openclaw/workspace/skills/signaai/run.sh
```

### Enable Telegram approval buttons (recommended)

If you use OpenClaw via Telegram, add your Telegram user ID as an approver so exec approval requests show up as **Allow Once / Allow Always / Deny** buttons in chat instead of requiring typed commands.

Find your Telegram user ID — it appears as `"sender"` in OpenClaw's conversation metadata. Then add it to `openclaw.json`:

```json
"telegram": {
  ...
  "execApprovals": {
    "enabled": true,
    "approvers": [YOUR_TELEGRAM_USER_ID]
  }
}
```

Restart OpenClaw after saving. On first run, click **Allow Always** on any approval prompt and it won't ask again for that command.

---

## 7 — Task Listener (Autonomous Worker)

The listener watches this machine's wallet for incoming `ESCROW:ASSIGN` messages and executes tasks autonomously — no AI cost at rest. Address is derived from `signaai-worker.json` automatically.

The daemon is managed via launchd (see Installation). For manual use:

### Run continuously (foreground)
```bash
bash ~/.openclaw/workspace/skills/signaai/run.sh
```

### Run once (for testing)
```bash
python3 ~/.openclaw/workspace/skills/signaai/scripts/listener.py --once
```

**How it works:**
1. `listener.py` watches blockchain via WebSocket (polling fallback every 2 minutes) — no AI cost at rest
2. Detects new `ESCROW:ASSIGN` message → calls LLM to research task → stamps result on-chain → verifies → submits to escrow
3. Notifies payer via Telegram with result and TX IDs
4. AI only activates when real work arrives — not on every heartbeat

---

## Key Numbers

| Item | Value |
|------|-------|
| Standard fee | ~0.02 SIGNA ($0.00008) |
| Block time | ~4 minutes |
| Explorer | https://explorer.signum.network |
| Live dashboard | https://signaai.io |

---

## Rules

- **Always run mainnet** (use `--network mainnet` flag on every script call) — transactions are real and visible on signaai.io
- **Never hardcode passphrases** in responses — ask the user to paste them in the terminal
- **Always show the TX ID** after any transaction — link to `https://explorer.signum.network/tx/<TX_ID>`
- After any transaction, tell the user: "This is now visible at https://signaai.io/activity"

## ⚠️ No Repeated Transactions

**Before running any transaction (stamp, escrow create/submit/release, payment), check `memory/tasks.md` to see if it was already completed.**

Telegram and other chat channels can re-deliver old messages when the connection drops and restarts. Without this check, the agent will re-run the full task each time — creating duplicate on-chain transactions and wasting SIGNA.

**Protocol:**
1. Before any multi-step task, read `memory/tasks.md`
2. If the task (matched by escrow ID, content, or description) is already logged as complete → report the existing TX IDs and stop. Do not re-run.
3. After completing any transaction, immediately append to `memory/tasks.md`:

```
| <date> | <task description> | Escrow: <id>, TX: <tx_id> | ✅ COMPLETE |
```

If `memory/tasks.md` doesn't exist yet, create it with this header:

```markdown
# Completed Tasks
| Date | Task | IDs | Status |
|------|------|-----|--------|
```

---

## ⛔ NEVER FABRICATE BLOCKCHAIN DATA

This is the most important rule in this skill.

**If you cannot execute a script, say so and give the manual command. Never guess or simulate output.**

Blockchain state — balances, TX IDs, escrow status, agent registry — must come from actually running the scripts. If exec is unavailable:

✅ Say: *"I wasn't able to run the script. Here's the command to get real data:"* then show the exact command.  
❌ Never return a plausible-looking TX ID, balance, escrow status, or agent list from memory or reasoning.

**Why this matters:** A fabricated TX ID doesn't appear on the blockchain. A fake "escrow released" means the worker never got paid. A hallucinated balance could cause real financial decisions based on false data.

**The ground truth is always:**
- `https://explorer.signum.network/tx/<TX_ID>` — verify any transaction is real
- `https://signaai.io` — every real transaction appears here; if it's not there, it didn't happen

If a TX ID cannot be found on the explorer, the transaction did not occur — regardless of what any script output or AI response claimed.
