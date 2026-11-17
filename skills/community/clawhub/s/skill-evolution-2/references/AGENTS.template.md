# Codex · 技能进化（知行环）配置

本项目使用「技能进化」（别号「知行环」，英文 id `skill-evolution`）框架进行经验积累与技能进化。

## Wiki 结构

所有经验数据存储在 `.wiki/` 目录：

```
.wiki/
├── raw/              # 执行轨迹（按日期追加）
├── knowledge/        # 持久化知识（失败模式 + 成功策略）
│   ├── patterns.md
│   ├── evolution_log.md
│   └── impact_tracker.md
├── skills/           # 可复用技能（可回滚）
└── meta/             # 配置信息
```

## 工作流程（七步闭环）

本框架把 WikiSkill 的经验存储机制与 RSI 的能力判据合成一条闭环：

```
①选域(HCI) → ②记录 → ③提炼 → ④提议 → ⑤门控(四问) → ⑥采纳/回滚 → ⑦升阶(L1-L5)
```

日常只需关注 ②③④，⑤ 必须人工。

### ② 执行任务时
在 `.wiki/raw/YYYY-MM-DD.md` 末尾追加轨迹：
- 记录关键决策点和异常
- 每条轨迹 ≤10 行
- 标记结果：✅ 成功 / ❌ 失败 / ⚠️ 部分成功

### ③ 复盘时（每 3-5 个任务后）
读取最近的轨迹，提炼模式到 `.wiki/knowledge/patterns.md`：
- 失败模式（FM-xxx）：同一错误出现 ≥2 次
- 成功策略（SS-xxx）：有效技巧在多个任务中验证

### ④ 技能进化时（每 5-10 个任务后）
基于 patterns 提出原子化改进：
- 每次只改一个技能，frontmatter 必须带 `source_patterns`（无法追溯来源的不许入库）
- 写入 `.wiki/skills/` 或修改现有技能
- 在 `impact_tracker.md` 记录提案，待后续验证

### ⑤ 门控（人工，不可自动）
四问全过才采纳：**可衡量 / 可保持 / 可迁移 / 可回滚**。
- **自评分不算证据**，必须在独立评估下复现
- **「可回滚」一票否决**——没有「变更历史」的技能不许采纳，无论多有效

## 关键原则

- **角色隔离**：执行任务时**不要读** `.wiki/knowledge/` 或 `.wiki/skills/`（实测会降低技能质量）
- **技能可回滚，Wiki 永不回滚**：知识层只增不减，失败原因必须留下
- **原子化改进**：每轮只改一个技能，便于归因
- **四问全过才采纳**：尤以「可回滚」为一票否决
- **失败也是知识**：被拒绝的提案记录原因，成为下一轮输入

## 触发命令

- "技能进化" / "知行环" → 报出技能名即唤醒，确认当前处于哪一步
- "记录轨迹" / "wiki log" → 追加当前任务轨迹
- "复盘" / "wiki maintain" → 提炼 patterns
- "进化技能" / "wiki evolve" → 提出并验证技能改进
- "wiki 状态" / "wiki status" → 展示统计

## 初始化

<!-- INIT_SECTION_START -->
如果 `.wiki/` 不存在，任选一种方式创建：

**方式 A — 用项目内脚本**（若 `.wiki/scripts/` 已存在）。一条命令，所有 shell 通用：

```bash
python .wiki/scripts/wiki_init.py
```
```bash
# Git Bash / WSL / Linux / macOS 也可用 .sh
bash .wiki/scripts/wiki_init.sh
```

**方式 A′ — 用 skill 目录的脚本**。把 `<skill目录>` 换成 skill-evolution 的实际位置：

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
```powershell
# Windows PowerShell（无 Python 时的备选）
powershell -ExecutionPolicy Bypass -File "<skill目录>\scripts\wiki_init.ps1"
```

> **`.workbuddy/` 是 WorkBuddy 的私有目录。** 如果你没装 WorkBuddy，
> `~/.workbuddy/skills/<skill名>/...` 这条路径**不存在**，命令会失败。
> 请用上面的 `<skill目录>` 写法，或直接用方式 B。
>
> **Git Bash 陷阱**：在 Git Bash 里**不要**用 `python "$HOME/..."`。
> Git Bash 的 `$HOME` 是 POSIX 格式（`/c/Users/xxx`），Windows 原生 Python 会解析成
> `C:\c\Users\xxx` 而找不到文件。Git Bash 请用 `.sh` 版本，
> 或改用 `python "$USERPROFILE\..."` / `python "$(cygpath -w "$HOME")/..."`。

**方式 B — 手动创建**（零外部依赖，任何环境都能用）：
```bash
mkdir -p .wiki/raw .wiki/knowledge .wiki/skills .wiki/meta
printf '# 模式库\n\n## 失败模式\n\n（暂无记录）\n\n## 成功策略\n\n（暂无记录）\n' > .wiki/knowledge/patterns.md
printf '# 技能演化日志\n\n（暂无记录）\n' > .wiki/knowledge/evolution_log.md
printf '# 提案影响追踪\n\n（暂无记录）\n' > .wiki/knowledge/impact_tracker.md
```
<!-- INIT_SECTION_END -->

## 参考

<!-- REF_SECTION_START -->
- 闭环全图与四问评分卡（权威源）：`.wiki/references/workflow.md`
- ① 选域 / ⑦ 升阶（HCI、L1-L5）：`.wiki/references/rsi-framework.md`
- 全链自改进设计五步：`.wiki/references/design-playbook.md`
- 平台适配：`.wiki/references/platforms.md`
- 自动化方案：`.wiki/references/automation.md`
- 模板集合：`.wiki/references/templates.md`
- 备选（需已安装 WorkBuddy）：`~/.workbuddy/skills/skill-evolution/references/`
- 原论文：WikiSkill, arXiv:2608.27454（经验怎么存、怎么迭代）；RSI 路线图, arXiv:2609.11873（改进算不算数、能自动到哪）
<!-- REF_SECTION_END -->

> 本文件已内联技能进化（知行环）的完整规则，可独立工作。若上述参考文件不可读，按本文件执行即可。
