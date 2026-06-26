# 依赖安装指南

本文档定义 SDD 工作流中的依赖自动安装策略，确保开发过程不被工具问题打断。

---

## 核心原则

> **完成开发，不为工具停顿**

- ✅ 遇到缺失依赖 → **立即安装**，不询问
- ✅ 安装失败 → 自动重试或降级方案
- ✅ 两层依赖策略 → 可预测的预装 + 按需安装

---

## 两层依赖策略

### Layer 1: 预装依赖（零注意力）

**定义**：开发环境中**必须**预先安装的工具

| 工具 | 用途 | 安装命令 |
|------|------|----------|
| **Python 3.11+** | 运行环境 | `apt install python3.11` |
| **Git** | 版本控制 | `apt install git` |
| **UV** | 包管理器 | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| **tmux 3.0+** | 会话管理 | `apt install tmux` |
| **Claude Code** | 代码生成 | `npm install -g @anthropic-ai/claude-code` |

**验证命令**：

```bash
# 一键检查所有预装依赖
~/.openclaw/skills/sdd-dev-workflow/scripts/check-environment.sh
```

### Layer 2: 按需安装（自动处理）

**定义**：项目特定依赖，遇到时自动安装

| 触发条件 | 自动安装命令 |
|---------|-------------|
| `ModuleNotFoundError: No module named 'fastapi'` | `pip install fastapi` |
| `ModuleNotFoundError: No module named 'pydantic'` | `pip install pydantic` |
| `command not found: pytest` | `pip install pytest` |
| `command not found: uvicorn` | `pip install uvicorn` |

**自动化脚本**：

```bash
# 检测到 ModuleNotFoundError 时自动执行
detect_and_install() {
  local error_msg="$1"

  # 提取模块名
  module=$(echo "$error_msg" | grep -oP "No module named '\K[^']+")

  if [ -n "$module" ]; then
    echo "⚠️ 检测到缺失模块: $module"
    echo "📦 自动安装: pip install $module"
    pip install "$module"
    echo "✅ 安装完成"
  fi
}
```

---

## 环境检查与安装

### 快速检查

```bash
# 运行环境检查脚本
~/.openclaw/skills/sdd-dev-workflow/scripts/check-environment.sh
```

**输出示例**：

```
✅ Python 3.11.0
✅ Git 2.34.1
✅ UV 0.4.0
✅ Claude Code 2.1.59
✅ tmux 3.2a
✅ specify 0.1.6
```

### 详细安装步骤

#### 1. Python 3.11+

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv python3.11-dev

# 验证
python3.11 --version
```

#### 2. UV 包管理器

```bash
# 安装
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证
uv --version
```

#### 3. Specify CLI

```bash
# 安装
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git

# 验证
specify --help
```

#### 4. Claude Code（智谱 Coding Plan）

```bash
# 安装 Claude Code
npm install -g @anthropic-ai/claude-code

# 安装智谱 Coding Helper
npm install -g @z_ai/coding-helper

# 配置智谱 Coding Plan
coding-helper auth glm_coding_plan_china "YOUR_API_KEY"
coding-helper auth reload claude

# 验证
claude --version
```

**GLM-5 模型配置**（`~/.claude/settings.json`）：

```json
{
  "env": {
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "glm-5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "glm-5",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "glm-5"
  }
}
```

#### 5. tmux

```bash
# Ubuntu/Debian
sudo apt-get install tmux

# 验证
tmux -V
```

---

## 项目依赖安装

### Python 项目

**requirements.txt 方式**（推荐）：

```bash
# 自动创建虚拟环境并安装依赖
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

**手动安装**：

```bash
# 常用依赖
pip install fastapi uvicorn sqlalchemy pydantic pytest pytest-asyncio

# 开发工具
pip install black flake8 mypy
```

### Node.js 项目

```bash
# 自动安装 package.json 依赖
npm install
```

---

## 环境变量配置

### 必需环境变量

