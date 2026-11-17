# 跨平台适配指南

技能进化（知行环）的核心是 `.wiki/` 目录结构和 Markdown 文件格式，与具体 Agent 平台无关。本文档说明如何在不同平台上使用。

## 通用原则

所有平台共享：
- **同一个 `.wiki/` 目录**：经验数据可跨平台迁移
- **相同的文件格式**：`raw/`、`knowledge/`、`skills/` 结构一致
- **相同的工作流**：三角色循环（Inference → Maintainer → Proposer）

## 初始化脚本：三选一（重要）

`.wiki/` 的初始化提供了三个等价版本，产出完全一致。按你的环境选：

| 脚本 | 适用环境 | 要求 |
|------|---------|------|
| `scripts/wiki_init.py` | Windows CMD / PowerShell、Linux、macOS | Python 3.6+ |
| `scripts/wiki_init.sh` | Linux / macOS / **Git Bash** / WSL | bash |
| `scripts/wiki_init.ps1` | Windows PowerShell 原生 | PowerShell 3.0+ |

按当前 shell 选一行（`SKILL_DIR` = 本 skill 所在目录，可以是解压后的任意位置）：

```powershell
# Windows PowerShell
python "$SKILL_DIR\scripts\wiki_init.py"
```
```cmd
:: Windows CMD
python "%SKILL_DIR%\scripts\wiki_init.py"
```
```bash
# Linux / macOS / Git Bash / WSL
bash "$SKILL_DIR/scripts/wiki_init.sh"
```
```powershell
# Windows PowerShell（无 Python 时的备选）
powershell -ExecutionPolicy Bypass -File "$SKILL_DIR\scripts\wiki_init.ps1"
```

**最省事的写法**：若项目已用 `install.py` 安装过，运行时已在项目内，
直接跑相对路径，这条命令在**所有 shell 下都成立**：

```bash
python .wiki/scripts/wiki_init.py
```

**为什么 `.sh` 在 Windows 上不够用**：CMD 和 PowerShell 原生环境没有 bash，
直接双击或 `.\wiki_init.sh` 会失败。Git Bash 用户可以正常用，但 Claude Code
在 Windows 上执行 hook 时走的是 cmd.exe/PowerShell，**不会**走 Git Bash——
这也是为什么提醒脚本必须提供 `.py` 版本（见 `references/automation.md`）。

### 路径必须来自"本 skill 的位置"，不要写成 `~/.workbuddy/`

`.workbuddy/skills/<skill名>/` 是 **WorkBuddy 的私有目录**。它只在装了 WorkBuddy
的机器上存在，Claude Code / Codex 用户机器上没有。早期版本把初始化命令和 hook
都指向那里，结果在纯 Claude Code 环境下**静默失效**——不报错、不提醒。

正确做法二选一：

| 做法 | 说明 |
|------|------|
| 用 `install.py` 做项目级安装 | 运行时复制进 `.wiki/scripts/`，项目完全自包含，可提交 Git |
| 用本 skill 的实际解压路径 | 如 `D:\tools\skill-evolution\scripts\wiki_init.py` |

### Windows 路径陷阱：Git Bash 的 POSIX 路径 ≠ Windows Python 的路径

这是 Windows 上最容易踩的坑，**同一个根因有两个表现**。

根因：Git Bash 使用 POSIX 路径格式，Windows 原生 Python 只认 Windows 格式。

**表现 1 — `$HOME` 展开后找不到脚本**

```
Git Bash 认为:   $HOME = /c/Users/xxx
传给 Python:     /c/Users/xxx/.workbuddy/scripts/wiki_init.py
Python 解析成:   C:\c\Users\xxx\.workbuddy\...   ← 多了个 c\
```

报错：`can't open file 'C:\c\Users\xxx\...'`

**表现 2 — 传路径参数后文件写丢**

```
Git Bash:   /tmp/demo  →  C:/Users/xxx/AppData/Local/Temp/demo
Win Python: /tmp/demo  →  C:\tmp\demo        ← 不是同一个地方
```

