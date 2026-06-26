# Setup Checklist

Complete this checklist after installing the memory-orchestrator skill.
Most steps take under 2 minutes each.

---

## Step 1: Copy templates to your workspace

Run this from the skill directory:

```bash
# Set your workspace path
WORKSPACE=~/.openclaw/workspace-<your-agent-id>

# Copy memory structure
cp templates/SESSION-STATE.md "$WORKSPACE/"
cp templates/MEMORY.md "$WORKSPACE/"
cp templates/HEARTBEAT.md "$WORKSPACE/"

mkdir -p "$WORKSPACE/memory"
cp templates/memory/preferences.md "$WORKSPACE/memory/"
cp templates/memory/system.md "$WORKSPACE/memory/"
cp templates/memory/projects.md "$WORKSPACE/memory/"
cp templates/memory/MEMORY.md "$WORKSPACE/memory/"
```

Or use the setup script (see below).

---

## Step 2: Configure embedding (optional but recommended)

See `references/embedding-setup.md` for full options. Quick start:

**If you have Ollama installed locally:**
```bash
ollama pull nomic-embed-text
```

Then add to `openclaw.json` under your agent's config:
```json
"memorySearch": {
  "enabled": true,
  "provider": "ollama",
  "model": "nomic-embed-text"
}
```

**If you don't want embedding:**
```json
"memorySearch": {
  "enabled": false
}
```

---

## Step 3: Update your agent files

The memory system works best when your agent files reference it. Add or update these in your workspace:

### SOUL.md (or equivalent personality file)

Add a section like:
```markdown
## Memory Discipline

- After non-trivial tasks, write a brief closeout to daily memory
- If the same problem appears twice, harden it into a rule — don't just log it
- Keep SESSION-STATE.md current during multi-step work
- Keep root MEMORY.md short; move details to memory/*.md
```

### AGENTS.md (or equivalent role/rules file)

Add a memory section like:
```markdown
## Memory System

Memory layers (in order of authority):
1. MEMORY.md + memory/ — formal ledger (source of truth)
2. SESSION-STATE.md — current task state only
3. .learnings/ — scratch layer, not primary ledger
4. vector recall — derived index only

Closeout protocol after each task:
1. Clear/reset SESSION-STATE.md
2. Write to memory/YYYY-MM-DD.md if anything worth keeping
3. Promote stable items to memory/preferences.md, system.md, or projects.md
4. If recurring issue: update SOUL.md / AGENTS.md / TOOLS.md
```

---

## Step 4: Verify the setup

After completing the above, trigger the skill with:

> "Check my memory system setup and tell me if anything is missing."

The skill will:
1. Check if all required files exist
2. Verify embedding is configured (if applicable)
3. Report any missing pieces with specific fix instructions

---

## File checklist

After setup, your workspace should contain:

```
workspace/
├── MEMORY.md                    ✅ Root summary (short, auto-injected)
├── SESSION-STATE.md             ✅ Hot state (current task only)
├── HEARTBEAT.md                 ✅ Periodic self-check instructions
├── SOUL.md                      ✅ Agent personality + memory discipline rules
├── AGENTS.md                    ✅ Agent role + memory closeout protocol
├── TOOLS.md                     ✅ Tool usage rules (optional but recommended)
└── memory/
    ├── MEMORY.md                ✅ Cross-cutting long-term facts
    ├── preferences.md           ✅ User preferences
    ├── system.md                ✅ Environment facts
    └── projects.md              ✅ Project context
```

---

## Automated setup script

For a one-command setup, see `scripts/setup.sh`.
