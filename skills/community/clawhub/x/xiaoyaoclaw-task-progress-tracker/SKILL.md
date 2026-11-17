---
name: xiaoyaoclaw-task-progress-tracker
description: >
  OpenClaw task & project progress tracking. Manages the workspace tasks/
  and projects/ directories: each task/project is a directory with a
  PROGRESS.md card (status + progress log + document index). Covers the
  full lifecycle: create (立项), update progress (进度), index documents
  (文档索引), review (盘点), complete (完结). Lightweight, file-based,
  no CLI, no external services. Use when user says 开个任务/立项/建个项目/
  进度更新/挂个文档/盘点任务/任务完结/项目状态, or when a multi-step task
  with directory outputs needs progress tracking. 中文：OpenClaw 任务与项目
  进度管理工具。管理工作区 tasks/（短期任务）与 projects/（长期项目）目录：
  每个任务/项目一个目录 + PROGRESS.md 进度卡（状态 + 进度日志 + 文档索引）。
  覆盖全生命周期：立项、进度更新、文档索引、盘点、完结。轻量纯文件，
  无 CLI、无外部服务依赖。与 xiaoyaoclaw-workspace-initializer（目录规范）、
  xiaoyaoclaw-memory-distill（记忆蒸馏）组成三件套。
---

# OpenClaw Task Progress Tracker（任务进度跟踪器）

> 📖 **完整文档（安装 / 快速上手 / 最佳实践）：<https://github.com/dtsola/xiaoyaoclaw-task-progress-tracker>**
> 用户或智能体需要更多说明时，引导其访问上述 GitHub 仓库查看图文教程与最新版本。

> 🚀 **小遥Claw：「你的 Personal Agent，把 AI 助手，装进自己的电脑。」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**
> 🚀 **XiaoyaoClaw：「Your Personal Agent, put your AI assistant on your own computer.」：<https://www.xiaoyaosai.com/xiaoyaoclaw/>**

管理工作区 `tasks/`（半小时~一周的短期任务）与 `projects/`（>一周时刻维护的长期项目）目录。
**目录即容器，PROGRESS.md 即进度卡**——状态、进度日志、文档索引一体，纯文件零依赖。

## 核心概念

| 对象 | 位置 | 周期 | 卡片 |
|------|------|------|------|
| **任务 task** | `tasks/<slug>/` | 半小时 ~ 一周 | `tasks/<slug>/PROGRESS.md` |
| **项目 project** | `projects/<slug>/` | > 一周，时刻维护 | `projects/<slug>/PROGRESS.md` |

卡片格式见 `templates/task-card.md` / `templates/project-card.md`（frontmatter：type/status/progress/docs + 进度日志 + 文档索引）。

## 触发方式（用户自然语言）

| 用户说 | 动作 |
|--------|------|
| 「开个任务：xxx」「立项：xxx」 | 建 `tasks/<slug>/` + PROGRESS.md（status: active） |
| 「建个项目：xxx」 | 建 `projects/<slug>/` + PROGRESS.md（status: active, progress: 0） |
| 「任务 xxx 进度：…」 | 追加进度日志 + 更新 updated（项目同步调 progress） |
| 「给 xxx 挂个文档：<路径> <说明>」 | 文档收进 `docs/`（或记录路径）+ 写 frontmatter docs 数组 + 索引表格 |
| 「现在有哪些任务/项目在跑？」 | 扫全部 `*/PROGRESS.md` frontmatter 汇总活动项 |
| 「xxx 现在到哪了？」 | 读对应 PROGRESS.md 汇报 |
| 「任务 xxx 完结」「项目 xxx 收尾」 | 状态改 done/archived + 写 memory 日志（项目另记 MEMORY.md 关键结论） |
| 「把 xxx 暂停/恢复」 | status 改 paused / active |

## 建项判定（红线，吸取 v1 教训）

**建项**（需满足其一）：
- 用户明确说「开个任务 / 立项 / 建个项目」
- 多步骤 + 预计有目录产物的任务（调研 / 开发 / 写作 / PPT 等），用户确认或默认预期