```bash
# 智谱 API Key
export ZHIPU_API_KEY="your-api-key"

# GitHub Token（用于 Speckit）
export GITHUB_TOKEN="your-github-token"
```

**注意**：Gateway 环境变量配置请参考 OpenClaw 官方文档。

---

## 自动安装逻辑

### 在 Autonomous Agent 中

```bash
# 在 Claude Code 执行过程中监控错误

monitor_and_install() {
  while IFS= read -r line; do
    # 检测 ModuleNotFoundError
    if echo "$line" | grep -q "ModuleNotFoundError"; then
      module=$(echo "$line" | grep -oP "No module named '\K[^']+")
      echo "📦 自动安装: pip install $module"
      pip install "$module"

    # 检测 command not found
    elif echo "$line" | grep -q "command not found"; then
      cmd=$(echo "$line" | grep -oP "command not found: \K.+")
      echo "📦 尝试安装: $cmd"

      # 尝试 pip 安装
      pip install "$cmd" 2>/dev/null || \
      apt-get install -y "$cmd" 2>/dev/null || \
      echo "❌ 无法自动安装 $cmd，需要人工介入"
    fi
  done
}

# 使用示例
claude --permission-mode bypassPermissions 2>&1 | monitor_and_install
```

---

## 常见安装问题

### Q: specify init 需要交互式确认？

**解决方案**：使用非交互模式

```bash
specify init . --here --ai claude --force --no-git
```

### Q: Claude Code 连接失败？

**错误**：`Unhandled stop reason: network_error`

**解决方案**：

```bash
# 检查 gateway 状态
openclaw gateway status

# 重启 gateway
openclaw gateway restart
```

### Q: python vs python3 问题？

**解决方案**：系统使用 `python3` 命令

```bash
# 创建别名（可选）
alias python='python3'
```

### Q: 外部 API 网络不可达？

**解决方案**：设置代理

```bash
export http_proxy=http://127.0.0.1:7890
export https_proxy=http://127.0.0.1:7890

# 或在 gateway.env 中配置
echo "http_proxy=http://127.0.0.1:7890" >> ~/.config/openclaw/gateway.env
```

### Q: pip 安装速度慢？

**解决方案**：使用国内镜像

```bash
# 临时使用
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple <package>

# 永久配置
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 依赖清单

### 常用 Python 包

| 包名 | 用途 | 安装命令 |
|------|------|----------|
| `fastapi` | Web 框架 | `pip install fastapi` |
| `uvicorn` | ASGI 服务器 | `pip install uvicorn` |
| `sqlalchemy` | ORM | `pip install sqlalchemy` |
| `pydantic` | 数据验证 | `pip install pydantic` |
| `pytest` | 测试框架 | `pip install pytest` |
| `pytest-asyncio` | 异步测试 | `pip install pytest-asyncio` |
| `black` | 代码格式化 | `pip install black` |
| `flake8` | 代码检查 | `pip install flake8` |

### 项目模板 requirements.txt

```txt
# Web 框架
fastapi==0.115.0
uvicorn[standard]==0.32.0

# 数据库
sqlalchemy==2.0.35

# 数据验证
pydantic==2.9.0
pydantic-settings==2.6.0

# 测试
pytest==9.0.2
pytest-asyncio==0.24.0
httpx==0.27.2
```

---

## 检查清单

**开始项目前**：
- [ ] 运行 `check-environment.sh`
- [ ] 确认 Python 3.11+ 已安装
- [ ] 确认 Git 已安装
- [ ] 确认 Claude Code 已安装

**遇到 ModuleNotFoundError**：
- [ ] 自动执行 `pip install <module>`
- [ ] 验证安装：`python3 -c "import <module>"`

**项目完成验收后**：
- [ ] 导出依赖：`pip freeze > requirements.txt`
- [ ] 提交 requirements.txt 到 Git

---

**最后更新**: 2026-03-13
**版本**: v1.0
