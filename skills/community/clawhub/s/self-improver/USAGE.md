# 🧠 Self-Improving Agent - Complete Usage Guide

**The Ultimate Guide to Continuous Learning and Auto-Improvement**

**[🇺🇸 English](USAGE.md)** | **[🇨🇳 中文指南](USAGE-CN.md)**

---

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [How It Works](#how-it-works)
3. [Installation](#installation)
4. [Basic Usage](#basic-usage)
5. [Advanced Usage](#advanced-usage)
6. [Configuration](#configuration)
7. [Learning Categories](#learning-categories)
8. [Hook System](#hook-system)
9. [Memory System](#memory-system)
10. [Real-World Examples](#real-world-examples)
11. [Troubleshooting](#troubleshooting)
12. [FAQ](#faq)

---

## 🎯 Introduction

**Self-Improving Agent** is a continuous learning system for OpenClaw that learns from every interaction and automatically improves its performance over time.

### Key Features

- 🧠 **Continuous Learning** - Learns from every interaction
- 🔄 **Auto-Improvement** - Automatically applies improvements
- 📚 **Memory System** - Stores and retrieves learnings
- 🔌 **Hook System** - Extensible hook system for custom improvements
- 📊 **Progress Tracking** - Track improvement over time
- ⚡ **Fully Automated** - Works automatically with OpenClaw

### Benefits

- ✅ **Get Smarter Over Time** - Improves with every use
- ✅ **No Manual Configuration** - Fully automated
- ✅ **Transparent** - All learnings are visible and reviewable
- ✅ **Customizable** - Create custom hooks and categories
- ✅ **Shareable** - Export and share learnings with team

---

## 🔧 How It Works

### Architecture Overview

```
┌─────────────────────────────────────┐
│      OpenClaw Agent Session         │
│         (User Interaction)          │
└──────────────┬──────────────────────┘
               │
               ↓ Session Ends
┌─────────────────────────────────────┐
│     Self-Improving Agent            │
│  ┌─────────────┐  ┌──────────────┐  │
│  │   Extract   │→ │   Analyze    │  │
│  │  Learnings  │  │   Patterns   │  │
│  └─────────────┘  └──────────────┘  │
└──────────────┬──────────────────────┘
               │
               ↓ Learnings
┌─────────────────────────────────────┐
│        Memory System                │
│  ┌─────────────┐  ┌──────────────┐  │
│  │   Store     │→ │   Retrieve   │  │
│  │  Learnings  │  │  Learnings   │  │
│  └─────────────┘  └──────────────┘  │
└──────────────┬──────────────────────┘
               │
               ↓ Apply Improvements
┌─────────────────────────────────────┐
│         Hook System                 │
│  ┌─────────────┐  ┌──────────────┐  │
│  │   Apply     │→ │   Improve    │  │
│  │   Hooks     │  │ Performance  │  │
│  └─────────────┘  └──────────────┘  │
└─────────────────────────────────────┘
```

### Workflow

#### **Phase 1: Run Session**
```bash
python -m self_improving_agent run
```

**What Happens:**
1. Load previously stored learnings
2. Apply all improvement hooks
3. Run OpenClaw Agent with improvements
4. Record new interaction data

#### **Phase 2: Learn & Extract**
```bash
python -m self_improving_agent learn
```

**What Happens:**
1. **Analyze Session Logs**
   - Read OpenClaw session records
   - Identify success and failure patterns

2. **Extract Learnings**
   ```json
   {
       "title": "Avoid Duplicate Searches",
       "category": "optimization",
       "content": "Check cache before searching for similar queries",
       "trigger": "User asks similar questions",
       "action": "Check cache first"
   }
   ```

3. **Store to Memory**
   - Save to `learnings/active_learnings.json`
   - Generate unique ID and timestamp

#### **Phase 3: Review Learnings**
```bash
python -m self_improving_agent review --verbose
```

**Output Example:**
```
📖 Reviewing learnings...

1. Avoid Duplicate Searches
   Category: optimization
   Date: 2026-03-14T10:30:00
   Content: Check cache before searching for similar queries

2. Error Prevention Pattern
   Category: error_prevention
   Date: 2026-03-14T09:15:00
   Content: Check network connection before API calls

✅ Total: 2 learnings
```

#### **Phase 4: Export Learnings**
```bash
python -m self_improving_agent export
```

**Generated File:** `learnings_export.md`

```markdown
# Self-Improving Agent - Learnings Export

Exported: 2026-03-14T11:00:00
Total Learnings: 2

---

## 1. Avoid Duplicate Searches

**Category:** optimization

**Date:** 2026-03-14T10:30:00

**Content:**
Check cache before searching for similar queries

---
```

---

## 🚀 Installation

### Prerequisites

- Python 3.10+
- OpenClaw installed
- pip or uv package manager

### Step 1: Clone the Repository

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/leohuang8688/self-improving-agent.git
cd self-improving-agent
```

### Step 2: Install Dependencies

```bash
# With pip
pip install -e .

# With uv
uv pip install -e .
```

### Step 3: Enable in OpenClaw

Add to your OpenClaw configuration file:

```json
{
  "skills": {
    "self-improving-agent": {
      "enabled": true,
      "auto_learn": true,
      "auto_apply": true
    }
  }
}
```

### Step 4: Restart OpenClaw

```bash
openclaw gateway restart
```

---

## 💻 Basic Usage

### Quick Start

```bash
# Run the self-improving agent
python -m self_improving_agent run

# Learn from last session
python -m self_improving_agent learn

# Review all learnings
python -m self_improving_agent review

# Export learnings to file
python -m self_improving_agent export
```

### Command Reference

#### `run` - Run the Agent

Executes the self-improving agent with all applied improvements.

```bash
python -m self_improving_agent run --workspace /path/to/workspace
```

**Options:**
- `--workspace` - Path to OpenClaw workspace (default: `~/.openclaw/workspace`)
- `--verbose` - Enable verbose output

#### `learn` - Learn from Session

Analyzes the last session and extracts learnings.

```bash
python -m self_improving_agent learn --verbose
```

**Options:**
- `--verbose` - Show detailed analysis
- `--session` - Specify session file to analyze

#### `review` - Review Learnings

Reviews all stored learnings.

```bash
python -m self_improving_agent review --verbose
```

**Options:**
- `--verbose` - Show full content of each learning
- `--category` - Filter by category (e.g., `optimization`)
- `--limit` - Limit number of results (e.g., `--limit 10`)

#### `export` - Export Learnings

Exports all learnings to a markdown file.

```bash
python -m self_improving_agent export
```

**Options:**
- `--output` - Output file path (default: `learnings_export.md`)
- `--format` - Export format (`markdown` or `json`)

---

## ⚙️ Advanced Usage

### Automated Workflow

Set up automatic learning and application:

```json
{
  "skills": {
    "self-improving-agent": {
      "enabled": true,
      "auto_learn": true,
      "auto_apply": true,
      "learn_after_session": true,
      "apply_on_startup": true,
      "review_frequency": "weekly"
    }
  }
}
```

### Custom Hooks

Create custom hooks in the `hooks/` directory:

```python
# hooks/cache_hook.py
"""
Cache Optimization Hook
"""

def apply():
    """Apply cache optimization"""
    print("📦 Applying cache optimization hook...")
    
    # Enable result caching
    enable_cache(ttl=300)  # 5 minute cache
    
    print("✅ Cache optimization applied")
```

### Custom Categories

Add custom learning categories:

```python
# In your learning extraction code
learning = {
    "type": "custom_category",
    "title": "My Custom Learning",
    "content": "Description of the learning"
}
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file in your workspace:

```bash
# Workspace Configuration
WORKSPACE_PATH=~/.openclaw/workspace

# Learning Configuration
LEARNING_ENABLED=true
AUTO_APPLY=true

# Hook Configuration
HOOKS_ENABLED=true

# Memory Configuration
MEMORY_PATH=~/.openclaw/workspace/self-improving-agent/learnings
MAX_LEARNINGS=1000
ARCHIVE_AFTER_DAYS=30
```

### Configuration File

Create `config.json` in your workspace:

```json
{
  "learning": {
    "enabled": true,
    "auto_apply": true,
    "min_confidence": 0.7
  },
  "memory": {
    "max_learnings": 1000,
    "archive_after_days": 30,
    "export_format": "markdown"
  },
  "hooks": {
    "enabled": true,
    "auto_load": true,
    "custom_hooks_path": "./hooks"
  }
}
```

---

## 📚 Learning Categories

### Built-in Categories

#### 1. **skill_improvement**
Improvements to specific skills or capabilities.

```json
{
    "type": "skill_improvement",
    "title": "Improved Stock Analysis",
    "content": "Use 5-day, 20-day, and 60-day moving averages for technical analysis"
}
```

#### 2. **error_prevention**
Patterns to prevent common errors.

```json
{
    "type": "error_prevention",
    "title": "API Call Checks",
    "content": "Check network connection and API key before calling external APIs"
}
```

#### 3. **optimization**
Performance optimizations.

```json
{
    "type": "optimization",
    "title": "Caching Strategy",
    "content": "Cache results for identical queries for 5 minutes"
}
```

#### 4. **best_practice**
Best practices and guidelines.

```json
{
    "type": "best_practice",
    "title": "Error Handling",
    "content": "Wrap all external calls in try-except blocks"
}
```

#### 5. **lesson_learned**
Lessons from failures or mistakes.

```json
{
    "type": "lesson_learned",
    "title": "Git Push Failure",
    "content": "Pull latest code before pushing to avoid conflicts"
}
```

---

## 🔌 Hook System

### What are Hooks?

Hooks are mechanisms that automatically apply learnings as improvements.

### How Hooks Work

```python
# When agent runs
agent.run()
  ↓
hooks.apply_all()  # Apply all hooks
  ↓
# All learned improvements automatically take effect
```

### Creating Custom Hooks

**Example:** `hooks/cache_hook.py`

```python
"""
Cache Optimization Hook
"""

def apply():
    """Apply cache optimization"""
    print("📦 Applying cache optimization hook...")
    
    # Enable result caching
    enable_cache(ttl=300)  # 5 minute cache
    
    print("✅ Cache optimization applied")
```

**Example:** `hooks/error_prevention_hook.py`

```python
"""
Error Prevention Hook
"""

def apply():
    """Apply error prevention improvements"""
    print("🛡️  Applying error prevention hook...")
    
    # Enable network checks
    enable_network_check()
    
    # Enable API validation
    enable_api_validation()
    
    print("✅ Error prevention applied")
```

---

## 💾 Memory System

### Storage Location

```
~/.openclaw/workspace/self-improving-agent/learnings/
├── active_learnings.json    # Current active learnings
├── archive.json             # Archived learnings
└── learnings_export.md      # Exported document
```

### active_learnings.json Structure

```json
[
    {
        "id": "a1b2c3d4",
        "type": "optimization",
        "title": "Cache Optimization",
        "content": "Cache results for identical queries for 5 minutes",
        "date": "2026-03-14T10:30:00",
        "applied": true
    }
]
```

### Memory Lifecycle

1. **New Learning** → Stored in `active_learnings.json`
2. **After 30 Days** → Moved to `archive.json`
3. **On Export** → Generated as `learnings_export.md`

---

## 🌟 Real-World Examples

### Example 1: Daily Usage

```bash
# Morning: Start work
python -m self_improving_agent run

# End of day: Learn from today
python -m self_improving_agent learn

# Weekend: Review learnings
python -m self_improving_agent review --verbose
```

### Example 2: Performance Tuning

```bash
# Run with performance analysis
python -m self_improving_agent run --verbose

# Analyze bottlenecks
python -m self_improving_agent learn

# Apply optimizations
python -m self_improving_agent run  # Automatically applies optimization hooks
```

### Example 3: Team Collaboration

```bash
# Export learnings
python -m self_improving_agent export

# Share with team
cat learnings_export.md | mail team@company.com
```

---

## 🐛 Troubleshooting

### No Learnings Found

**Problem:** `No learnings extracted`

**Solutions:**
1. Ensure learning is enabled in configuration
2. Check if interactions have occurred
3. Verify workspace path is correct
4. Check session logs exist

### Import Errors

**Problem:** `ModuleNotFoundError: No module named 'self_improving_agent'`

**Solutions:**
1. Install package: `pip install -e .`
2. Check Python version: requires Python 3.10+
3. Verify installation: `python -m self_improving_agent --help`

### Hooks Not Applying

**Problem:** `Hooks not being applied`

**Solutions:**
1. Check `hooks/` directory exists
2. Verify hooks have `apply()` function
3. Check for Python syntax errors in hooks
4. Enable hooks in configuration

### Memory Issues

**Problem:** `Memory system not working`

**Solutions:**
1. Check `learnings/` directory exists
2. Verify write permissions
3. Check disk space
4. Review memory configuration

---

## ❓ FAQ

### Q: How often should I run learn?

**A:** Recommended frequency:
- **Daily:** For heavy usage
- **Weekly:** For moderate usage
- **Monthly:** For light usage

### Q: Can I use this without OpenClaw?

**A:** Yes! While designed for OpenClaw, you can use it as a standalone learning system by providing your own session logs.

### Q: How many learnings can I store?

**A:** Default limit is 1000 active learnings. You can configure this in `config.json`.

### Q: Can I share learnings with team?

**A:** Yes! Use `export` command to generate shareable markdown or JSON files.

### Q: Are learnings persistent?

**A:** Yes! Learnings are stored in JSON files and persist across sessions.

### Q: Can I delete specific learnings?

**A:** Yes! Edit `active_learnings.json` manually or use the `review` command with delete option (coming soon).

### Q: How do I backup learnings?

**A:** Backup the entire `learnings/` directory:

```bash
cp -r ~/.openclaw/workspace/self-improving-agent/learnings/ /backup/location/
```

---

## 📝 License

MIT License

---

## 👨‍💻 Author

PocketAI for Leo - OpenClaw Community

---

## 🙏 Credits

- OpenClaw Team
- Self-Improving Agent Concept
- Python Community

---

**Happy Learning! 🚀**