症状：脚本打印"初始化完成"，但 `find .wiki` 找不到目录。

**解法（均已实测）**

首选：**用项目内相对路径**，它不含任何 shell 变量，全部环境通用：

```bash
python .wiki/scripts/wiki_init.py
```

若运行时还没复制进项目（尚未执行 `install.py`）：

| 场景 | 命令 |
|------|------|
| 用 `.sh` 绕开（Git Bash 推荐） | `bash "<skill目录>/scripts/wiki_init.sh"` |
| 改用 Windows 格式变量 | `python "$USERPROFILE\<skill目录>\scripts\wiki_init.py"` |
| 让 `cygpath` 转换 | `python "$(cygpath -w "<skill目录>")/scripts/wiki_init.py"` |

传路径参数时同样要转换成 Windows 格式：

```bash
python .wiki/scripts/wiki_init.py "$(pwd -W)"
```

不传参时通常没问题——Python 取自身 cwd，与 bash 一致。

### `bash` 在哪，各机不同（不要照抄路径）

手动跑 `.sh` 或写 hook 时，**不要照抄任何写死的 bash 路径**——Git 可能装在
`C:\Program Files\Git`、`D:\Program Files\Git`、`%LOCALAPPDATA%\Programs\Git`（免管理员安装）
或任意自选目录；系统盘也不一定是 `C:`。先查本机实际路径：

| Shell | 查询命令 |
|-------|---------|
| CMD | `where bash` |
| PowerShell | `Get-Command bash \| Select-Object -ExpandProperty Source` |
| Git Bash | `which bash` |

两个坑：

- 输出第一条若是 `%SystemRoot%\System32\bash.exe`，那是 **WSL 中继**、不是 Git Bash；
  往下取第二条，或直接改用 `.py` 入口（最省事）。
- **代码里永远不要写死 bash 路径**。`scripts/install.py` 就是范例：Windows 上用探测到的
  Python 解释器（`detect_python()`），其他平台才用 PATH 里的 `bash`——换机器不用改一行。

## WorkBuddy / CodeBuddy

**配置方式**：直接使用本 SKILL.md，无需额外配置。

**触发命令**：
- "记录轨迹" / "wiki log" → 闭环 ② 记录
- "复盘" / "wiki maintain" → 闭环 ③ 提炼
- "进化技能" / "wiki evolve" → 闭环 ④ 提议 + ⑤ 门控
- "wiki 状态" / "wiki status" → 展示统计

**优势**：
- 内置 skill 系统，自动识别触发词
- 可直接调用 `scripts/wiki_init.sh` 初始化

> **两者差异（2026-09-17 联网核实）**：skill 触发方式相同，但**定时调度能力不同**。
> WorkBuddy 的定时 automation 由本地客户端持久保存，适合"每周 / 每两周复盘"这类长周期。
> CodeBuddy 的定时任务**仅存在于 CodeBuddy Code（CLI）**且是**会话级**——只在 CLI 运行期间
> 有效、退出即清除且不写盘、循环任务 **3 天后自动过期**、中断期间错过的任务**不补跑**；
> CodeBuddy **IDE / 插件没有**此功能。因此在 CodeBuddy 上做周期复盘，需改用
> **headless + 外部调度器**（`codebuddy -p -y "<prompt>"` + 计划任务 / cron / CI），
> 详见 `automation.md` 的「方式一」注记。

## Claude Code

**配置步骤**：

推荐用统一安装器一条命令完成（创建 `.wiki/`、复制运行时、生成自包含 `CLAUDE.md`、装 hook）：

```bash
python <skill目录>/scripts/install.py --platform claude --target <项目目录>
```

手动方式：

1. 复制模板文件到项目根目录：
   ```bash
   cp "<skill目录>/references/CLAUDE.template.md" CLAUDE.md
   ```

2. 编辑 `CLAUDE.md`，按需调整：
   - 修改项目名称和描述
   - 确认 `.wiki/` 路径（默认为项目根目录下的 `.wiki/`）
   - 若没装 WorkBuddy，把初始化段改用模板里的**方式 B**（内联命令，无外部依赖）

