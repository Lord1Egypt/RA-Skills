# 技能进化（知行环）· 自动化运行指南

> 本文件由原 `wikiskill`、`rsi-knowledge`、`rsi-self-improvement-designer` 三份 automation.md
> **合并而成**——三模块现在同属一个 skill，所有 prompt 都在这里，不再有跨 skill 指针。
>
> 面向人的完整操作手册（哪些自动、哪些手动、什么时候做、具体怎么做）见
> **`README.md`** 的「自动化 vs 手动：谁做什么」「什么时候操作（时间线）」
> 「具体怎么操作（按平台）」三节。

## 自动化的四个层次

| 层次 | 能否自动 | 可行方案 | 成熟度 |
|------|---------|---------|--------|
| L1 指令常驻 | ✅ 能 | CLAUDE.md / AGENTS.md 全量加载 | 已实现 |
| L2 自动记录轨迹 | ✅ 能 | Claude Code Stop hook / git hook | 可配置 |
| L3 周期复盘进化 | ✅ 能 | WorkBuddy 定时 automation / cron | 可配置 |
| L4 门控验证 | ❌ 不能 | 需人判断"技能是否真的变好" | 设计如此 |

**核心原则**：论文里 Wiki 维护是**离线批量**做的，Inference Agent 执行时不读 Wiki。对应到实践——
- **在线**（每次任务）：只做 L2 记录，轻到无感
- **离线**（周期性）：做 L3 复盘和进化，批量处理

别试图在每次任务里跑完整四步循环，那是论文的训练流程，不是日常用法。

---

## 支持矩阵（平台 × 操作系统）

| 平台 | 自动调用机制 | Windows | Linux | macOS |
|------|-------------|:------:|:-----:|:-----:|
| WorkBuddy | 定时 automation（周期注入）+ 触发词自动识别 | ✅ | ✅ | ✅ |
| CodeBuddy Code（CLI） | 会话级定时（**不适合长周期**）；持久周期用 headless + 外部调度器 | ✅ | ✅ | ✅ |
| Claude Code | `CLAUDE.md` 常驻指令 + `Stop` hook 提醒 | ✅ | ✅ | ✅ |
| Codex | `AGENTS.md` 常驻指令 + git `post-commit` 提醒 | ✅* | ✅ | ✅ |

\* Codex 在 Windows 上依赖 Git for Windows 自带的 bash 运行 git hook。

> **关于 CodeBuddy 的定时能力（2026-09-17 联网核实官方文档）**：WorkBuddy 的定时 automation
> 是原生功能、**持久保存**（依官方文档，未在本仓库内实际跑过一轮完整周期）。CodeBuddy 必须分形态看：
> - **CodeBuddy IDE / 插件**：**没有**定时任务功能（官方"定时任务"文档仅存在于 `/docs/cli/` 下）。
> - **CodeBuddy Code（CLI）**：**有**，但是**会话级**的——只在 CLI 运行期间有效、
>   **退出即清除且不写盘**、循环任务 **3 天后自动过期**、中断期间错过的任务**不补跑**
>   （单会话上限 50 个，最小间隔 1 分钟）。因此**不适合**"每周 / 每两周复盘"这类长周期。
> - **CodeBuddy 上的持久周期方案**：用 headless 模式 `codebuddy -p -y "<编排 prompt>"`
>   交给**外部调度器**（Windows 计划任务 / Linux cron / GitHub Actions）定时拉起。
> 若都不便，改用方式三的 git hook 或手动触发即可——不影响本文档其余结论。

所有机制均为**文件/配置驱动，与模型权重无关**，因此跨操作系统行为一致：
在 Windows 上跑出来的 `.wiki/` 目录原样复制到 Linux/macOS 机器即可继续用。

> **Stop hook 的实际作用（别误解）**：安装器写入的命令是 `python ".wiki/scripts/wiki_remind.py"`
> （项目级相对路径；用户级则为 `~/.claude/scripts/skill-evolution/wiki_remind.py`）。
> 该脚本**只输出一句"本次任务是否有值得记录的经验"的提醒**，不含 RSI 或自改进内容，
> **也不会自动触发任何模块**。真正让框架自动进场的是常驻指令（CLAUDE.md / AGENTS.md）
> 与方式一的定时任务。

---

## 方式一：WorkBuddy 定时自动化（推荐主方案）

用 WorkBuddy 的定时任务，周期性跑复盘 / 体检 / 设计。这是最省心的方案。

**创建方式**：直接对 WorkBuddy 说一句话即可，例如：

> 创建一个每周定时任务：每周日晚上 9 点，对我的项目执行一次经验复盘

下面提供三种粒度的 prompt 模板，按需取用。

### 模板 A：仅经验沉淀（闭环 ③ 提炼 + ④ 提议）

