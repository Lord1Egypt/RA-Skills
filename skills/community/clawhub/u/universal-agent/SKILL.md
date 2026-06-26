---
name: universal-agent
author: 王教成 Wang Jiaocheng (波动几何)
description: >
  This skill should be used when the user needs to execute tasks through a complete 
  automated workflow: understand natural language intent, dynamically generate commands 
  or Python scripts, auto-execute them via shell, and summarize results. This is a 
  minimal universal agent implementation based on "LLM brain + command executor limbs" 
  architecture. Use this when users say things like "help me do X automatically", 
  "generate code and run it", "universal agent", "execute task end-to-end", or when 
  tasks require dynamic code generation and execution with automatic error recovery.
---

# Universal Agent Skill

A minimal universal AI agent that automates end-to-end task execution: understand user intent in natural language, generate commands or scripts, execute them, analyze results, and self-recover from errors.

## Architecture

```
Natural Language Input
       ↓
  ┌─────────────┐
  │ LLM (Brain) │ Understand intent, generate command/Python script
  └──────┬──────┘
         │ Auto-generate code/command
         ↓
  ┌─────────────────┐
  │ Command Executor │ Execute any command, control software & hardware
  │ (Limbs)          │
  └───────┬─────────┘
          │ Actual execution
          ↓
     Task Complete ✅
```

## File Structure

```
universal-agent/
├── SKILL.md                    # This file (skill definition)
├── scripts/
│   ├── universal_agent.py      # Main program (complete standalone implementation)
│   └── config.json             # Configuration file (fill in API key for standalone mode)
└── references/
    └── README.md               # Detailed usage documentation
```

## When to Use

Use this skill when:

- User describes a task in natural language that requires automated execution
- Task needs dynamic code generation (Python script) and immediate execution
- Task involves file operations, data processing, system administration, CLI tools, API calls
- User wants end-to-end automation without manual intervention
- Keywords: "万能agent", "universal agent", "自动执行", "动态生成代码", "生成并执行", "帮我做XX"

## How It Works

### Automated Workflow (4 Steps)

1. **Think** — LLM understands task, judges complexity, decides whether to generate a shell command or Python script
2. **Execute** — Auto-write file → Run command/script → Capture output
3. **Fix** — On error, LLM analyzes error, auto-fixes code, retries (up to 2 times)
4. **Summarize** — Translates technical output into human-friendly language

### Why It's "Universal"

| Capability | Description |
|------------|-------------|
| Shell Commands | File ops, process management, system admin |
| Python Scripts | Data processing, web scraping, ML, image processing |
| CLI Tools | git, docker, ffmpeg, aws, any CLI |
| Hardware Control | Serial/GPIO/network-controlled physical devices |
| API Calls | Any HTTP API |

**Command executor can run Python → Python can do anything → Agent can do anything**

## Usage Modes

This skill supports **three** distinct usage modes, each suited to different scenarios:

### Mode 1: Standalone (独立运行)

Run the bundled script directly as an independent program. The script handles everything internally — LLM calls, command execution, safety checks, retries, memory.

```bash
# Single task mode (needs API key)
python scripts/universal_agent.py --run "task description"

# Interactive mode
python scripts/universal_agent.py

# With environment variables
set LLM_API_KEY=sk-xxx && python scripts/universal_agent.py --run "任务"
```

**What works:** Safety ✅ | Auto-retry ✅ | Memory persistence ✅ | Needs API Key.

---

### Mode 2: Bridge Execution (桥接执行 — 推荐)

Execute the script with `--backend bridge`. The script's **brain is provided by the external Agent** that loaded this Skill, while the script itself handles **execution, safety, retry, and memory**. Any Agent with LLM + command execution can use this.

```bash
# Basic bridge execution
python scripts/universal_agent.py --backend bridge --run "任务描述"

# View full protocol spec
python scripts/universal_agent.py --bridge-info
```

**How it works — the Agent drives the script through environment variables:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Bridge Mode Flow                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ① User: "列出当前目录的文件"                                │
│       ↓                                                     │
│  ② External Agent LLM → generates decision                  │
│     set UA_THINK={"type":"command","content":"dir /b"}      │
│       ↓                                                     │
│  ③ Agent executes:                                          │
│     python ... --backend bridge --run "列出当前目录的文件"   │
│       ↓                                                     │
│  ④ Script reads UA_THINK → runs "dir /b"                    │
│     → safety check passes → captures output                 │
│       ↓ (if error)                                          │
│  ⑤ Script requests fix via UA_DEBUG_AND_FIX env var         │
│       ↓                                                     │
│  ⑥ External Agent provides fixed code                       │
│     set UA_DEBUG_AND_FIX="fixed_command_or_script"           │
│       ↓                                                     │
│  ⑦ Script re-executes → success                             │
│       ↓                                                     │
│  ⑧ Script reads UA_SUMMARIZE for final output               │
│     → returns structured JSON result                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Environment Variable Protocol:**

