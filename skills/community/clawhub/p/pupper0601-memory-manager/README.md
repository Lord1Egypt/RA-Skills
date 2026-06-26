# Memory Manager — OpenClaw 专用记忆系统 v3.5.0

专为 OpenClaw 设计的三层 AI 记忆管理系统，支持跨设备同步和向量语义搜索。

> **新用户**：安装后运行 `mm onboard` 开始配置！

---

## ✨ OpenClaw 集成特性

| 特性 | 说明 |
|------|------|
| 🏗️ 三层记忆架构 | L1 临时 → L2 长期 → L3 永久 |
| 🔍 向量语义搜索 | 自然语言查询，不只是关键词 |
| 🔄 GitHub 同步 | 跨 OpenClaw 设备无缝同步 |
| 👥 多用户隔离 | OpenClaw 用户身份自动识别 |
| 🗜️ 智能压缩 | 自动升级/降级存储层 |
| 🔗 关联记忆网络 | 相似度 > 0.85 自动关联 |
| 🎯 重要性评分 | 访问频率 + 最近访问评分 |
| 🧠 AI 自我洞察 | 自动总结和分析记忆模式 |

---

## 🚀 快速安装

### Windows（PowerShell）

```powershell
# 一键安装（推荐）
powershell -ExecutionPolicy Bypass -File install.ps1

# 或从网络安装
irm https://raw.githubusercontent.com/Pupper0601/memory-manager/main/install.ps1 | iex
```

> **注意**：若提示 `ExecutionPolicy` 错误，请以管理员身份运行 PowerShell 并执行：
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### macOS / Linux（Bash）

```bash
# ⚠️ 安全提醒：以下命令会下载并立即执行远程脚本，请确保信任此仓库
# 如需检查脚本内容，建议先下载查看再执行

# 一键安装（推荐 --no-shell-rc 选项，不修改shell配置文件）
curl -fsSL https://raw.githubusercontent.com/Pupper0601/memory-manager/main/install.sh | bash -s -- --no-shell-rc

# 或下载后运行（推荐方式 - 更安全）
git clone https://github.com/Pupper0601/memory-manager.git
cd memory-manager
./install.sh --no-shell-rc

# 完全手动安装（最安全）
git clone https://github.com/Pupper0601/memory-manager.git
cd memory-manager
pip install -r requirements.txt
# 手动设置环境变量，避免自动修改shell配置文件
```

### OpenClaw 手动安装

```bash
# 克隆到 OpenClaw workspace 的 skills 目录
git clone https://github.com/Pupper0601/memory-manager.git ~/.openclaw/workspace/skills/memory-manager

# 安装依赖
cd ~/.openclaw/workspace/skills/memory-manager
pip install -r requirements.txt

# 配置 OpenClaw 记忆系统
mm onboard
```

### OpenClaw 推荐配置

```bash
# Linux/macOS 安装到 OpenClaw workspace
./install.sh -u $(whoami) -b siliconflow -p "$HOME/.openclaw/memory" --silent

# Windows 安装到 OpenClaw workspace
.\install.ps1 -UserName $env:USERNAME -Backend siliconflow -MemoryPath "$HOME\.openclaw\memory" -Silent
```

| 参数 | 说明 | OpenClaw 推荐 |
|------|------|---------------|
| 用户名 | OpenClaw 用户ID | 系统用户名或 OpenClaw UID |
| 后端 | embedding 后端 | siliconflow (国内推荐) |
| 路径 | 记忆仓库路径 | `~/.openclaw/memory` |
| 跳过依赖 | 已有依赖时使用 | 第一次安装时不跳过 |

---

## 📋 系统要求

| 组件 | 最低版本 | 说明 |
|------|----------|------|
| Python | 3.8+ | 支持 python3 / python / py 命令 |
| pip | 任意 | 随 Python 自动安装 |
| Git | 任意 | 可选，GitHub 同步时需要 |

### Python 安装指引