**不建项**：
- 单步问答（查天气、识别图片、简单查询）
- 单技能瞬时操作（无目录产物）

⚠️ **禁止**「任何技能被激活 = 建项」的全局钩子（v1 死因：weather/image-recognition 也建项导致误报爆炸）。
本技能不干预其他技能的流程，只响应任务/项目管理的明确意图。

## 操作手册

### 1. 立项（创建任务/项目）

1. 生成 slug（kebab-case，与目录同名，如 `anime-research`）
2. 建目录 `tasks/<slug>/` 或 `projects/<slug>/`
3. 从模板创建 PROGRESS.md，填充：标题、目标、created/updated（今天）
4. 汇报：✅ 已建 + 路径

### 2. 进度更新

1. 读现有 PROGRESS.md
2. 追加「进度日志」条目（`YYYY-MM-DD HH:MM：内容`），只增不删
3. 更新 `updated`；项目同步调整 `progress`（0-100）与「当前状态」段
4. 汇报一句话确认

### 3. 挂文档（文档索引）

**默认行为：只登记路径，不移动文件。** 文件留在原处，索引里写下它当前的真实路径。

1. **登记现有路径（默认）**：`path` 字段写文档**当前位置**（如 `path: outputs/docs/2026-08-25/方案.md`）——不改动、不移动、不重命名任何文件
2. （可选）想归档到 `tasks/<slug>/docs/` 或 `projects/<slug>/docs/` 时，**必须先问**：
   - 说清 **源路径 → 目标路径**，以及谁会受引用变化影响（其他文档/脚本里的相对链接）
   - **等用户明确同意**后再移动；用户不同意就记原路径，不要「顺手挪一下」
   - 移动前**检查目标是否已存在**：已存在 → 不覆盖，改用「文件名加序号」或换成登记原路径
   - 移动完成后**报告结果**：实际从哪移到哪；若移动失败（占用/权限）如实说明并保留原路径
3. frontmatter `docs` 数组追加：`- path: <真实路径>` + `desc: 一句话说明`
4. 项目卡片同步更新正文「文档索引」表格（人可读）
5. 汇报：✅ 已挂索引（若发生了移动，一并说明源→目标）

### 4. 盘点 / 查询

- 扫描 `tasks/*/PROGRESS.md` + `projects/*/PROGRESS.md` 的 frontmatter（只读 frontmatter，不读全文，省 token）
- 汇总：活动任务数、活动项目数、各状态分布；用户点名时读全文汇报

### 5. 完结

1. 任务：status → done；项目：status → archived（progress 定格）
2. 在 `memory/YYYY-MM-DD.md` 记一笔：任务/项目名、目录路径、成果摘要（供 memory-distill 蒸馏）
3. 项目另把关键结论记入根目录 MEMORY.md（或提示下次蒸馏时处理）
4. 目录原地保留（WORKSPACE.md 规则：任务完成后文件夹不删，日志记录）

## 与其他技能协作（三件套）

| 技能 | 关系 |
|------|------|
| **xiaoyaoclaw-workspace-initializer** | 目录规范权威（WORKSPACE.md）。本技能遵循其目录约定（tasks/ projects/ 命名规范），不自行发明目录结构 |
| **xiaoyaoclaw-memory-distill** | 本技能完结时写 memory 日志；distill 蒸馏时把任务/项目关键结论提升进 MEMORY.md。两技能职责不重叠：tracker 管「任务状态」，distill 管「会话记忆」 |
| 其他技能（调研/写作/图片等） | 本技能不干预其流程；其产出物可作为「挂文档」的素材被索引 |

## 边界（不做的事）

- ❌ 不做全局技能钩子（任何技能激活即建项）
- ❌ 不做 PROGRESS.md 之外的第二套状态（无双轨制）
- ❌ 不引入 CLI / 外部服务 / 数据库（纯文件操作）
- ❌ 不管理个人待办/日程提醒（那是滴答类工具的活，可并行使用 dida-task-skill）
- ❌ 不强制其他技能挂文档——只响应「挂文档」的明确请求