```
执行一次经验沉淀复盘（本框架闭环 ③④ 的离线维护阶段）：

1. 读取当前项目 .wiki/raw/ 下最近 7 天的执行轨迹
2. 识别模式：
   - 失败模式（FM-xxx）：同类错误出现 ≥2 次
   - 成功策略（SS-xxx）：有效技巧在多个任务中验证
3. 追加到 .wiki/knowledge/patterns.md（只增不减，绝不覆盖已有内容）
4. 在 .wiki/knowledge/evolution_log.md 追加本次维护记录
5. 若识别出值得固化的模式，提出一个原子化技能改进，写入 .wiki/skills/
6. 在 .wiki/knowledge/impact_tracker.md 记录提案，状态标记为"待验证"

约束：
- Wiki 层只增不减，即使某条结论后来被推翻也保留原文
- 每次只提一个技能改进（原子化，便于归因）
- 若 .wiki/ 不存在则跳过并说明，不要自动创建
- 若近期无新轨迹，输出"无需维护"即可，不要凑内容
- 注意角色隔离：这是离线维护任务，与日常任务执行分离
```

### 模板 B：仅 RSI 体检（选域 ① + 升阶 ⑦）

```
参考 skill-evolution skill 的 references/rsi-framework.md
（该 skill 的安装目录，WorkBuddy 下为 ~/.workbuddy/skills/skill-evolution），
执行一次 RSI 框架体检：
1. 读取 RSI 五级自主权（L1–L5）与"环境-数据-模型"四步闭环定义
2. 审视当前项目最近的工作流，逐条标注其成熟度等级与可改进切口
3. 用四大追问（可衡量 / 可保持 / 可迁移 / 可回滚）筛掉"一次性刷榜"式伪改进
4. 输出 ≤5 条候选自改进项，每条带：切口、预期 HCI 增益、独立验证方式

约束：
- 本模块是只读知识底座，不要改动它；也不修改项目代码
- 只做诊断与候选生成；如需落地，转 ②③④ 记录-提炼-提议，再走 ⑤ 门控
- 本任务唯一的写操作：把结论追加到 .wiki/raw/<当天日期>.md
  （若 .wiki/ 不存在则跳过并说明，不要自动创建）
```

### 模板 C：仅自改进设计（全链设计）

```
参考 skill-evolution skill 的 references/design-playbook.md
（该 skill 的安装目录，WorkBuddy 下为 ~/.workbuddy/skills/skill-evolution），
执行一次自改进闭环体检：
1. 先读 references/rsi-framework.md 的 L1–L5 自主权与"环境-数据-模型"四步闭环、四大追问
2. 定位当前项目自改进成熟度，定下一步 L 级目标
3. 选一个具体工作流（优先"反馈廉价、验证明确、部署链路短"的切口）套四步闭环：
   重构环境 → 暴露缺口 → 再训练/沉淀 → 迭代环境
4. 用四大追问为每个改进设独立验证与回滚方案
5. 把可固化的经验/技能沉淀到 .wiki/skills/，状态标记"待验证"

约束：
- 不擅自大规模改项目代码；只产出方案 + 沉淀经验
- 每次只提一个原子化改进，便于归因
- 把结论追加到 .wiki/raw/<当天日期>.md
  （若 .wiki/ 不存在则先跳过并说明，不要自动创建）
```

**建议频率**：模板 A 每周一次（高频开发可改为每 2-3 天）；模板 B/C 每月一次，可与 A 合并进同一个任务。

---

## 方式二：Claude Code（CLAUDE.md 常驻 + Stop hook）

1. **先跑安装器**（它会创建 `.wiki/`、复制运行时与全部参考文档、生成**已渲染**的 `CLAUDE.md`、装好 Stop hook）：
   ```bash
   python "<skill目录>/scripts/install.py" --platform claude --target <项目目录>
   ```
   `<skill目录>` = 本 skill 的实际安装位置（WorkBuddy 下为 `~/.workbuddy/skills/skill-evolution`）。

   > **顺序很重要**：不要先手动 `cp` 模板再跑安装器。安装器发现 `CLAUDE.md` 已存在会**跳过生成**，
   > 于是你留下的仍是**原始模板**——初始化段里是 `<skill目录>` 占位符与 `~/.workbuddy` 私有路径。
   >
   > **怎么判断渲染成功**：`<!-- INIT_SECTION_START -->` 标记在**渲染后依然保留**（安装器靠它做
   > 幂等重装），所以看到这个标记**并不代表**没渲染。真正的判据是看**两段标记之间**是否还残留
   > `<skill目录>` 占位符或 `~/.workbuddy` 私有路径——有则是原始模板，无则是渲染成功。

