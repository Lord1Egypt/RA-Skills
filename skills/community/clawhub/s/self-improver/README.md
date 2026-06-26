# 🧠 Self-Improving-Agent

**A continuous learning system for OpenClaw that learns from interactions, errors, recoveries, and performance metrics to automatically improve over time.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## ✨ Features

- 🧠 **Continuous Learning** - Learns from every interaction
- ❌ **Error Learning** - Learns from mistakes to avoid repetition
- ✅ **Recovery Learning** - Learns successful recovery patterns
- 📚 **Session Learning** - Learns from successful sessions
- 📊 **Performance Learning** - Learns from performance metrics
- 🔄 **Auto-Improvement** - Automatically applies improvements
- 📚 **Memory System** - Stores and retrieves learnings
- 🔌 **Extensible Hook System** - Easy to add custom hooks
- 🔧 **Python CLI** - Easy to use command-line interface
- 🧩 **OpenClaw Skill** - Seamless integration with OpenClaw

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- OpenClaw installed (optional, for integration)
- pip or uv package manager

### Installation

#### As OpenClaw Skill

```bash
# Clone to OpenClaw skills directory
cd ~/.openclaw/workspace/skills
git clone https://github.com/leohuang8688/self-improving-agent.git
cd self-improving-agent
pip install -e .
```

**Auto-learning is enabled by default!** After each OpenClaw session, error, or recovery, the agent will automatically learn and improve.

#### As Standalone Package

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
# → Auto-learning triggers automatically on errors, recoveries, and session ends!
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

Analyzes error logs and extracts learnings from mistakes.

```bash
python -m self_improving_agent learn-errors --verbose
```

### `learn-recoveries` - Learn from Recoveries

Analyzes recovery logs and extracts successful patterns.

```bash
python -m self_improving_agent learn-recoveries --verbose
```

### `review` - Review Learnings

Reviews all stored learnings from all types.

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

#### Core Hooks (src/hooks.py)

- **`onSessionEnd(session)`**
  - **Triggered**: When session ends
  - **Purpose**: Post-session learning, cleanup, save state
  - **Parameter**: `session` - Session object

- **`onError(error)`**
  - **Triggered**: When an error occurs
  - **Purpose**: Error logging, learning from mistakes
  - **Parameter**: `error` - Error object

- **`onRecovery()`**
  - **Triggered**: When recovering from error
  - **Purpose**: Learn successful recovery patterns
  - **Parameter**: None

- **`onPerformanceMetric(metric)`**
  - **Triggered**: When a performance metric is collected
  - **Purpose**: Learn from performance metrics
  - **Parameter**: `metric` - Performance metric object

#### Learning Hooks (hooks/*.py)

- **`error_learning.py`** - Learns from errors to avoid repetition
- **`session_learning.py`** - Learns from successful sessions
- **`performance_learning.py`** - Learns from performance metrics

---

## 📝 Learning Types

### 1. **Session Learning** 📚
- **Triggered by**: `onSessionEnd`
- **Learns from**: Conversation patterns, user preferences, successful patterns
- **Stored in**: `learnings/sessions.json`
- **Purpose**: Improve future session performance

### 2. **Error Learning** ❌
- **Triggered by**: `onError`
- **Learns from**: Mistakes, errors, failures
- **Stored in**: `learnings/errors.json`
- **Purpose**: Avoid repeating mistakes

### 3. **Recovery Learning** ✅
- **Triggered by**: `onRecovery`
- **Learns from**: Successful recoveries
- **Stored in**: `learnings/recoveries.json`
- **Purpose**: Repeat successful recovery patterns

### 4. **Performance Learning** 📊
- **Triggered by**: `onPerformanceMetric`
- **Learns from**: Performance metrics, optimization opportunities
- **Stored in**: `learnings/performance.json`
- **Purpose**: Optimize performance over time

---

## 📁 Project Structure

```
self-improving-agent/
├── src/
│   └── hooks.py              # Core hook manager
├── hooks/
│   ├── error_learning.py     # Error learning hook
│   ├── session_learning.py   # Session learning hook
│   └── performance_learning.py # Performance learning hook
├── learnings/
│   ├── sessions.json         # Session learnings
│   ├── errors.json           # Error learnings
│   ├── recoveries.json       # Recovery learnings
│   └── performance.json      # Performance learnings
├── test_hooks.py             # Test script
├── main.py                   # Main entry point
├── README.md                 # This file
├── SKILL.md                  # OpenClaw skill definition
└── pyproject.toml            # Python project config
```

---

## 🔧 Configuration

### OpenClaw Integration

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
        },
        "session-learning": {
          "enabled": true
        },
        "performance-learning": {
          "enabled": true
        }
      }
    }
  }
}
```

### Standalone Usage

No configuration needed! Just install and run.

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
      "traceback": "Traceback..."
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

### `learnings/sessions.json`
```json
[
  {
    "timestamp": "2026-03-15T12:00:00",
    "session_id": "session-123",
    "duration": 300,
    "interactions": 10,
    "success_patterns": ["successful_completion"]
  }
]
```

### `learnings/performance.json`
```json
[
  {
    "timestamp": "2026-03-15T12:40:00",
    "metric_type": "response_time",
    "metric_value": 150,
    "context": {
      "operation": "query",
      "duration": 150
    },
    "optimization": ["Consider caching"]
  }
]
```

---

## 🧪 Testing

Run the test suite:

```bash
cd /root/.openclaw/workspace/skills/self-improving-agent
python3 test_hooks.py
```

This will test all hooks and verify that learning is working correctly.

---

## 🎯 Best Practices

1. **Review learnings regularly** - Review and apply learnings weekly
2. **Export learnings** - Export learnings for backup
3. **Apply learnings** - Apply learnings to improve future performance
4. **Clean old learnings** - Remove outdated learnings periodically
5. **Test hooks** - Regularly test hooks to ensure they're working

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**PocketAI for Leo** - OpenClaw Community

GitHub: [@leohuang8688](https://github.com/leohuang8688/self-improving-agent)

---

## 🙏 Acknowledgments

- OpenClaw Team - For the amazing framework
- Leo - For the inspiration and testing
- Community - For continuous support

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/leohuang8688/self-improving-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/leohuang8688/self-improving-agent/discussions)

---

**Happy Learning! 🧠🚀**
