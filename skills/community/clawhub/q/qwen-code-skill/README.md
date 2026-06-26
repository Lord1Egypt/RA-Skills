<div align="center">

# 🦌 Qwen Code Skill

> 🚀 Alibaba Cloud Qwen Code CLI wrapper for OpenClaw. Execute tasks, review code, and automate workflows with AI-powered assistance.

**Author**: [@UserB1ank](https://github.com/UserB1ank)  
**Version**: v1.2.0  
**License**: MIT

[📝 Changelog](CHANGELOG.md) | [📦 Examples](assets/examples/)

</div>

---

## 📖 Overview

| | |
|---|---|
| **What it is** | OpenClaw tool wrapper for Alibaba Cloud Qwen Code CLI |
| **Pain it solves** | Integrates Qwen Code into OpenClaw workflows for task execution, code review, and automation |
| **Use in 30 seconds** | `scripts/qwen-code.js status` to check status, `scripts/qwen-code.js run "task"` to execute |

### ✨ Features

- 🎯 **Task Execution** - Run programming tasks with natural language
- 🔍 **Code Review** - Automated code analysis and suggestions
- 🤖 **Headless Mode** - JSON output for automation and CI/CD
- 🔌 **OpenClaw Integration** - Background execution, process management, model selection

---

## 🚀 Quick Start

### Prerequisites

```bash
# Node.js 20+
node --version

# Install Qwen Code CLI
npm install -g @qwen-code/qwen-code@latest

# Verify installation
qwen --version
```

### Authentication

```bash
# Option 1: OAuth (Recommended)
qwen auth login

# Option 2: API Key
export DASHSCOPE_API_KEY="sk-xxx"
```

### Basic Usage

```bash
# Check status
scripts/qwen-code.js status

# Run a task
scripts/qwen-code.js run "Create a Flask API"

# Code review
scripts/qwen-code.js review src/app.ts

# Headless mode (JSON output)
scripts/qwen-code.js headless "Analyze code" -o json
```

---

## 📋 Commands

| Command | Description | Example |
|---------|-------------|---------|
| `status` | Check Qwen Code status and authentication | `scripts/qwen-code.js status` |
| `run <task>` | Execute programming task | `scripts/qwen-code.js run "Create REST API"` |
| `review <file>` | Code review and analysis | `scripts/qwen-code.js review src/main.py` |
| `headless <task>` | Headless mode (JSON output) | `scripts/qwen-code.js headless "Analyze" -o json` |
| `help` | Show help information | `scripts/qwen-code.js help` |

---

## 🔌 OpenClaw Integration

### Background Execution

```bash
# Basic task
bash workdir:~/project background:true yieldMs:30000 \
  command:"qwen -p 'Create Python Flask API'"

# Specify model
bash workdir:~/project background:true yieldMs:30000 \
  command:"qwen -p 'Analyze code structure' -m qwen3-coder-plus"

# YOLO mode (auto-approve)
bash workdir:~/project background:true yieldMs:30000 \
  command:"qwen -p 'Refactor this function' -y"
```

### Process Management

```bash
# View logs
process action:log sessionId:XXX

# Check completion
process action:poll sessionId:XXX

# Send input (if Qwen asks)
process action:write sessionId:XXX data:"y"
```

### Headless Mode (Automation/CI/CD)

```bash
# JSON output
qwen -p "Analyze code structure" --output-format json

# Pipeline operations
git diff | qwen -p "Generate commit message"

# Batch processing
find src -name "*.ts" | xargs -I {} qwen -p "Review {}"
```

---

## 📁 Project Structure

```
qwen-code-skill/
├── SKILL.md                      # Skill definition (coding-agent format)
├── README.md                     # This file
├── CHANGELOG.md                  # Version history
├── _meta.json                    # Metadata
├── assets/
│   └── examples/                 # Example code
│       ├── basic-task.example.sh
│       ├── code-review.example.sh
│       ├── ci-cd.example.yml
│       └── headless-mode.example.js
├── scripts/
│   └── qwen-code.js              # Main script
└── references/
    └── qwen-cli-commands.md      # Command reference
```

---

## ✅ For / ❌ Not For

### ✅ For

- Developers using Qwen Code for programming tasks
- Teams needing code review and analysis
- Automation scripts and CI/CD integration
- OpenClaw Sub-Agent and Skills management
- Batch code analysis and refactoring

### ❌ Not For

- Environments without Qwen Code CLI installed
- GUI-based interaction requirements
- Non-Alibaba Cloud LLM users
- Offline environments (requires network connection)

---

## 🛡️ Security & Boundaries

| Component | Behavior | Executes Shell Commands? |
|-----------|----------|-------------------------|
| `scripts/qwen-code.js` | Wraps Qwen Code CLI commands | Yes (via `qwen` command) |
| `references/qwen-cli-commands.md` | Command reference documentation | No (plain text) |
| `assets/examples/` | Example code files | No (static files) |

### ⚠️ Security Notes

- This Skill does not execute code directly, only calls Qwen Code CLI
- All code generation and modifications require user confirmation
- Use review mode in production environments
- Disable YOLO mode for sensitive projects

---

## 📦 Examples

See [`assets/examples/`](assets/examples/) for complete examples:

| Example | Description |
|---------|-------------|
| `basic-task.example.sh` | Basic task execution |
| `code-review.example.sh` | Code review workflow |
| `ci-cd.example.yml` | GitHub Actions integration |
| `headless-mode.example.js` | Node.js automation example |

---

## 🔗 References

- [📖 Qwen Code Official Docs](https://qwenlm.github.io/qwen-code-docs/zh/)
- [📝 Command Reference](references/qwen-cli-commands.md)
- [📦 Example Code](assets/examples/)
- [🦌 OpenClaw Documentation](https://openclaw.ai)

---

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

### Latest: v1.2.0 (2026-02-27)

✨ **English-Only Refactoring**
- SKILL.md reformatted to coding-agent style
- All documentation in English
- Simplified structure for clarity
- Added troubleshooting section

### v1.1.0 (2026-02-27)

✨ **EvoMap Style Refactoring**
- Bilingual README support (EN/中文)
- Example code directory with 4 examples
- Complete command reference documentation
- Optimized SKILL.md structure

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for the OpenClaw Community**

[🔝 Back to Top](#-qwen-code-skill)

</div>