| Variable | When Used | Format |
|----------|----------|--------|
| `UA_THINK` | Step 1 — decision | JSON: `{"type":"command\|script","content":"...","explanation":"..."}` |
| `UA_GENERATE_SCRIPT` | If type=script and code needed | Complete Python source code |
| `UA_SUMMARIZE` | Final step — result summary | Natural language summary text |
| `UA_DEBUG_AND_FIX` | On error retry — fixed code | Fixed Python/shell code |

**What works:** Safety ✅ | Auto-retry ✅ | Memory persistence ✅ | **No API Key needed** (Agent provides LLM).

**Who can use this:** WorkBuddy, Cursor, Continue.dev, Aider, Cline, any AI IDE/tool with LLM + shell access.

---

### Mode 3: Inline Simulation (模拟执行)

The loaded Agent reads this SKILL.md, learns the architecture pattern, and **simulates the workflow using its own native capabilities** without executing the script at all. The script serves as a reference/teaching example only.

- Agent uses its own LLM instead of `LLMBrain`
- Agent uses its own `execute_command` instead of `UniversalExecutor`
- Agent does its own summarization

**What works:** Fastest ⚡ | No setup | **Safety ❌ Retry ❌ Memory ❌** (script features unused).

## Core Components

### `scripts/universal_agent.py` — Main Program

Four core classes implementing the full agent:

| Class | Role | Key Methods |
|-------|------|-------------|
| `LLMBrain` | Brain — HTTP LLM interface (Mode 1) | `think()`, `generate_script()`, `summarize()`, `debug_and_fix()` |
| `AgentBridge` | Brain — External Agent bridge (Mode 2) | `think()`, `generate_script()`, `summarize()`, `debug_and_fix()`, `set_response()` |
| `UniversalExecutor` | Limbs (command execution) | `execute()`, `_execute_command()`, `_execute_script()`, `_check_danger()` |
| `ContextManager` | Memory (state management) | `add_task_record()`, `get_context_string()`, `save()/load()` |
| `UniversalAgent` | Main orchestrator | `run()`, `chat()`, `batch_run()` |

See `references/README.md` for full API documentation and examples.

### Safety Mechanisms

The executor includes built-in danger detection:

| Level | Examples | Handling |
|-------|----------|----------|
| 🔴 High | `rm -rf /`, `format C:` | **Forced confirmation required** |
| 🟡 Medium | `pip uninstall`, `sudo` | Warning prompt |
| 🟢 Low | `ls`, `cat`, `python script.py` | Direct execution |

Danger patterns are defined in `HIGH_DANGER_PATTERNS` and `MEDIUM_DANGER_PATTERNS` within the script.

## Configuration

### Mode 1 (Standalone) — Needs API Key

**Option A — Config File:**
Edit `scripts/config.json` and fill in your API key.

**Option B — Environment Variables:**
```bash
set LLM_API_KEY=your-key-here
set LLM_MODEL=gpt-4o
set LLM_BASE_URL=https://api.openai.com/v1
```

**Option C — Local Ollama (Free):**
```bash
ollama run llama3
# Then select ollama_llama3 preset when starting the script
```

Configuration priority: Environment variables > config.json > Interactive input.

### Mode 2 (Bridge) — No API Key Needed

The external Agent provides all LLM capabilities. Configure only optional settings:
```bash
# Optional: change input source from env to file
set UA_INPUT_SOURCE=file

# Optional: skip safety confirmations (not recommended)
# Use --dangerous flag instead
```

### Mode 3 (Simulation) — No Configuration Needed

Agent uses its own native capabilities. Nothing to configure.

## Supported LLM Providers

| Provider | Models | base_url |
|----------|--------|----------|
| OpenAI | gpt-4o, gpt-4o-mini | https://api.openai.com/v1 |
| DeepSeek | deepseek-chat, deepseek-reasoner | https://api.deepseek.com |
| Qwen | qwen-max, qwen-turbo | https://dashscope.aliyuncs.com/compatible-mode/v1 |
| Zhipu GLM | glm-4-plus | https://open.bigmodel.cn/api/paas/v4 |
| Local Ollama | llama3, qwen2, any model | http://localhost:11434/v1 |
| Groq | llama-3.1-70b-versatile | https://api.groq.com/openai/v1 |
| Any OpenAI-compatible API | any | your-url |

## Platform Support

✅ **Cross-platform** — Windows, macOS, Linux:

| OS | Shell Backend |
|----|--------------|
| Windows | `cmd.exe /c` (with `CREATE_NO_WINDOW`) |
| macOS | `bash` (`shell=True`) |
| Linux | `bash` (`shell=True`) |

All file I/O uses UTF-8 encoding. Python script execution uses `sys.executable` for platform-agnostic invocation.

## Dependencies

✅ **Zero external dependencies** — Python standard library only:
- `os`, `sys` — System operations
- `subprocess` — Command execution
- `json`, `re` — JSON parsing and regex
- `time/datetime` — Time handling
- `urllib` — HTTP requests (fallback)

Optional:
- `requests` library — Better HTTP support (`pip install requests`)

## Free Options

1. **Ollama + local model** (completely free, unlimited, private)
2. **DeepSeek** (~¥1/million tokens, excellent cost-performance)
3. **Groq Cloud** (free tier available, ultra-fast inference)
