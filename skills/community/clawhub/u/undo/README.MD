# Undo.skill

> Give your AI agent a **time machine for file edits**.
> Revert to any previous state — by conversation step, timestamp, or named checkpoint.

`undo-skill` is a lightweight **Skill plugin** for AI coding agents. It brings **Claude Code-level (and better) undo/revert capabilities** to **OpenClaw** and other Node.js-based LLM agents. It automatically snapshots every file modification and enables powerful **undo/revert capabilities** — so your AI can safely experiment, and you always have a regret pill.

✨ Think of it as **Git for AI actions**, but designed natively for conversational, step-by-step agent workflows.

[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Skill-7c3aed)](https://openclaws.io/docs/tools/skills/)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Compatible-green)](https://agentskills.io)

---

## 🌟 Why You Need This

Today's AI agents **write files but can't undo**. One hallucinated edit → broken app → hours of debugging.

With `undo-skill`:
- 🔙 Revert the last 3 changes with `/undo --steps 3`
- ⏱️ Go back to how files looked at `2026-04-10T14:00`
- 🏷️ Mark safe states: `/checkpoint before-db-migration` → later `/undo --to before-db-migration`
- 🌿 Undo safely — previous states are preserved on branches, never destroyed
- 💡 Perfect for building **AI pair programmers with memory**

---

## 📦 Installation

```bash
# Install to OpenClaw workspace skills (available to all agents)
git clone https://github.com/x-guang/undo-skill ~/.openclaw/workspace/skills/undo

# Or install to a specific project's skills
git clone https://github.com/x-guang/undo-skill <your-project>/.openclaw/skills/undo
```

Then no restart is needed — it auto-initializes on first use, or run `refresh skills` if troubleshooting.

**Requirements:** Node.js ≥ 18, Git ≥ 2.0. That's it — no extra dependencies.

---

## 🧪 Quick Demo

Imagine your AI just broke `package.json`:

```bash
# List recent file changes
node /path/to/undo-skill/scripts/list.js

# Output:
# [5] 2026-04-10 14:05  modified: package.json (+12, -3)
#     └─ Updated dependency versions in package.json
# [4] 2026-04-10 14:03  added: src/utils.ts (+45)
#     └─ Added utility functions for date formatting
# ...

# Undo the last change
node /path/to/undo-skill/scripts/undo.js --steps 1

# Done! package.json is restored, previous state preserved on branch "checkpoint/undo-5"
```

Or ask your agent:
> "undo the last change" / "show me the history" / "go back to before the refactor"

---

## 🛠️ How It Works

1. **Auto-snapshot**: After each AI file modification (Write/Edit/Shell), the skill triggers a snapshot that records all changes via git diff.
2. **External git repo**: Snapshots are stored in `~/.local/share/undo-skill/repos/` — **never in your project directory**. Your project's own `.git` is completely untouched.
3. **Structured commit messages**: Each snapshot includes a human-readable description of what changed, which files were affected, and a summary — useful for both you and the AI to understand history.
4. **Safe undo with branching**: When you undo, the current state is preserved on a `checkpoint/` branch before resetting. You can always restore to the pre-undo state.
5. **Watchdog**: A lightweight file watcher runs in the background as a safety net for multi-turn conversations where the LLM might forget to snapshot.

---

## 🧩 Skill Integration

This is a **drop-in Skill**:
- ✅ Contains `SKILL.md` (auto-loaded by OpenClaw)
- ✅ Pure Node.js scripts — no npm install needed
- ✅ Works alongside other skills (e.g., `git-skill`, `test-skill`)

Just install it — your agent gains temporal awareness.

---

## 🚀 Use Cases

| User Goal | How `undo-skill` Helps |
|--------|------------------------|
| "AI messed up my code" | `/undo --last` instantly recovers |
| "Show me what changed since step 3" | `/undo --list --from 3` |
| "I want to try a risky refactor" | `/checkpoint before-refactor` → experiment → `/undo --to before-refactor` if needed |
| Debug autonomous agent runs | Replay + revert = deterministic testing |

---

## 📁 Project Structure

```
undo-skill/
├── README.md          ← You're reading this!
├── SKILL.md           ← AI-readable skill manifest
├── scripts/
│   ├── init.js        ← Initialize tracking for a project
│   ├── snapshot.js    ← Record current file state
│   ├── undo.js        ← Revert to a previous state
│   ├── list.js        ← List change history
│   ├── checkpoint.js  ← Create named checkpoints
│   └── watcher.js     ← Background file change detector (safety net)
└── references/
    └── api.md         ← Human-readable API spec
```

> 💡 Follows the **standard Skill format** used by OpenClaw, an agent framework.

---

## 🤝 Contribute

Want to add:
- Visual timeline UI?
- Side-effect reversal (e.g., `apt install` → `apt remove`)?
- Integration with other agents (OpenCode, Claude Code, Aider, etc.)?

PRs welcome! Let's make AI coding **safe by default**.

---

## 📜 License

MIT — use freely in personal and commercial projects.

---

> Built for the era of **autonomous AI developers**.
> If this saved you from one broken deploy, please ⭐ the repo — it helps me improve it!