2. 在生成的 `CLAUDE.md` 末尾追加一条常驻指令：
   > 涉及"经验复盘 / 记录轨迹 / 技能进化 / 自改进 / 能力评估 / 自主性分级"时，
   > 先读 skill-evolution 的对应 references，再决策。

**作用域**

| 位置 | 作用范围 |
|------|---------|
| `~/.claude/settings.json` | 所有项目（一次配置永久生效） |
| `<项目>/.claude/settings.json` | 仅当前项目 |

**安装器会合并而非覆盖**：已有的 `permissions`、`PostToolUse`、其他 `Stop` hook 全部保留，
重复安装自动跳过，卸载只移除本框架 hook 且**绝不删除 `.wiki/` 数据**。

**平台自适应**：安装器检测 `os.name` 选择提醒脚本，并探测 `python` / `python3` / `py -3`：

| 场景 | 生成的命令 | 说明 |
|------|-----------|------|
| 项目级 · Windows | `python ".wiki/scripts/wiki_remind.py"` | 相对路径，项目可移动/可 clone |
| 项目级 · Unix | `bash ".wiki/scripts/wiki_remind.sh"` | 同上 |
| 用户级 · Windows | `python "C:\Users\x\.claude\scripts\skill-evolution\wiki_remind.py"` | 绝对路径，服务所有项目 |
| 用户级 · Unix | `bash "$HOME/.claude/scripts/skill-evolution/wiki_remind.sh"` | 用 `$HOME`，配置可迁移 |

或手动：按平台选一个模板，把其中的 `hooks` 字段合并进 `.claude/settings.json`。
两个模板都用**项目内相对路径**，无需替换用户名：

| 平台 | 模板文件 |
|------|---------|
| macOS / Linux | `assets/hooks/claude-code-settings.json` |
| Windows | `assets/hooks/claude-code-settings.windows.json` |

> 相对路径要求 `.wiki/scripts/` 已存在（先跑 `install.py` 或手动复制）。
> 用户级配置若要用绝对路径，需把命令里的脚本路径改为
> `~/.claude/scripts/skill-evolution/wiki_remind.*`（用 `install.py --user` 会自动装好）。
>
> **模板里的 `python` 是写死的**：若你的机器只有 `python3` 或 `py -3`（Windows 上很常见），
> 手抄模板时必须把命令里的 `python` 换成实际可用的那个，否则 hook 会静默失效。
> `install.py` 会自动探测（`python` → `python3` → `py -3`），省去这一步。

**为什么 Windows 用户级用绝对路径而非 `%USERPROFILE%`**：环境变量语法在不同 shell 下不通用——
cmd 用 `%USERPROFILE%`，PowerShell 用 `$env:USERPROFILE`，sh 用 `$HOME`。Claude Code
在 Windows 上走 cmd.exe/PowerShell，写死哪种语法都可能失效，故改用绝对路径。
代价是配置不可跨机器复制，换机器重跑一次安装器即可。

---

## 方式三：Codex（AGENTS.md 常驻 + git hook）

Codex **没有 hooks 机制**。推荐用安装器（只生成 `.wiki/` 与渲染后的 `AGENTS.md`）：

```bash
python "<skill目录>/scripts/install.py" --platform codex --target <项目目录>
```

再在生成的 `AGENTS.md` 末尾追加同样的常驻指令（内容同方式二第 2 步）。

想在提交时得到提醒，自己在 `.git/hooks/post-commit` 里加一段
（Windows 由 Git for Windows 自带的 bash 执行，Linux/macOS 由系统 sh 执行）：

```bash
#!/bin/bash
if [ -d ".wiki" ]; then
  echo "[技能进化] 本次提交若有值得沉淀的经验，先说一句「记录轨迹」"
fi
```

`chmod +x .git/hooks/post-commit`（Windows 上可省略——Git 不依赖执行位）

---

## 方式四：Git Hook（跨平台通用）

最通用的兜底方案，任何工具链都能用。在 `.git/hooks/post-commit` 加入：

```bash
#!/bin/bash
# 提交后提醒记录轨迹
if [ -d ".wiki" ]; then
  echo "[技能进化] 本次提交若有值得记录的踩坑或技巧，请追加到 .wiki/raw/$(date +%Y-%m-%d).md"
fi
```

记得 `chmod +x .git/hooks/post-commit`。

---

## 跨操作系统注意事项（必读）

