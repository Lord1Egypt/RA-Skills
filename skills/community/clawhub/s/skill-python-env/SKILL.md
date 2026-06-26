---
name: skill-python-env
description: 【OpenClaw 内部工具 skill】为其他 skill 提供 Python 虚拟环境管理。按 Python 版本号在 ~/.python_env/<version> 下创建共享环境，多个 skill 可复用同一版本环境。自动安装 uv（若未安装）。不直接面向用户。
emoji: 🐍
metadata:
  clawdbot:
    config:
      requiredEnv: []
      stateDirs: []
      internal: true
      calledBy: other_skills
      example: |
        # 在其他 skill 脚本中调用（确保 Python 3.11 环境存在）
        bash ~/.openclaw/skills/skill-python-env/scripts/ensure_python_env.sh 3.11
        source ~/.python_env/3.11/bin/activate
---

# skill-python-env

> **内部工具 skill** — 本 skill 不直接响应用户指令，由其他需要 Python 环境的 skill 在执行时调用。

## 设计原则

- **按版本共享**：环境以 Python 版本号命名（`~/.python_env/3.11`），不同 skill 只要版本相同即复用同一环境，避免重复创建
- **幂等安全**：环境已存在则秒返回，包安装使用 `uv pip install`（已安装的包自动跳过）
- **零前置依赖**：uv 未安装时自动下载安装，安装完毕后继续执行，无需用户手动干预

## 目录结构

```
skill-python-env/
├── SKILL.md
├── _meta.json
└── scripts/
    ├── ensure_python_env.sh    # Shell 版（供 bash/zsh/Git Bash 调用）
    └── ensure_python_env.py    # Python 版（供 uv run 或 python3 调用）
```

## 调用接口

两个脚本功能完全相同，根据调用方语言选择。

### Shell 版

```bash
bash ~/.openclaw/skills/skill-python-env/scripts/ensure_python_env.sh <python_version> [packages...]
```

| 参数 | 说明 |
|------|------|
| `python_version` | 必填，如 `3.11`、`3.12` |
| `packages...` | 可选，追加安装的包，空格分隔 |

### Python 版（uv run）

```bash
uv run ~/.openclaw/skills/skill-python-env/scripts/ensure_python_env.py <python_version> [--packages pkg1 pkg2 ...]
```

| 参数 | 说明 |
|------|------|
| `python_version` | 必填，如 `3.11`、`3.12` |
| `--packages` | 可选，追加安装的包 |

## 输出格式

脚本运行完成后，stdout 末尾输出以下机器可读行，供调用方 grep 解析：

```
PYTHON_ENV_ACTIVATE:/home/user/.python_env/3.11/bin/activate
PYTHON_ENV_DIR:/home/user/.python_env/3.11
PYTHON_ENV_VERSION:3.11
```

## 其他 skill 集成示例

### 方式 A：直接激活后运行（Shell）

```bash
#!/usr/bin/env bash
# 其他 skill 的入口脚本

SKILL_ENV="$HOME/.openclaw/skills/skill-python-env/scripts/ensure_python_env.sh"

# 确保 Python 3.11 环境就绪，并安装本 skill 所需的包
bash "$SKILL_ENV" 3.11 requests httpx

# 激活并执行
source "$HOME/.python_env/3.11/bin/activate"
python -m my_skill "$@"
```

### 方式 B：解析输出路径（更健壮）

```bash
#!/usr/bin/env bash
SKILL_ENV="$HOME/.openclaw/skills/skill-python-env/scripts/ensure_python_env.sh"

OUTPUT=$(bash "$SKILL_ENV" 3.11 requests 2>&1)
echo "$OUTPUT"

ACTIVATE=$(echo "$OUTPUT" | grep '^PYTHON_ENV_ACTIVATE:' | cut -d: -f2-)
source "$ACTIVATE"
python -m my_skill "$@"
```

### 方式 C：Python 调用

```python
import subprocess, os
from pathlib import Path

script = Path.home() / ".openclaw/skills/skill-python-env/scripts/ensure_python_env.py"
result = subprocess.run(
    ["uv", "run", str(script), "3.11", "--packages", "requests"],
    capture_output=True, text=True
)
# 解析激活路径（仅用于参考，Python 脚本通常直接 import）
activate = next(
    line.split(":", 1)[1] for line in result.stdout.splitlines()
    if line.startswith("PYTHON_ENV_ACTIVATE:")
)
```

## 环境路径规范

| 平台 | 激活命令 |
|------|----------|
| Linux / macOS | `source ~/.python_env/3.11/bin/activate` |
| Windows (Git Bash) | `source ~/.python_env/3.11/Scripts/activate` |
| Windows (PowerShell) | `& "$env:USERPROFILE\.python_env\3.11\Scripts\Activate.ps1"` |

## uv 自动安装

| 平台 | 安装方式 | 安装路径 |
|------|----------|----------|
| Linux / macOS | curl / wget 管道 sh | `~/.local/bin/uv` |
| Windows | PowerShell `irm` | `%USERPROFILE%\.local\bin\uv.exe` |

安装成功后脚本会提示将对应目录加入 `PATH` 以永久生效。

## 常见问题

**Q: 想重置某个版本的环境**
删除目录后重新调用即可自动重建：
```bash
rm -rf ~/.python_env/3.11
bash ensure_python_env.sh 3.11
```

**Q: uv 找不到指定的 Python 版本**
uv 会自动从官方源下载对应版本的 Python，需要网络可访问 `python.org`。

**Q: Windows PowerShell 执行策略报错**
以管理员身份运行：`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`
