# xiaoyaoclaw-task-progress-tracker v2 — 设计文档

> 立项日期：2026-08-26 | 指挥官决策：cairn-cli 太重弃用，自研贴合 tasks/projects 目录的轻量 skill
> 与 v1 的关系：同名重启，定位完全不同（v1=PROGRESS.md 双轨制+全局钩子，已废弃；v2=目录生命周期管理）

## 1. 需求定义（指挥官原话拆解）

| 管理对象 | 周期 | 特征 |
|---------|------|------|
| **tasks 任务** | 半小时 ~ 一周 | 快进快出、轻量 |
| **projects 项目** | > 一周，时刻维护 | 持续演进、文档积累 |

**两大核心能力**：
1. **进度记录**——每次工作后记录进度，可回溯
2. **上下文文档索引**——任务/项目执行中天然生成的文档，在进度中做索引，方便记起来

## 2. 设计原则（吸取教训）

1. **目录即任务/项目**：tasks/xxx、projects/xxx 目录本身就是容器，不另起炉灶
2. **真相源 = 工作区文件**：不依赖外部服务（滴答/GitHub Issues/自托管 App 全排除）
3. **建项克制**：不做「任何技能触发=建项」的全局钩子（v1 死因）；建项由用户指令或明确预期驱动
4. **无双轨制**：不做 PROGRESS.md 状态层 × 内容层分离（v1 维护负担）；状态就写在目录卡片里
5. **无 CLI**：纯 skill 指令，agent 直接操作文件（对比 cairn 的 npm CLI 太重）
6. **三件套协同**：initializer（目录规范权威）→ tracker（任务状态）→ memory-distill（记忆蒸馏）

## 3. 数据模型

> 状态载体统一命名为 **PROGRESS.md**（指挥官指定，2026-08-26）——语义即「进度文件」，README 留给展示场景。

### 3.1 任务卡片（tasks/<slug>/PROGRESS.md）

```yaml
---
type: task
status: active | paused | done | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
docs:                     # 📌 文档索引（天然生成的文档挂这里）
  - path: <文档的真实路径>
    desc: 一句话说明
---
# 任务标题
## 目标
（一句话/一段）
## 进度日志
- YYYY-MM-DD HH:MM：干了什么
- YYYY-MM-DD HH:MM：干了什么
```

### 3.2 项目卡片（projects/<slug>/PROGRESS.md）

```yaml
---
type: project
status: active | paused | archived
progress: 0-100           # 项目进度百分比（时刻维护）
created: YYYY-MM-DD
updated: YYYY-MM-DD
docs:
  - path: tasks/example-task/docs/design.md
    desc: 方案设计
---
# 项目标题
## 目标 / 背景
## 当前状态
（一段话：现在做到哪、下一步是什么）
## 进度日志
- YYYY-MM-DD：里程碑/进展
## 文档索引
| 文档 | 说明 | 更新 |
|------|------|------|
| tasks/example-task/docs/design.md | 方案设计 | 08-26 |
```

### 3.3 与现有目录规范的关系（initializer 对齐）

- `tasks/<slug>/` = 一次性任务目录（WORKSPACE.md 已有约定），`PROGRESS.md` 是状态载体
- `projects/<slug>/` = 长期项目目录，同样加 `PROGRESS.md`
- `docs/` 子目录 = 任务/项目天然生成的文档统一收纳处（替代散落根目录）
- 遵循命名规范：slug kebab-case
- ⚠️ 与 v1 的 PROGRESS.md 区别：v1 是「双轨制」的状态层（与内容产物分离）；v2 的 PROGRESS.md 是任务/项目目录内**唯一的卡片文件**（状态+进度+文档索引一体），文档实体在 docs/ 由索引指向，不存在第二套状态

## 4. 核心机制

### 4.1 建项判定（克制原则）

**建项**（需满足其一）：
- 用户明确说「开个任务/立项/做个项目 xxx」
- 多步骤 + 预计有目录产物的任务（调研/开发/写作/PPT），且用户确认或默认预期

**不建项**：
- 单步问答（查天气、识别图片、简单查询）
- 单技能瞬时操作（无目录产物）

**v1 教训对照**：v1 用「任何技能被激活=建项」→ weather/image-recognition 也建 PROGRESS.md → 误报爆炸。v2 改为「用户指令或明确预期」驱动，技能触发不再自动建项。

### 4.2 进度记录

