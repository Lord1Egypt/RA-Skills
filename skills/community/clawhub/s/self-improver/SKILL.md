---
name: self-improving-agent
description: Self-improving agent system for OpenClaw. Enables continuous learning from interactions, errors, and recoveries. Automatically improves performance over time.
---

# Self-Improving Agent

A continuous learning agent system for OpenClaw that learns from:
- ✅ **Interactions** - Learn from every conversation
- ✅ **Errors** - Learn from mistakes to avoid them
- ✅ **Recoveries** - Learn what works to recover successfully

---

## ✨ Features

- 🧠 **Continuous Learning** - Learns from every interaction
- ❌ **Error Learning** - Learns from mistakes to avoid repetition
- ✅ **Recovery Learning** - Learns successful recovery patterns
- 🔄 **Auto-Improvement** - Automatically applies improvements
- 📚 **Memory System** - Stores and retrieves learnings
- 🔌 **Hook System** - Extensible hook system for custom improvements
- 📊 **Progress Tracking** - Track improvement over time
- 🔧 **Python CLI** - Easy to use command-line interface
- 🧩 **OpenClaw Skill** - Seamless integration with OpenClaw

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenClaw installed
- pip or uv package manager

### Installation

#### As OpenClaw Skill

```bash
# Clone to OpenClaw skills directory
cd ~/.openclaw/workspace/skills
git clone https://github.com/leohuang8688/self-improving-agent.git
```

**Auto-learning is enabled by default!** After each OpenClaw session, the agent will automatically learn and improve.

#### As Python Package

```bash
# Clone the repository
git clone https://github.com/leohuang8688/self-improving-agent.git
cd self-improving-agent

# Install with pip
pip install -e .

# Or install with uv
uv pip install -e .
```

### Basic Usage

#### Automatic Mode (Recommended)

Just use OpenClaw normally! Learning happens automatically after each session, error, or recovery.

```bash
# Start OpenClaw
openclaw

# Use it normally...

# Exit OpenClaw
# → Auto-learning triggers automatically!
```

#### Manual Mode

```bash
# Run the self-improving agent
python -m self_improving_agent run

# Learn from last session
python -m self_improving_agent learn

# Learn from errors
python -m self_improving_agent learn-errors

# Learn from recoveries
python -m self_improving_agent learn-recoveries

# Review all learnings
python -m self_improving_agent review

# Export learnings to file
python -m self_improving_agent export
```

---

## 📖 Commands

### `run` - Run the Agent

Executes the self-improving agent with all applied improvements.

```bash
python -m self_improving_agent run --workspace /path/to/workspace
```

### `learn` - Learn from Session

Analyzes the last session and extracts learnings.

```bash
python -m self_improving_agent learn --verbose
```

### `learn-errors` - Learn from Errors

Analyzes error logs and extracts learnings.

```bash
python -m self_improving_agent learn-errors --verbose
```

### `learn-recoveries` - Learn from Recoveries

Analyzes recovery logs and extracts successful patterns.

```bash
python -m self_improving_agent learn-recoveries --verbose
```

### `review` - Review Learnings

Reviews all stored learnings.

```bash
python -m self_improving_agent review --verbose
```

### `export` - Export Learnings

Exports all learnings to a markdown file.

```bash
python -m self_improving_agent export
```

---

## 🪝 Hook System

### Available Hooks

#### `onSessionEnd(session)`
- **Triggered**: When session ends
- **Purpose**: Post-session learning, cleanup, save state
- **Parameter**: `session` - Session object

#### `onError(error)`
- **Triggered**: When an error occurs
- **Purpose**: Error logging, learning from mistakes
- **Parameter**: `error` - Error object

#### `onRecovery()`
- **Triggered**: When recovering from error
- **Purpose**: Learn successful recovery patterns
- **Parameter**: None

---

## 📝 Learning Types

### 1. **Session Learning**
- **Triggered by**: `onSessionEnd`
- **Learns from**: Conversation patterns, user preferences
- **Stored in**: `learnings/sessions.json`

### 2. **Error Learning**
- **Triggered by**: `onError`
- **Learns from**: Mistakes, errors, failures
- **Stored in**: `learnings/errors.json`
- **Purpose**: Avoid repeating mistakes

### 3. **Recovery Learning**
- **Triggered by**: `onRecovery`
- **Learns from**: Successful recoveries
- **Stored in**: `learnings/recoveries.json`
- **Purpose**: Repeat successful recovery patterns

---

## 📁 Project Structure

```
self-improving-agent/
├── src/
│   ├── hooks.py              # Hook manager
│   └── ...
├── hooks/
│   └── error_learning.py     # Error learning hook
├── learnings/
│   ├── sessions.json         # Session learnings
│   ├── errors.json           # Error learnings
│   └── recoveries.json       # Recovery learnings
├── main.py
├── README.md
└── SKILL.md
```

---

## 🔧 Configuration

In OpenClaw configuration file:

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "self-improve": {
          "enabled": true
        },
        "error-learning": {
          "enabled": true
        }
      }
    }
  }
}
```

---

## 📊 Learning Files

### `learnings/errors.json`
```json
[
  {
    "timestamp": "2026-03-15T12:30:00",
    "error_type": "ValueError",
    "error_message": "Invalid parameter",
    "context": {
      "traceback": "..."
    }
  }
]
```

### `learnings/recoveries.json`
```json
[
  {
    "timestamp": "2026-03-15T12:35:00",
    "recovery_method": "automatic_recovery"
  }
]
```

---

## 🎯 Best Practices

1. **Review learnings regularly** - Review and apply learnings weekly
2. **Export learnings** - Export learnings for backup
3. **Apply learnings** - Apply learnings to improve future performance
4. **Clean old learnings** - Remove outdated learnings periodically

---

## 📝 License

MIT License

## 👨‍💻 Author

PocketAI for Leo - OpenClaw Community