3. 初始化 Wiki（按 shell 选一行）：
   ```powershell
   # Windows PowerShell
   python "<skill目录>\scripts\wiki_init.py"
   ```
   ```cmd
   :: Windows CMD
   python "<skill目录>\scripts\wiki_init.py"
   ```
   ```bash
   # Linux / macOS / Git Bash / WSL
   bash "<skill目录>/scripts/wiki_init.sh"
   ```

**使用方式**：
- Claude Code 会自动读取 `CLAUDE.md` 中的指令
- 通过自然语言触发："记录这次任务的轨迹"、"复盘一下最近的经验"
- 或直接编辑 `.wiki/` 中的文件

**注意事项**：
- Claude Code 没有内置的 skill 触发机制，需要手动提醒或使用约定命令
- 建议在项目 README 中说明技能进化（知行环）的使用方式

## Codex (OpenAI)

**配置步骤**：

推荐用安装器（Codex 没有 hook 机制，因此只生成 `AGENTS.md` 和 `.wiki/`）：

```bash
python <skill目录>/scripts/install.py --platform codex --target <项目目录>
```

手动方式：

1. 复制模板文件到项目根目录：
   ```bash
   cp "<skill目录>/references/AGENTS.template.md" AGENTS.md
   ```

2. 编辑 `AGENTS.md`，按需调整：
   - 修改项目名称和描述
   - 确认 `.wiki/` 路径
   - 若没装 WorkBuddy，把初始化段改用模板里的**方式 B**

3. 初始化 Wiki（按 shell 选一行）：
   ```powershell
   # Windows PowerShell
   python "<skill目录>\scripts\wiki_init.py"
   ```
   ```cmd
   :: Windows CMD
   python "<skill目录>\scripts\wiki_init.py"
   ```
   ```bash
   # Linux / macOS / Git Bash / WSL
   bash "<skill目录>/scripts/wiki_init.sh"
   ```

**使用方式**：
- Codex 会读取 `AGENTS.md` 中的指令
- 通过自然语言触发工作流
- 或直接操作 `.wiki/` 目录

**注意事项**：
- Codex 的文件操作能力较强，适合批量维护 Wiki
- 建议定期让 Codex 执行 "wiki maintain" 和 "wiki evolve"

## 跨平台迁移场景

### 场景 1：从 WorkBuddy 迁移到 Claude Code

1. 将 `.wiki/` 目录整体复制到新项目
2. 在 Claude Code 项目中创建 `CLAUDE.md`（使用模板）
3. Claude Code 会自动读取已有的 `patterns.md` 和 `skills/`

### 场景 2：团队协作（多人多平台）

1. 将 `.wiki/` 目录纳入 Git 版本控制
2. 每个成员使用自己偏好的平台
3. 定期 `git pull` 同步 Wiki 更新
4. 冲突处理：
   - `raw/` 和 `knowledge/` 通常只追加，冲突少
   - `skills/` 可能有并发修改，需人工审查

### 场景 3：多项目共享经验

1. 为每个项目创建独立的 `.wiki/`
2. 定期将成功的 `skills/` 提取到共享库
3. 其他项目可引用或复制这些技能

## 平台特性对比

| 平台 | Skill 触发 | 文件操作 | 上下文管理 | 推荐度 |
|------|-----------|---------|-----------|--------|
| WorkBuddy | ✅ 自动 | ✅ 强 | ✅ 优秀 | ⭐⭐⭐⭐⭐ |
| CodeBuddy | ✅ 自动 | ✅ 强 | ✅ 优秀 | ⭐⭐⭐⭐（定时调度受限，见上） |
| Claude Code | ⚠️ 手动 | ✅ 强 | ✅ 优秀 | ⭐⭐⭐⭐ |
| Codex | ⚠️ 手动 | ✅ 强 | ⚠️ 一般 | ⭐⭐⭐ |

**推荐**：优先使用 WorkBuddy（定时调度最完整）。CodeBuddy 的 skill 触发与文件操作体验与 WorkBuddy 同级，但**周期任务需外接调度器**。