- 每次工作结束/阶段性完成后，更新卡片 `updated` + 追加「进度日志」条目（时间+做了什么）
- projects 额外维护 `progress` 百分比 + 「当前状态」段
- 进度日志只追加不删除（天然时间线，供回溯）

### 4.3 文档索引（cairn artifact 思想，轻量版）

- 任务/项目执行中生成的重要文档 → **默认记录其现有路径**（不移动文件）→ 写入卡片 frontmatter `docs` 数组 + 正文表格；
  确需归档到 `docs/` 时，**先向用户说明源→目标并取得同意**，确认目标不覆盖已有文件，移动后报告结果
- agent 侧：读卡片时 `docs` 是机器可读索引（YAML），一眼知道有哪些文档、在哪、是什么
- 人侧：正文「文档索引」表格可读
- **关键差异 vs cairn**：cairn 用 CLI 命令（`cairn artifact`）创建+链接；v2 无 CLI，agent 直接改 frontmatter，零依赖

### 4.4 生命周期与 memory-distill 协同

```
立项（建目录+卡片）→ 执行（更新进度/挂文档索引）→ 完结（状态 done）
→ 写 memory/YYYY-MM-DD.md 日志（含目录路径+成果摘要）
→ memory-distill 蒸馏时把项目/任务关键结论提升进 MEMORY.md
```

- 任务完结：`status: done` → 日志记一笔 → 目录原地保留（WORKSPACE.md 规则）
- 项目完结：`status: archived` → 关键结论进 MEMORY.md（供蒸馏）
- 会话恢复：agent 启动时扫 `tasks/*/PROGRESS.md` + `projects/*/PROGRESS.md` 的 frontmatter 即可知全貌（轻量扫描，不读全文）

## 5. 触发方式（SKILL.md 意图识别）

| 用户说 | 动作 |
|--------|------|
| 「开个任务 xxx」「立项 xxx」 | 建 tasks/<slug>/ + 卡片 |
| 「建项目 xxx」 | 建 projects/<slug>/ + 卡片 |
| 「任务 xxx 进度更新：…」 | 追加进度日志 + 更新 updated |
| 「给 xxx 挂个文档」 | 移文档入 docs/ + 写索引 |
| 「盘点当前任务/项目」 | 扫卡片 frontmatter 汇总 |
| 「任务 xxx 完结」 | status: done + 写 memory 日志 |
| 「当前进度」 | 读卡片汇报 |

## 6. 不做什么（边界）

- ❌ 不做全局技能钩子（v1 教训）
- ❌ 不做 PROGRESS.md 双轨制（v1 教训）
- ❌ 不引入 CLI / 外部服务 / 数据库
- ❌ 不管理个人待办（那是 dida-task-skill 的活，可并行）
- ❌ 不干预其他技能的中间产物存放（只做「索引」邀请，不强制）

## 7. 交付物清单

```
projects/xiaoyaoclaw-task-progress-tracker/
├── DESIGN.md          # 本文档（设计）
├── USER_GUIDE.md      # 用户使用指南（站在使用者角度）
├── SKILL.md           # 技能主体（意图识别表 + 操作手册 + 与 initializer/memory-distill 协作说明）
├── templates/
│   ├── task-card.md       # 任务卡片模板
│   └── project-card.md    # 项目卡片模板
├── README.md          # 项目说明（对标 initializer 结构）
├── LICENSE            # MIT
└── assets/            # 可选 hero 图
```

## 8. 开发计划

1. 设计确认（指挥官审核本文档）
2. 建项目目录 + 模板文件
3. 写 SKILL.md（意图识别 + 操作手册 + 边界）
4. 全局技能同步（state/skills/）
5. 本工作区实测（用真实任务跑一遍：立项→进度→挂文档→完结→日志）
6. 发布 GitHub + ClawHub（流程照旧：代理 push、无 BOM JSON、PATCH 后 GET 确认）

## 9. 与 v1 对比（防混淆）

| 维度 | v1（已废弃） | v2（本次） |
|------|-------------|-----------|
| 状态载体 | PROGRESS.md（双轨制：状态层×内容层分离） | PROGRESS.md（唯一卡片：状态+进度+文档索引一体） |
| 建项触发 | 任何技能激活即建项 | 用户指令/明确预期 |
| 文档 | 不管理 | docs/ 索引（cairn artifact 思想） |
| CLI | 无 | 无（保持轻量） |
