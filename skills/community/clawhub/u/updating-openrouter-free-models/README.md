# OpenRouter Free Models Updater / OpenRouter免费模型更新器

[English](#english-version) | [中文版本](#中文版本)

---

## English Version

### Overview / 概述

An automated tool for fetching, testing, and managing free models from OpenRouter AI. This skill integrates with both Claude Code and OpenClaw to keep your free model configurations synchronized and validated automatically.

An automated tool for fetching, testing, and managing free models from OpenRouter AI. This skill integrates with both Claude Code and OpenClaw to keep your free model configurations synchronized and validated automatically.

**🎯 Purpose / 目的:**
- Automatically fetch all free models from OpenRouter API
- Batch test each model's availability before adding to config
- Synchronize configurations between Claude Code and OpenClaw
- Ensure only working models are added, with fallbacks configured

### Features / 功能特点

✅ **Automated Fetching** - Retrieves free models from OpenRouter API with intelligent filtering
✅ **Batch Testing** - Tests each model with a short API call to verify availability
✅ **Dual Config Support** - Updates both Claude Code (`settings.json`) and OpenClaw (`openclaw.json`)
✅ **Fallback Management** - Configures model fallbacks for reliability
✅ **Validation Built-in** - JSON syntax checking and self-tests
✅ **Service Integration** - Includes OpenClaw restart script for config reload

### Quick Start / 快速开始

#### Prerequisites / 前置要求

- Python 3.8+
- Node.js (for OpenClaw config updates)
- OpenRouter API key (set as `OPENROUTER_API_KEY` or in config)
- OpenClaw installed (optional, for OpenClaw integration)

#### Installation / 安装

```bash
# Clone or copy the skill files to your workspace
cd ~/.openclaw/workspace/skills/  # For OpenClaw
# or
cd ~/.claude/skills/              # For Claude Code

# Place all files in a directory: updating-openrouter-free-models/
```

#### Usage / 使用方法

**可以直接复制以下 prompt 给 Claude Code 或 OpenClaw，AI 会自动完成安装:**

<details>
<summary><strong>📋 Click to copy Claude Code installation prompt</strong></summary>

```
I have the updating-openrouter-free-models skill files in the current directory. Please install this skill for Claude Code by:

1. Creating the skill directory at ~/.claude/skills/updating-openrouter-free-models/
2. Copying all files from current directory to that location
3. Setting correct permissions (chmod +x for .sh files)
4. Verifying installation by running: python3 fetch_models.py && python3 test_models.py
5. Showing me the installation summary

Current directory files:
- SKILL.md
- INSTALLATION.md
- fetch_models.py
- test_models.py
- apply_updates.py
- apply_updates_openclaw.js
- restart_openclaw.sh
- test-skill.sh
- complete_test.sh

Please install all files and confirm the skill is ready to use.
```
</details>

<details>
<summary><strong>📋 Click to copy OpenClaw installation prompt</strong></summary>

```
I have the updating-openrouter-free-models skill files in the current directory. Please install this skill for OpenClaw by:

1. Creating the skill directory at ~/.openclaw/workspace/skills/updating-openrouter-free-models/
2. Copying all files from current directory to that location
3. Setting executable permissions on all .sh files
4. Running the complete test: ./complete_test.sh
5. Showing me the installation summary with model count

Current directory files:
- SKILL.md
- INSTALLATION.md
- fetch_models.py
- test_models.py
- apply_updates_openclaw.js
- restart_openclaw.sh
- test-skill.sh
- complete_test.sh

Please install and verify the skill works correctly.
```
</details>

**Full Workflow / 完整流程:**

```bash
# 1. Fetch all free models from OpenRouter
python3 fetch_models.py

# 2. Test each model's availability
python3 test_models.py

# 3. Apply updates to configurations
# For Claude Code:
python3 apply_updates.py

# For OpenClaw:
node apply_updates_openclaw.js

# 4. (OpenClaw only) Restart the service
./restart_openclaw.sh

# 5. Validate
python3 -m json.tool ~/.claude/settings.json  # Claude
python3 -m json.tool ~/.openclaw/openclaw.json  # OpenClaw
```

**One-Command Test / 一键测试:**

```bash
./complete_test.sh  # Runs full workflow with sample models
```

### How It Works / 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                    Update Process                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐     ┌──────────────────┐            │
│  │ Fetch Models     │────▶│ Test Availability│            │
│  │ from OpenRouter  │     │ (API Call)       │            │
│  └──────────────────┘     └──────────────────┘            │
│          │                         │                       │
│          ▼                         ▼                       │
│  /tmp/free_models.txt        /tmp/verified_models.txt    │
│  (All free models)           (Only working models)       │
│                                                             │
│                          ┌──────────────────┐            │
│                          │ Update Configs   │            │
│                          │ - Claude Code    │            │
│                          │ - OpenClaw       │            │
│                          └──────────────────┘            │
│                                    │                       │
│                                    ▼                       │
│                          ~/.claude/settings.json         │
│                          ~/.openclaw/openclaw.json       │
│                                                             │
│                          ┌──────────────────┐            │
│                          │ Restart Service  │            │
│                          │ (OpenClaw only)  │            │
│                          └──────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### File Structure / 文件结构

```
updating-openrouter-free-models/
├── SKILL.md                    # Detailed skill documentation
├── INSTALLATION.md             # Installation instructions
├── fetch_models.py             # Fetch free models from OpenRouter API
├── test_models.py              # Batch test model availability
├── apply_updates.py            # Python config updater (Claude Code)
├── apply_updates_openclaw.js  # Node.js config updater (OpenClaw)
├── restart_openclaw.sh         # OpenClaw service restart script
├── test-skill.sh               # Skill integration test
└── complete_test.sh            # Full workflow test script
```

### Key Components / 核心组件

#### 1. Fetch Script (`fetch_models.py`)
- Queries OpenRouter API: `https://openrouter.ai/api/v1/models`
- Identifies free models by:
  - `:free` suffix in model ID
  - All pricing fields (`prompt`, `completion`, `request`) equal to `0`
- Outputs to `/tmp/free_models.txt`

#### 2. Test Script (`test_models.py`)
- Reads models from `/tmp/free_models.txt`
- Sends test API requests (5 tokens) to each model
- Records verified models to `/tmp/verified_models.txt`
- Records failed models to `/tmp/failed_models.txt` with error reasons

#### 3. Config Updaters
- **Python** (`apply_updates.py`): Updates Claude Code `settings.json`
- **Node.js** (`apply_updates_openclaw.js`): Updates OpenClaw `openclaw.json`
- Updates three sections:
  - `providers.openrouter.models` - model provider configuration
  - `agents.defaults.model.fallbacks` - fallback chain
  - `agents.defaults.models` - model-specific settings

#### 4. Restart Script (`restart_openclaw.sh`)
- Restarts OpenClaw gateway service
- Tries multiple methods: `launchctl`, `pkill` + `nohup`
- Logs: `/tmp/openclaw-gateway.log`

### Configuration Format / 配置格式

#### Claude Code (`~/.claude/settings.json`)

```json
{
  "availableModels": [
    "openrouter/hunter-alpha:free",
    "openrouter/arcee-ai/trinity-large-preview:free",
    ...
  ]
}
```

#### OpenClaw (`~/.openclaw/openclaw.json`)

```json
{
  "models": {
    "providers": {
      "openrouter": {
        "models": [
          { "id": "openrouter/hunter-alpha:free", "name": "hunter-alpha", "api": "openai-completions" },
          ...
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/stepfun/step-3.5-flash:free",
        "fallbacks": [
          "openrouter/arcee-ai/trinity-large-preview:free",
          ...
        ]
      },
      "models": {
        "openrouter/stepfun/step-3.5-flash:free": {},
        "openrouter/arcee-ai/trinity-large-preview:free": {},
        ...
      }
    }
  }
}
```

### Environment Variables / 环境变量

For authentication with OpenRouter API:

- `OPENROUTER_API_KEY` - Your OpenRouter API key (recommended)
- `ANTHROPIC_AUTH_TOKEN` - Claude Code compatibility mode

The scripts will automatically detect and use whichever is available.

### Testing / 测试

**Run the test suite:**

```bash
# Quick integration test
./test-skill.sh

# Full workflow test
./complete_test.sh

# Manual verification
python3 fetch_models.py && python3 test_models.py
cat /tmp/verified_models.txt
```

**Test Checklist / 测试清单:**

- [ ] Fetch produces non-empty model list
- [ ] All verified models pass batch API test
- [ ] Claude settings JSON is valid
- [ ] OpenClaw JSON is valid (if used)
- [ ] `availableModels` exists and is array in Claude settings
- [ ] OpenClaw `providers.openrouter.models` contains models
- [ ] OpenClaw `agents.defaults.model.fallbacks` includes all except primary
- [ ] OpenClaw `agents.defaults.models` has entries for all verified models
- [ ] Actual API call works with at least one model from the updated list

### Maintenance / 维护

**Recommended Frequency / 建议频率:**
- Run monthly - OpenRouter frequently adds/removes free models
- After encountering API errors with specific models
- Before major deployments to ensure model availability

**What gets updated each run:**
- Primary model list (from `:free` tag or zero pricing)
- Verified working models only (failed ones excluded)
- Fallback chain (auto-generated, excludes primary)
- Model entries in agent defaults

### Troubleshooting / 故障排除

#### "Permission denied" on scripts
```bash
chmod +x restart_openclaw.sh test-skill.sh complete_test.sh
```

#### OpenClaw config not found
- Check file exists: `ls ~/.openclaw/openclaw.json`
- If missing, run: `openclaw configure`

#### Restart fails
```bash
# Check if already running
pgrep -f "openclaw.*gateway"

# Manual restart
openclaw gateway

# Check logs
tail -f /tmp/openclaw-gateway.log
```

#### Models not appearing after update
1. Did you restart OpenClaw? (Required for config changes)
2. Check JSON syntax: `python3 -m json.tool ~/.openclaw/openclaw.json`
3. Verify `provider.models` array contains your models
4. Verify `agents.defaults.models` has entries for all models

#### API rate limits
The script includes 0.5s delay between tests. If you hit rate limits:
- Increase `time.sleep(1.0)` in `test_models.py` line 112
- Run the script during off-peak hours

### Differences: Claude Code vs OpenClaw / 差异对比

| Aspect / 方面 | Claude Code | OpenClaw |
|--------------|-------------|----------|
| Config file / 配置文件 | `~/.claude/settings.json` | `~/.openclaw/openclaw.json` |
| Field name / 字段名 | `availableModels` | `providers.openrouter.models` |
| Fallback support / 回退支持 | Native (auto) | Explicit `agents.defaults.model.fallbacks` |
| Restart required / 需重启 | No (hot reload) | **Yes** (gateway restart) |
| Script language / 脚本语言 | Python | Node.js primary + Python |
| Config format / 配置格式 | Simple array | Nested objects (provider + agents) |
| Alias support / 别名支持 | No | Yes |

### Best Practices / 最佳实践

1. **Always test before applying** - Review `/tmp/failed_models.txt` to understand which models failed
2. **Set primary model strategically** - Choose the most reliable model as primary (edit `apply_updates_openclaw.js` line 23)
3. **Regular updates** - Run monthly to keep model list current
4. **Keep backups** - Backup your config files before updates:
   ```bash
   cp ~/.claude/settings.json ~/.claude/settings.json.backup
   cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup
   ```
5. **Monitor logs** - Check `/tmp/openclaw-gateway.log` after restart
6. **Don't skip self-tests** - Always run validation commands before considering update complete

### Common Pitfalls / 常见问题

| Issue / 问题 | Symptom / 症状 | Solution / 解决方案 |
|-------------|----------------|-------------------|
| Missing rate limiting / 缺少限流 | API errors, timeouts | Increase sleep duration in `test_models.py` |
| Duplicate models / 重复模型 | Same model twice in config | Script uses `set()` to deduplicate automatically |
| Forgetting fallbacks / 忘记配置回退 | Only primary model works | Script auto-generates fallbacks from verified list |
| Invalid JSON / JSON语法错误 | Config won't load | Run `python3 -m json.tool` to validate syntax |
| Skipping restart (OpenClaw) / 跳过重启 | Changes not taking effect | Always run `./restart_openclaw.sh` for OpenClaw |

### License / 许可证

This skill is provided as-is for use with Claude Code and OpenClaw.

### Support / 支持

- **Documentation:** See `SKILL.md` in this directory
- **Installation Guide:** See `INSTALLATION.md` in this directory
- **Issues:** Report issues with detailed error logs from `/tmp/openclaw-gateway.log`
- **OpenRouter API Docs:** https://openrouter.ai/docs
- **Claude Code:** https://claude.ai/code
- **OpenClaw:** Check your OpenClaw installation docs

---

## 中文版本

### 概述

自动化工具，用于从 OpenRouter AI 获取、测试和管理免费模型。该技能与 Claude Code 和 OpenClaw 集成，自动保持您的免费模型配置同步和验证。

**🎯 目的:**
- 自动从 OpenRouter API 获取所有免费模型
- 批量测试每个模型的可用性，然后再添加到配置中
- 在 Claude Code 和 OpenClaw 之间同步配置
- 确保只添加可用的模型，并配置回退机制

### 功能特点

✅ **自动获取** - 智能筛选从 OpenRouter API 获取免费模型
✅ **批量测试** - 通过简短 API 调用测试每个模型的可用性
✅ **双配置支持** - 同时更新 Claude Code (`settings.json`) 和 OpenClaw (`openclaw.json`)
✅ **回退管理** - 配置模型回退以提高可靠性
✅ **内置验证** - JSON 语法检查和自检
✅ **服务集成** - 包含 OpenClaw 重启脚本以重新加载配置

### 快速开始

#### 前置要求

- Python 3.8+
- Node.js (用于 OpenClaw 配置更新)
- OpenRouter API 密钥 (设置为 `OPENROUTER_API_KEY` 或在配置中)
- 已安装 OpenClaw (可选，用于 OpenClaw 集成)

#### 安装

```bash
# 克隆或将技能文件复制到您的工作区
cd ~/.openclaw/workspace/skills/  # 用于 OpenClaw
# 或
cd ~/.claude/skills/              # 用于 Claude Code

# 将所有文件放在目录中: updating-openrouter-free-models/
```

#### 使用方法

**可以直接复制以下 prompt 给 Claude Code 或 OpenClaw，AI 会自动完成安装:**

<details>
<summary><strong>📋 点击复制 Claude Code 安装提示</strong></summary>

```
I have the updating-openrouter-free-models skill files in the current directory. Please install this skill for Claude Code by:

1. Creating the skill directory at ~/.claude/skills/updating-openrouter-free-models/
2. Copying all files from current directory to that location
3. Setting correct permissions (chmod +x for .sh files)
4. Verifying installation by running: python3 fetch_models.py && python3 test_models.py
5. Showing me the installation summary

Current directory files:
- SKILL.md
- INSTALLATION.md
- fetch_models.py
- test_models.py
- apply_updates.py
- apply_updates_openclaw.js
- restart_openclaw.sh
- test-skill.sh
- complete_test.sh

Please install all files and confirm the skill is ready to use.
```
</details>

<details>
<summary><strong>📋 点击复制 OpenClaw 安装提示</strong></summary>

```
I have the updating-openrouter-free-models skill files in the current directory. Please install this skill for OpenClaw by:

1. Creating the skill directory at ~/.openclaw/workspace/skills/updating-openrouter-free-models/
2. Copying all files from current directory to that location
3. Setting executable permissions on all .sh files
4. Running the complete test: ./complete_test.sh
5. Showing me the installation summary with model count

Current directory files:
- SKILL.md
- INSTALLATION.md
- fetch_models.py
- test_models.py
- apply_updates_openclaw.js
- restart_openclaw.sh
- test-skill.sh
- complete_test.sh

Please install and verify the skill works correctly.
```
</details>

**一键测试:**

```bash
./complete_test.sh  # 使用示例模型运行完整工作流
```

### 工作原理

```
┌─────────────────────────────────────────────────────────────┐
│                    更新流程                                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────────┐     ┌──────────────────┐            │
│  │ 从 OpenRouter    │────▶│ 测试可用性        │            │
│  │ 获取模型         │     │ (API 调用)       │            │
│  └──────────────────┘     └──────────────────┘            │
│          │                         │                       │
│          ▼                         ▼                       │
│  /tmp/free_models.txt        /tmp/verified_models.txt    │
│  (所有免费模型)              (仅工作模型)                 │
│                                                             │
│                          ┌──────────────────┐            │
│                          │ 更新配置          │            │
│                          │ - Claude Code    │            │
│                          │ - OpenClaw       │            │
│                          └──────────────────┘            │
│                                    │                       │
│                                    ▼                       │
│                          ~/.claude/settings.json         │
│                          ~/.openclaw/openclaw.json       │
│                                                             │
│                          ┌──────────────────┐            │
│                          │ 重启服务          │            │
│                          │ (仅 OpenClaw)    │            │
│                          └──────────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### 文件结构

```
updating-openrouter-free-models/
├── SKILL.md                    # 详细技能文档
├── INSTALLATION.md             # 安装说明
├── fetch_models.py             # 从 OpenRouter API 获取免费模型
├── test_models.py              # 批量测试模型可用性
├── apply_updates.py            # Python 配置更新器 (Claude Code)
├── apply_updates_openclaw.js  # Node.js 配置更新器 (OpenClaw)
├── restart_openclaw.sh         # OpenClaw 服务重启脚本
├── test-skill.sh               # 技能集成测试
└── complete_test.sh            # 完整工作流测试脚本
```

### 核心组件

#### 1. 获取脚本 (`fetch_models.py`)
- 查询 OpenRouter API: `https://openrouter.ai/api/v1/models`
- 通过以下方式识别免费模型:
  - 模型 ID 包含 `:free` 后缀
  - 所有定价字段 (`prompt`, `completion`, `request`) 等于 `0`
- 输出到 `/tmp/free_models.txt`

#### 2. 测试脚本 (`test_models.py`)
- 从 `/tmp/free_models.txt` 读取模型
- 向每个模型发送测试 API 请求 (5 tokens)
- 记录已验证的模型到 `/tmp/verified_models.txt`
- 记录失败的模型到 `/tmp/failed_models.txt`，包含错误原因

#### 3. 配置更新器
- **Python** (`apply_updates.py`): 更新 Claude Code `settings.json`
- **Node.js** (`apply_updates_openclaw.js`): 更新 OpenClaw `openclaw.json`
- 更新三个部分:
  - `providers.openrouter.models` - 模型提供者配置
  - `agents.defaults.model.fallbacks` - 回退链
  - `agents.defaults.models` - 模型特定设置

#### 4. 重启脚本 (`restart_openclaw.sh`)
- 重启 OpenClaw 网关服务
- 尝试多种方法: `launchctl`, `pkill` + `nohup`
- 日志: `/tmp/openclaw-gateway.log`

### 配置格式

#### Claude Code (`~/.claude/settings.json`)

```json
{
  "availableModels": [
    "openrouter/hunter-alpha:free",
    "openrouter/arcee-ai/trinity-large-preview:free",
    ...
  ]
}
```

#### OpenClaw (`~/.openclaw/openclaw.json`)

```json
{
  "models": {
    "providers": {
      "openrouter": {
        "models": [
          { "id": "openrouter/hunter-alpha:free", "name": "hunter-alpha", "api": "openai-completions" },
          ...
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/stepfun/step-3.5-flash:free",
        "fallbacks": [
          "openrouter/arcee-ai/trinity-large-preview:free",
          ...
        ]
      },
      "models": {
        "openrouter/stepfun/step-3.5-flash:free": {},
        "openrouter/arcee-ai/trinity-large-preview:free": {},
        ...
      }
    }
  }
}
```

### 环境变量

用于 OpenRouter API 的身份验证:

- `OPENROUTER_API_KEY` - 您的 OpenRouter API 密钥 (推荐)
- `ANTHROPIC_AUTH_TOKEN` - Claude Code 兼容模式

脚本会自动检测并使用其中任何一个可用的密钥。

### 测试

**运行测试套件:**

```bash
# 快速集成测试
./test-skill.sh

# 完整工作流测试
./complete_test.sh

# 手动验证
python3 fetch_models.py && python3 test_models.py
cat /tmp/verified_models.txt
```

**测试清单:**

- [ ] 获取生成非空的模型列表
- [ ] 所有验证通过的模型都通过批量 API 测试
- [ ] Claude 设置 JSON 有效
- [ ] OpenClaw JSON 有效 (如使用)
- [ ] Claude 设置中包含 `availableModels` 且为数组
- [ ] OpenClaw `providers.openrouter.models` 包含模型
- [ ] OpenClaw `agents.defaults.model.fallbacks` 包含除主模型外的所有模型
- [ ] OpenClaw `agents.defaults.models` 包含所有验证模型的条目
- [ ] 实际 API 调用能使用更新列表中的至少一个模型获得响应

### 维护

**建议频率 / 建议频率:**
- 每月运行一次 - OpenRouter 频繁添加/删除免费模型
- 遇到特定模型的 API 错误后
- 在主要部署前确保模型可用性

**每次运行更新的内容:**
- 主模型列表 (来自 `:free` 标签或零定价)
- 仅验证通过的模型 (失败的被排除)
- 回退链 (自动生成，排除主模型)
- 代理默认值中的模型条目

### 故障排除

#### "Permission denied" on scripts / 脚本权限被拒绝
```bash
chmod +x restart_openclaw.sh test-skill.sh complete_test.sh
```

#### OpenClaw 配置文件未找到
- 检查文件是否存在: `ls ~/.openclaw/openclaw.json`
- 如果缺失，运行: `openclaw configure`

#### 重启失败
```bash
# 检查是否已在运行
pgrep -f "openclaw.*gateway"

# 手动重启
openclaw gateway

# 检查日志
tail -f /tmp/openclaw-gateway.log
```

#### 更新后模型未出现
1. 您重启 OpenClaw 了吗? (配置更改需要重启)
2. 检查 JSON 语法: `python3 -m json.tool ~/.openclaw/openclaw.json`
3. 验证 `provider.models` 数组包含您的模型
4. 验证 `agents.defaults.models` 包含所有模型的条目

#### API 速率限制
脚本在测试之间包含 0.5 秒延迟。如果您遇到速率限制:
- 在 `test_models.py` 第 112 行增加 `time.sleep(1.0)`
- 在非高峰时段运行脚本

### Claude Code 与 OpenClaw 差异对比

| 方面 | Claude Code | OpenClaw |
|------|-------------|----------|
| 配置文件 | `~/.claude/settings.json` | `~/.openclaw/openclaw.json` |
| 字段名 | `availableModels` | `providers.openrouter.models` |
| 回退支持 | 原生 (自动) | 显式 `agents.defaults.model.fallbacks` |
| 是否需要重启 | 否 (热重载) | **是** (网关重启) |
| 脚本语言 | Python | Node.js 为主 + Python |
| 配置格式 | 简单数组 | 嵌套对象 (提供者 + 代理) |
| 别名支持 | 否 | 是 |

### 最佳实践

1. **始终先测试后应用** - 查看 `/tmp/failed_models.txt` 了解哪些模型失败
2. **战略性选择主模型** - 选择最可靠的模型作为主模型 (编辑 `apply_updates_openclaw.js` 第 23 行)
3. **定期更新** - 每月运行一次以保持模型列表最新
4. **保留备份** - 在更新前备份配置文件:
   ```bash
   cp ~/.claude/settings.json ~/.claude/settings.json.backup
   cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup
   ```
5. **监控日志** - 重启后检查 `/tmp/openclaw-gateway.log`
6. **不要跳过自检** - 完成更新前始终运行验证命令

### 常见问题

| 问题 | 症状 | 解决方案 |
|------|------|----------|
| 缺少限流 / 缺少限流 | API 错误, 超时 | 在 `test_models.py` 中增加 sleep 持续时间 |
| 重复模型 / 重复模型 | 配置中出现相同的模型两次 | 脚本使用 `set()` 自动去重 |
| 忘记配置回退 / 忘记配置回退 | 只有主模型工作 | 脚本从验证列表自动生成回退 |
| JSON 无效 / JSON无效 | 配置无法加载 | 运行 `python3 -m json.tool` 验证语法 |
| 跳过重启 (OpenClaw) / 跳过重启 | 更改未生效 | OpenClaw 始终运行 `./restart_openclaw.sh` |

### License / 许可证

本技能按原样提供，用于 Claude Code 和 OpenClaw。

### Support / 支持

- **文档:** 查看此目录中的 `SKILL.md`
- **安装指南:** 查看此目录中的 `INSTALLATION.md`
- **问题报告:** 提供详细的错误日志，来自 `/tmp/openclaw-gateway.log`
- **OpenRouter API 文档:** https://openrouter.ai/docs
- **Claude Code:** https://claude.ai/code
- **OpenClaw:** 查看您的 OpenClaw 安装文档

---

**Project Version / 项目版本:** 1.0.0
**Last Updated / 最后更新:** 2025-03-16
**Compatible with / 兼容:** Claude Code + OpenClaw
**Language / 语言:** Python 3.8+, Node.js
**License / 许可证:** MIT (assumed)
