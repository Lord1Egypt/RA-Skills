# 🏎️ OpenClaw Sport Mode

> **Shift your agent into high gear.** 
> Temporarily boost OpenClaw's heartbeat frequency for intense monitoring tasks, then auto-cool-down when done.

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)

## Why?

By default, OpenClaw checks in every 30 minutes. That's great for battery life, but terrible when you're:
- 🍿 Watching **Codex** write code (you want to see errors *now*).
- 🏗️ Waiting for a **long build** or deployment.
- 🎮 Playing a turn-based game with your agent.

**Sport Mode** lets you toggle a high-frequency heartbeat (e.g., 3m, 1m) and inject a "Mission" that the agent will obsessively check until completion.

## 🚀 Installation

### Manual
```bash
git clone https://github.com/l1veIn/openclaw-sport-mode.git ~/.openclaw/skills/sport-mode
```

## 🗣️ Conversational Usage (Recommended)

Just ask your agent!

> **You:** "I'm running a long compile task. Can you watch it for me?"
> **Agent:** "Sure."
> **You:** "Start **Sport Mode** with a 1-minute interval. If it fails, ping me."
> **Agent:** (Executes `sport-mode on` automatically) "🏎️ Sport Mode activated!"

## 💻 CLI Usage

### 1. Shift into Sport Mode (On)

```bash
# Default: 3-minute interval
sport-mode on --task "Monitor the build. If failed, notify me immediately."

# Turbo Mode: 1-minute interval
sport-mode on --task "Play idiom solitaire" --every "1m"
```

This will:
1. Hot-patch your `openclaw.json` to the new interval (Gateway reloads automatically).
2. Create/Overwrite `HEARTBEAT.md` with your task and a state machine template.

### 2. Cool Down (Off)

```bash
sport-mode off
```

This will:
1. Reset heartbeat to **30m** (default).
2. Clear `HEARTBEAT.md`.

## 🌟 Real World Examples

### 1. Supervising Coding Agents
We used Sport Mode to supervise **Codex** building a complex Rust project through multiple milestones.
Instead of manually checking progress, we set the agent on auto-pilot:

```bash
sport-mode on --task "Monitor Codex in tmux. If current milestone passes tests, auto-start the next one. If stuck, notify me."
```
**Result:** The agent autonomously verified tests, committed code, and started the next phase—all while we grabbed a coffee. ☕

### 2. Interactive Games
Turn your agent into a game master.

#### Word Chain (English)
```bash
sport-mode on --every "1m" --task "Play Word Chain. Start with 'Apple'. Reply with a word starting with the last letter. 10 rounds."
```

#### 成语接龙 (Chinese Idiom Solitaire)
```bash
sport-mode on --every "1m" --task "成语接龙：每分钟回复一个成语，接上一个成语的尾字。5轮后自动结束。"
```
### 3. The Self-Destruct Protocol (自毁机制)
How to ensure the high-frequency heartbeat stops automatically? Write the shutdown command *into* the task instructions.

**Initial `HEARTBEAT.md`:**
```markdown
# 🏎️ Sport Mode Active
Target: 1m

## Task
Count down from 5.
State: 5

## Instructions
1. Decrement state.
2. If State > 0, update this file.
3. If State == 0, run: `sport-mode off` (Self-Destruct).
```

**Agent Action (Round 1):**
- Reads file.
- Sends "Count: 4".
- **Updates file** to `State: 4`.

**Agent Action (Round 5):**
- Reads `State: 1`.
- Decrements to 0.
- Executes `sport-mode off`.
- **Result:** Heartbeat resets to 30m, file is cleared. Mission complete.

## 🧠 Best Practices

### The "Auto-Pilot" Pattern
Sport Mode encourages a **Stateless Agent, Stateful File** pattern. 
Instead of relying on a massive conversation history context, let the agent read `HEARTBEAT.md`, perform one step, update `HEARTBEAT.md`, and sleep.

**Example HEARTBEAT.md during a game:**
```markdown
# 🏎️ Sport Mode Active
Target: 1m

## Task
Idiom Solitaire
State:
- Last: 天长地久
- Remaining: 1

## Auto-Off
If Remaining == 0, run `sport-mode off`.
```

### Silence is Golden
When running every 1 minute, don't let your agent spam you.
- **No change?** Reply `HEARTBEAT_OK` (silence).
- **Status changed?** Send a notification.

## License

MIT
