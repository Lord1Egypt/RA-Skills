# 安装与初始化指南

> **目标**：最快 5 分钟完成环境准备，开始使用 SDD 工作流

---

## 🚀 快速开始（仅需智谱 Key）

### 一键配置

```bash
npx @z_ai/coding-helper
```

按提示输入智谱 API Key，自动完成 Claude Code 配置。

**官方文档**：[智谱 Coding Plan - Claude Code 配置指南](https://docs.bigmodel.cn/cn/coding-plan/tool/claude.md)

---

## ✅ 环境验证

```bash
# 运行环境检查脚本
~/.openclaw/skills/sdd-dev-workflow/scripts/check-environment.sh
```

---

## 📦 环境分层

### 最小环境（3 项 - 必需）

| 工具 | 版本要求 | 用途 | 安装 |
|------|---------|------|------|
| **Node.js** | 18+ | Claude Code 运行环境 | `brew install node` (macOS) / `apt install nodejs` (Ubuntu) |
| **Git** | 任意 | 版本控制 | 系统自带 |
| **智谱 Key** | - | LLM 服务 | [智谱开放平台获取](https://bigmodel.cn/usercenter/proj-mgmt/apikeys) |

**验证命令**：

```bash
node --version    # v18.x.x 或更高
git --version     # 任意版本
claude --version  # 通过 coding-helper 配置后可用
```

---

### 完整环境（+5 项 - 可选）

| 工具 | 版本要求 | 用途 | 是否必需 |
|------|---------|------|----------|
| **Python** | 3.11+ | 后端项目开发 | ⚪ 可选 |
| **UV** | 任意 | Python 包管理 | ⚪ 可选 |
| **tmux** | 3.0+ | 会话管理 | ⚪ 可选 |
| **specify-cli** | 最新 | 规范工具 | ⚪ 可选 |
| **GITHUB_TOKEN** | - | Speckit | ⚪ 可选 |

**说明**：
- **最小环境**即可运行 SDD 工作流
- **完整环境**用于 Python 后端项目、自动化 agent、Speckit 等高级功能

---

## 🔧 详细安装步骤

### 1. 安装 Node.js

**macOS**：

```bash
brew install node
```

**Ubuntu/Debian**：

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**验证**：

```bash
node --version
```

---

### 2. 安装 Claude Code + 智谱配置

**方式一：自动化助手（推荐）**

```bash
npx @z_ai/coding-helper
```

**方式二：手动安装**

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 配置智谱 Coding Plan
# 编辑 ~/.claude/settings.json
```

```json
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "your_zhipu_api_key",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-4.5-air",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-4.7",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5",
    "API_TIMEOUT_MS": "3000000",
    "CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC": "1"
  }
}
```

**验证**：

```bash
claude --version
```

**官方文档**：[智谱 Claude Code 配置指南](https://docs.bigmodel.cn/cn/coding-plan/tool/claude.md)

---

### 3. 安装 Git

**macOS**：系统自带

**Ubuntu/Debian**：

```bash
sudo apt-get install git
```

**验证**：

```bash
git --version
```

---

### 4. 安装 Python 3.11+（可选）

**Ubuntu/Debian**：

```bash
sudo apt-get install python3.11 python3.11-venv python3.11-dev
```

**macOS**：

```bash
brew install python@3.11
```

**验证**：

```bash
python3 --version
```

---

### 5. 安装 UV（可选）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**验证**：

```bash
uv --version
```

---

### 6. 安装 tmux（可选）

**Ubuntu/Debian**：

```bash
sudo apt-get install tmux
```

**macOS**：

```bash
brew install tmux
```

**验证**：

```bash
tmux -V
```

---

### 7. 安装 specify-cli（可选）

```bash
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

**验证**：

```bash
specify --help
```

---

## 📁 项目初始化

### 正式项目

```bash
~/.openclaw/skills/sdd-dev-workflow/scripts/init-project.sh my-project
cd ~/openclaw/workspace/projects/my-project
```

### 临时项目

```bash
~/.openclaw/skills/sdd-dev-workflow/scripts/init-project.sh test-xyz --tmp
cd ~/openclaw/workspace/tmp/test-xyz
```

### 手动初始化（如 specify 不可用）

```bash
# 创建目录结构
mkdir -p .specify/{specs,plans,tasks,context}
mkdir -p specs templates scripts

# 复制宪法模板
cp ~/.openclaw/skills/sdd-dev-workflow/templates/constitution-enterprise.md \
   .specify/memory/constitution.md
```

---

## 🔐 环境变量配置

### 必需环境变量

```bash
# 智谱 API Key（通过 coding-helper 自动配置）
# 无需手动设置
```

### 可选环境变量

```bash
# GitHub Token（用于 Speckit）
export GITHUB_TOKEN="your-github-token"
```

**注意**：如果需要 cron 任务，请自行配置 Gateway 环境变量（参考 OpenClaw 文档）。

---

## ❓ 常见安装问题

### Q: specify init 需要交互式确认？

**解决方案**：使用非交互模式

```bash
specify init . --here --ai claude --force --no-git
```

---

### Q: Claude Code 连接失败？

**错误**：`Unhandled stop reason: network_error`

**解决方案**：

```bash
# 检查 gateway 状态
openclaw gateway status

# 重启 gateway
openclaw gateway restart
```

---

### Q: python vs python3 问题？

**解决方案**：系统使用 `python3` 命令

```bash
# 使用 python3 而非 python
python3 --version
```

---

### Q: 外部 API 网络不可达？

**解决方案**：设置代理

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890
```

---

### Q: Claude Code v2.1.69 版本 BUG？

**解决方案**：设置环境变量

```bash
export ENABLE_TOOL_SEARCH=0
export CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1
```

参考：[Issue #30926](https://github.com/anthropics/claude-code/issues/30926)

---

## 🎯 推荐配置

### 新手推荐

- ✅ 最小环境（Node.js + Git + 智谱 Key）
- ✅ 使用 `coding-helper` 自动配置
- ⚪ 暂不安装可选工具

### 完整开发环境

- ✅ 最小环境
- ✅ Python 3.11+
- ✅ UV
- ✅ tmux
- ✅ specify-cli
- ✅ GITHUB_TOKEN

---

## 📚 参考文档

- [智谱 Coding Plan - Claude Code 配置指南](https://docs.bigmodel.cn/cn/coding-plan/tool/claude.md)
- [Claude Code 官方文档](https://docs.anthropic.com/claude-code)
- [Speckit GitHub](https://github.com/github/spec-kit)

---

**最后更新**: 2026-03-13
**版本**: v1.1