| 陷阱 | 表现 | 解法（均已实测） |
|------|------|----------------|
| **Claude Code 在 Windows 用 `.sh`** | hook 静默失效、无报错 | 必须用 `.py` 且写绝对路径；统一安装器已自动处理 |
| **Windows 上裸 `bash xxx.sh`** | 命中 `%SystemRoot%\System32\bash.exe`（WSL 中继），无发行版时报 `execvpe(/bin/bash) failed` | 用 `.py`，或显式调用 `"<Git 安装目录>\bin\bash.exe"`（**各机不同**，先 `where bash` 查实际路径） |
| **Git Bash 的 POSIX 路径** | `/c/Users/x` 被 Windows Python 解析成 `C:\c\Users\x` | 用 `$(cygpath -w "<路径>")` 或项目内相对路径 |
| **环境变量语法不通用** | cmd `%VAR%` / PowerShell `$env:VAR` / sh `$VAR` | Windows 用户级 hook 写死绝对路径，避开变量 |
| **机器无 `python` 命令** | 老配置写死 `python` 时报错 | 安装器自动探测 `python`/`python3`/`py -3`；Linux/macOS 常只有 `python3`，手动命令需自行替换 |

上述规则以 `references/platforms.md` 为**唯一权威源**；如两处不一致以该文件为准。

---

## 什么不该自动化

**门控验证（L4）不建议自动化**。判断"这个技能改进到底有没有用"需要人看实际效果。强行自动化会导致：
- 无效技能被自动采纳，污染技能库
- 论文里的自动门控依赖 held-out 验证集，个人开发没有这个条件

**实践建议**：让 automation 跑 ③ 提炼与 ④ 提议，把提案标为"待验证"，
你在下次遇到类似任务时自然检验，有效就留下，无效就回滚。这个人工环节反而是质量保障。

**另外两条红线**（任何平台都不自动）：
- **采纳 / 回滚决策**——自动化最多把提案标成"待验证"，采纳还是回滚由人拍板。
- **初始化 `.wiki/`**——定时任务发现 `.wiki/` 不存在会**跳过而不创建**（避免在无关项目里乱建目录），所以第一次必须手动。

---

## 组合建议

| 场景 | 推荐组合 |
|------|---------|
| 主用 WorkBuddy | 定时 automation（周复盘）+ 手动提"记录轨迹" |
| 主用 Claude Code | Stop hook（自动提醒）+ 定时手动复盘 |
| 主用 CodeBuddy | headless `-p -y` + 外部调度器；或 Git hook + 手动触发词 |
| 多工具混用 | Git hook（通用提醒）+ WorkBuddy automation（集中复盘） |
| 想立刻见效 | 不做自动化，直接手动把已知坑写进 patterns.md |

---

## 全链联合自动化（一锅端）

本 skill 的七步闭环可打包进**同一个**跨平台自动化，实现"免手动、跨 OS"的自改进循环：

```
①⑦ 读 references/rsi-framework.md        → 概念底座（只读，产出判据）
   用 references/design-playbook.md 设计闭环 → 产出方案（不写文件）
②③④⑥ 交给经验沉淀层写 .wiki/            → 唯一写盘方（可回滚）
⑤ 人工门控验证（L4）                        → 任何平台都不自动
```

**统一编排 prompt 模板（WorkBuddy 定时 automation 直接可用；CodeBuddy headless、Claude Code/Codex 亦可用作周期任务 prompt）**：

```
按 skill-evolution 的七步闭环执行一轮周期维护（①选域 → ②记录 → ③提炼 → ④提议 → ⑤门控 → ⑥采纳/回滚 → ⑦升阶）：

1. 读 skill-evolution skill 的 references/rsi-framework.md
   （该 skill 的安装目录，WorkBuddy 下为 ~/.workbuddy/skills/skill-evolution），
   掌握 L1–L5 自主权、四步闭环、四大追问
2. 用同目录 references/design-playbook.md，
   定位当前项目的自改进成熟度，选一个反馈廉价、验证明确、部署短的切口套四步闭环，
   产出一份原子化自改进方案
3. 把可固化的经验/技能沉淀进 .wiki/skills/（带 frontmatter 与变更历史），
   在 .wiki/knowledge/impact_tracker.md 标记"待验证"，并向 .wiki/raw/ 追加当天轨迹

约束：
- 本任务只读 + 沉淀，不擅自大规模改项目代码
- 每次只提一个原子化改进，便于归因
- 若 .wiki/ 不存在则跳过并说明，不要自动创建
- 门控验证（L4）留给人：提案标"待验证"，不自动采纳
- 角色隔离：这是离线维护任务，不要把它混进日常任务执行中
```

**平台/OS 覆盖**：该编排 prompt 本身是纯文本，在 WorkBuddy 定时 automation、
CodeBuddy headless（`-p -y` + 外部调度器）、Claude Code 的 cron/手动触发、
Codex 的 AGENTS.md 周期任务下**均可直接运行**；
底层 `.wiki/` 目录 Windows/Linux/macOS 原样通用（路径陷阱见 `references/platforms.md`）。