- **Windows**：[python.org](https://python.org) 下载安装，或 Microsoft Store 搜索 `Python 3.11`
- **macOS**：`brew install python3` 或从 [python.org](https://python.org) 下载
- **Linux (Ubuntu/Debian)**：`sudo apt install python3 python3-pip`
- **Linux (CentOS/RHEL)**：`sudo yum install python3 python3-pip`

---

## 📝 快速使用

```bash
# 首次使用引导
mm onboard

# 记录记忆
mm log "完成了用户认证功能"

# 语义搜索
mm search "查找相关内容"

# 搜索公共记忆
mm search "团队进展" --shared

# AI 总结
mm insight

# 每日洞察
mm insight --daily

# 查看统计
mm stats

# 更新向量索引
mm embed

# GitHub 同步
mm sync push
mm sync pull
```

---

## 📁 目录结构

```
memory-manager/
├── SKILL.md               # WorkBuddy Skill 定义
├── MEMORY_STYLE_GUIDE.md  # AI 记忆规范
├── README.md              # 本文件
├── reference.md           # 完整技术文档
├── mm.py                  # 快捷命令入口
├── pyproject.toml         # 项目元数据
├── requirements.txt       # 依赖声明
├── install.ps1            # Windows 安装脚本
├── install.sh             # Linux/macOS 安装脚本
└── scripts/
    ├── embed_backends.py      # embedding 后端（OpenAI/SiliconFlow/Zhipu）
    ├── memory_embed.py        # 向量生成
    ├── memory_search.py       # 语义搜索
    ├── memory_sync.py         # GitHub 同步
    ├── memory_compress.py     # 智能压缩
    ├── memory_insight.py      # AI 洞察
    ├── memory_stats.py        # 统计信息
    ├── memory_index.py        # 目录索引生成
    ├── memory_access_log.py   # 访问日志 & 重要性评分
    ├── memory_init.py         # 初始化
    ├── memory_onboard.py      # 首次引导
    └── lancedb_integration.py # LanceDB 加速（可选）
```

---

## 🗂️ 记忆分层

```
L1 临时 (7天)  →  L2 长期 (30天)  →  L3 永久 (永久)
    ↓                ↓                ↓
  daily/          weekly/          permanent/
```

| 层级 | 路径 | 用途 |
|------|------|------|
| L1 | `users/{uid}/daily/` | 当前会话上下文 |
| L2 | `users/{uid}/weekly/` | 跨会话重要信息 |
| L3 | `users/{uid}/permanent/` | 核心价值观、关键决策 |
| 公共 | `shared/` | 团队共享知识 |

---

## ⚙️ 配置

### API Key 设置

```bash
# 硅基流动（推荐，国内可用）
# Linux/macOS
export SILICONFLOW_API_KEY="sk-xxx"
export EMBED_BACKEND=siliconflow

# Windows PowerShell
$env:SILICONFLOW_API_KEY = "sk-xxx"
$env:EMBED_BACKEND = "siliconflow"
# 或永久设置（重启后有效）
[Environment]::SetEnvironmentVariable("SILICONFLOW_API_KEY", "sk-xxx", "User")

# OpenAI
export OPENAI_API_KEY="sk-xxx"
```

### OpenClaw 配置文件

```json
// ~/.openclaw/memory/.memory_config.json（自动生成）
{
  "version": "3.5.0",
  "uid": "pupper",
  "base_dir": "/home/user/.openclaw/memory",
  "backend": "siliconflow",
  "auto_sync": true
}
```

### OpenClaw 环境变量

| 变量 | 说明 | OpenClaw 用途 |
|------|------|---------------|
| `MM_UID` | OpenClaw 用户 ID | 自动绑定 OpenClaw 身份 |
| `MM_BASE_DIR` | 记忆仓库路径 | `~/.openclaw/memory` (推荐) |
| `MM_DEFAULT_SCOPE` | 默认搜索范围 | `private` (用户私有) |
| `EMBED_BACKEND` | embedding 后端 | `siliconflow` (国内可用) |
| `SILICONFLOW_API_KEY` | 硅基流动 Key | 国内最优选择 |
| `OPENAI_API_KEY` | OpenAI Key | 备选方案 |
| `GITHUB_TOKEN` | GitHub PAT | OpenClaw 记忆同步 |

---

## 🌐 多平台注意事项

### Windows 特有问题

| 问题 | 解决方案 |
|------|----------|
| `python` 命令不识别 | 安装时勾选"Add to PATH"，或用 `py` 命令 |
| `pip` 找不到 | 改用 `python -m pip install ...` |
| 路径含中文报错 | 建议使用英文路径，如 `C:\memory` |
| Git 找不到 | 确认 Git 已加入 PATH，或重新安装 Git for Windows |
| PowerShell 权限问题 | 运行 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` |

### macOS 特有问题

| 问题 | 解决方案 |
|------|----------|
| `python3` 版本过低 | `brew install python3` 安装最新版 |
| `grep -P` 不支持 | 脚本已替换为兼容写法，无需处理 |
| `.zshrc` vs `.bash_profile` | 脚本自动检测，macOS 默认 zsh |
| Apple Silicon (M1/M2) | Python 需下载 arm64 版本 |

### Linux 特有问题

| 问题 | 解决方案 |
|------|----------|
| `python3-pip` 未安装 | `sudo apt install python3-pip` |
| `ensurepip` 不可用 | `sudo apt install python3-venv` |
| 权限不足 | 建议用户级安装：`pip install --user ...` |

---

## ❓ 常见问题

**Q: 安装时报 `ModuleNotFoundError: No module named 'openai'`**  
A: 运行 `pip install openai numpy`，或 `python -m pip install openai numpy`

**Q: 向量搜索返回结果少？**  
A: 运行 `mm embed --rebuild` 重建向量库

**Q: `mm` 命令找不到？**  
A: 重启终端，或手动运行：
```bash
# Linux/macOS
source ~/.zshrc  # 或 source ~/.bashrc

# Windows PowerShell
. $PROFILE
```

**Q: 硅基流动访问慢？**  
A: 可换用智谱：`export EMBED_BACKEND=zhipu`

**Q: GitHub 推送失败（认证错误）？**  
A: 设置 Personal Access Token：
```bash
export GITHUB_TOKEN=ghp_xxx
# Windows: $env:GITHUB_TOKEN = "ghp_xxx"
```

**Q: 如何迁移数据？**  
A: 直接在新设备 `git clone` 仓库，然后 `mm embed --rebuild`

**Q: 如何多用户使用？**  
A: 每个用户设置不同的 `MM_UID`，数据自动隔离

**Q: Windows 上记忆路径含空格报错？**  
A: 安装时指定无空格路径，如 `-MemoryPath "C:\MyMemory"`

---

## 🤖 OpenClaw 集成

Memory Manager 是 OpenClaw 的记忆后端，支持跨渠道身份绑定：

```bash
# 安装后配置 OpenClaw
cd memory-manager
python mm.py onboard

# 使用
mm search "我上周做了什么"
mm log "完成了用户认证功能"
mm insight
```

---

## 🔄 更新日志

### v3.5.0 (2026-04-06)
- 跨平台全面适配（Windows / macOS / Linux）
- 修复 macOS `grep -P` 不兼容问题
- 修复 install.sh `$PIP_CMD` 含空格执行失败
- 修复 install.ps1 `$script:MemoryPath` 未初始化
- 修复 Python 3.8 `list[str]` 类型注解不兼容
- 修复 scripts 跨目录导入问题（`sys.path.insert`）
- 修复 Windows `git` 编码 & 路径查找
- `mm` 命令默认路径改为 `~/.memory-manager/memory`

### v3.0.0
- 关联记忆网络（相似度 > 0.85 自动关联）
- 重要性评分（访问频率 + 最近访问 + 手动标记）
- 快照回滚（`mm compress --undo`）
- 搜索综合排序（语义 60% + 重要性 40%）

---

## 📄 License

MIT — 欢迎 Fork & Star ⭐
