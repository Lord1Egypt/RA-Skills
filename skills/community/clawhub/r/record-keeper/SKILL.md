---
name: record-keeper
alwaysLoad: true
description: >
  工作记录归档标准。当用户要求记录工作内容时,严格按照本 skill 的类别和模板执行。
  触发场景:记录会议、记录需求、记录规划、写SOP、写复盘/报告、值班/人事等行政记录、创建记录文件、归档工作记录。
  类别严格封闭,共13类:meeting / requirement / plan / sop / report / admin / badcase / task / weekly / monthly / quarterly / yearly / memo,不可自行扩展。
  所有记录文件存放在 records/YYYY-MM/ 下,文件名格式:[YYYYMMDD]-[category]-[topic]-[sub-topic]-[seq].md
  badcase 类使用专用文件名格式:[YYYYMMDD]-badcase-[service]-[keyword/topic][-seq].md
---

# Record Keeper - 工作记录归档标准

## 路径约定

本 skill 使用以下占位符，agent 执行时自动解析：

| 占位符 | 含义 | 解析方式 |
|--------|------|----------|
| `{SKILL_DIR}` | 本 skill 的安装目录 | agent 加载 skill 时自动解析为绝对路径 |
| `{WORKSPACE}` | agent 当前工作目录 | exec 的 `workdir` 参数 |

**脚本位置**：`{SKILL_DIR}/scripts/`
- `embed.py` — 向量索引生成与搜索
- `status.py` — 记录状态管理

**数据位置**（均在 `{WORKSPACE}` 下）：
- `records/` — 记录文件目录
- `vectors/embeddings.db` — 向量数据库（SQLite）

---

## 核心规则

### 目录结构

```
{WORKSPACE}/
├── records/
│   ├── 2026-04/
│   │   └── YYYYMMDD-[category]-[topic]-[sub-topic]-[seq].md
│   ├── 2026-05/
│   └── ...
└── vectors/
    └── embeddings.db
```

按月归档。目录不存在时自动创建。

### 文件名规则

```
[YYYYMMDD]-[category]-[topic]-[sub-topic 可选]-[seq 可选].md
```

- `YYYYMMDD`:创建日期
- `category`:必须为以下 13 类之一
- `topic`:中文主题
- `sub-topic`:可选,进一步细分
- `seq`:可选,三位序号 `001`~`999`,同日同主题多份时使用
- 分隔符:英文连字符 `-`

### 十三大类别(严格封闭)

| 类别代码 | 含义 | 使用场景 | 模板文件 |
|---------|------|---------|---------|
| `meeting` | 会议记录 | 有明确开会行为、多人参与、产生讨论/决议/待办 | references/meeting.md |
| `requirement` | 需求文档 | 产品/技术需求的完整定义,含背景/范围/方案/验收标准 | references/requirement.md |
| `plan` | 计划/规划 | 项目计划、季度规划、排期、里程碑、路线图 | references/plan.md |
| `sop` | 标准流程 | 可复用的标准作业程序,有版本号,指导"怎么做" | references/sop.md |
| `report` | 分析/复盘/总结 | 对已有事物的分析、复盘、总结、评审报告 | references/report.md |
| `admin` | 行政/运营事务 | 值班、人事、团队档案、培训记录、成本工时等 | references/admin.md |
| `badcase` | 缺陷案例 | 搜索消歧错误、排序异常、意图识别失败、分词问题等质量缺陷案例 | references/badcase.md |
| `task` | 任务提醒/待办事项 | 每日待办、任务分配、工作清单、截止日期提醒 | references/task.md |
| `weekly` | 周报 | 每周工作内容汇总、进度梳理、下周规划。系统出具草稿，用户审阅补充 | references/weekly-report.md |
| `monthly` | 月报 | 每月工作内容汇总、OKR 进度追踪、下月规划 | references/monthly-report.md |
| `quarterly` | 季报 | 每季度工作汇总、OKR 完成评估、下季度规划建议 | references/quarterly-report.md |
| `yearly` | 年报 | 年度工作总结、大事纪、下年度规划建议 | references/yearly-report.md |
| `memo` | 工作备忘录 | 日常工作总结、技术决策备忘、经验总结、待确认事项临时记录 | references/memo.md |

### WEEKLY 专用文件名格式

```[YYYYMMDD]-weekly-report-[week-range].md```

- `YYYYMMDD`:周报生成日期(通常为周六)
- `week-range`:周数标识,格式为 `W{周数}`,如 `W18` 表示第18周
- 示例:`20260503-weekly-report-W18.md`
- 周数计算:使用 ISO 周数标准

### MONTHLY 专用文件名格式

```[YYYYMMDD]-monthly-report-[YYYY-MM].md```

- `YYYYMMDD`:月报生成日期(通常为每月25日)
- `YYYY-MM`:月报覆盖的月份
- 示例:`20260425-monthly-report-2026-04.md`

### QUARTERLY 专用文件名格式

```[YYYYMMDD]-quarterly-report-[YYYY-QX].md```

- `YYYYMMDD`:季报生成日期(通常为季度末月25日)
- `YYYY-QX`:季报覆盖的季度标识
- 示例:`20260625-quarterly-report-2026-Q2.md`

### YEARLY 专用文件名格式

```[YYYYMMDD]-yearly-report-[YYYY].md```

- `YYYYMMDD`:年报生成日期(每年12月25日)
- `YYYY`:年报覆盖的年份
- 示例:`20261225-yearly-report-2026.md`

### BADCASE 专用文件名格式

```[YYYYMMDD]-badcase-[service]-[keyword/topic][-seq].md
```

- `service`:服务类型,必须为以下 4 种之一(严格封闭)

| 服务代码 | 含义 | 示例 |
|---------|------|------|
| `apex` | 消歧服务 | 20260423-badcase-apex-白云机场南-001.md |
| `sug` | 大搜下拉 | 20260423-badcase-sug-搜索词推荐异常.md |
| `nlu` | NLU 识别服务 | 20260423-badcase-nlu-意图识别错误.md |
| `other` | 其他服务 | 20260423-badcase-other-未知问题.md |

- `keyword/topic`:搜索词或问题主题(中文或拼音)
- `seq`:可选,三位序号 `001`~`999`,同日同服务同主题多份时使用

### 边界判定

容易混淆的场景:

- **需求会** → `meeting`(记录会议过程),会后产出需求文档 → `requirement`
- **季度评审会** → `meeting`,评审会后整理重点事项 → `plan`
- **落地页延期复盘** → `report`,复盘会议过程 → `meeting`
- **Flutter 评审 SOP** → `sop`,讨论建立 SOP 的会议 → `meeting`
- **值班排班** → `admin`,讨论排班方案的会议 → `meeting`
- **消歧 badcase** → `badcase`,讨论消歧 badcase 的会议 → `meeting`
- **分词 badcase** → `badcase`,讨论分词 badcase 的会议 → `meeting`
- **明天要做的 3 件事** → `task`(日常待办)
- **Q2 项目排期** → `plan`(长期规划)
- **值班安排表** → `admin`(行政运营)
- **任务分配会议** → `meeting`(讨论过程)
- **技术方案零散笔记** → `memo`(非正式，轻量记录)
- **BADCASE 处理经验总结** → `memo`(经验方法论记录)
- **日常工作总结** → `memo`(当天工作内容的简要记录)
- **某个技术方案的零散笔记** → `memo`(非正式,轻量记录)
- **工作备忘** → `memo`(当天工作内容的简要记录)

**判定原则**：记录的是"讨论过程"就用 `meeting`，记录的是"产出的文档/结论"就用对应类别。

- **本周工作汇总** → `weekly`（由 cron 自动生成或手动触发）
- **单次任务记录** → `task`（每日待办，非汇总）
- **单次会议** → `meeting`（不是周报的一部分）
- **项目复盘** → `report`（深度分析，非周度汇总）
- **季度总结** → `report`（更长时间维度的分析）
- **周报中的会议条目** → 周报内引用 `meeting` 记录，不重复创建
- **周报中的任务条目** → 周报内引用 `task` 记录，不重复创建
- **月报** → `monthly`（每月汇总，含 OKR 进度追踪）
- **月报中的会议条目** → 月报内引用 `meeting` 记录，不重复创建
- **月报中的周报条目** → 月报内引用 `weekly` 记录，不重复创建
- **季报** → `quarterly`（每季度汇总，含 OKR 完成评估、下季度建议）
- **季报中的月报条目** → 季报内引用 `monthly` 记录，不重复创建
- **季报中的周报条目** → 季报内引用 `weekly` 记录，不重复创建
- **年报** → `yearly`（每年汇总，含年度大事纪、OKR 年度评估、下年度规划）
- **年报中的季报条目** → 年报内引用 `quarterly` 记录，不重复创建
- **年报中的月报条目** → 年报内引用 `monthly` 记录，不重复创建
- **年报中的周报条目** → 年报内引用 `weekly` 记录，不重复创建

---

## 工作流程

### 记录创建流程

1. **判断类别** — 根据上述 13 类和边界判定规则确定 category
2. **生成文件名** - 按 `[YYYYMMDD]-[category]-[topic]...` 格式
3. **读取模板** - 从 `{SKILL_DIR}/references/` 读取对应模板
4. **填充内容** - 根据用户提供的信息填充模板,保留占位符标记未确认项
5. **写入文件** - 存入 `{WORKSPACE}/records/YYYY-MM/` 目录
6. **🔴 强制更新向量索引** - 写入文件后**必须立即**运行 `embed.py init`,不可省略,不可延迟：
   ```
   exec: command="/usr/bin/python3 {SKILL_DIR}/scripts/embed.py init", workdir="{WORKSPACE}"
   ```
7. **设置状态** - 根据文档内容和用户说明，从 `references/status-transitions.md` 中查找恰当的初始状态（默认 `open`，若明确已完成则设为 `done`），执行：
   ```
   exec: command="/usr/bin/python3 {SKILL_DIR}/scripts/status.py set-file <文件名> <状态>", workdir="{WORKSPACE}"
   ```

> ⚠️ **顺序不可颠倒**：必须先 embed.py init（将文件写入数据库），再 status.py set-file（从数据库查询文件）。

### ⚠️ 强制规则

- **写入记录后**:必须**立即**运行 `embed.py init`(使用 workdir 参数,不用 cd &&)
- **subagent 完成后**:主 agent 必须检查是否有新文件产生,如有则运行 `embed.py init`
- **不可省略**:即使用户没有明确要求,也必须自动执行
- **如被打断**:恢复时必须先确认向量索引是否已更新

---

### 📋 任务完成检查清单

**任何涉及记录创建/修改的任务完成后,必须确认以下全部勾选后,才能开始新任务:**

- [ ] 新文件已写入 `{WORKSPACE}/records/YYYY-MM/` 目录
- [ ] **已执行 `embed.py init` 更新向量索引**
- [ ] **已执行 `status.py set-file` 设置记录状态**
- [ ] 向量索引验证成功(无报错)
- [ ] 如使用 subagent,已清理子会话(`cleanup: "delete"`)

**检查不通过,不得开始新任务!**

### 记录检索流程

当用户要求"查阅"、"查找"、"搜索"某类记录时,按以下顺序执行:

1. **向量搜索** - 使用 `embed.py search <关键词>` 检索相关记录(首选)

2. **按状态查询（当查询涉及完成/未完成状态时）** - 直接使用 SQLite 按 status 字段查询：
   ```
   exec: command="/usr/bin/python3 {SKILL_DIR}/scripts/status.py list --category <类别> --status <状态>", workdir="{WORKSPACE}"
   ```
   或按所有类别查询未完成的记录：
   ```
   exec: command="/usr/bin/python3 {SKILL_DIR}/scripts/status.py list --status open --status in_progress", workdir="{WORKSPACE}"
   ```
   **适用场景**：查询"未完成的 badcase"、"进行中的任务"等。
   当 `status` 字段有值时，优先使用 SQL 查询，语义搜索作为补充。

3. **定位文件** - 根据搜索结果读取对应文件
4. **返回内容** - 整理并返回用户需要的信息

#### ⚠️ 检索强制规则

- 查询记录数据时,**必须**优先使用 `embed.py search` 从向量索引中查找
- 查询状态时（如"未完成"、"进行中"），直接使用 `status.py list --status <状态>`
- **禁止**跳过向量搜索直接使用 grep/find 翻文件（status 查询除外）
- 只有在向量索引不可用(embed.py 不存在或向量库为空)时,才降级到文件名匹配 → grep
- 降级时必须告知用户降级原因

## 通用约定

- 所有文件顶部必须有元信息块(时间/提出人/标签等,见各模板)
- 未确认信息保留占位符(如 `_待确认_`),不瞎编
- 删除和覆盖操作必须谨慎,先确认
- 使用 Markdown 格式,表格对齐

---

## 向量索引集成

### 向量文件位置

| 用途 | 路径 | 说明 |
|------|------|------|
| 向量数据库 | `{WORKSPACE}/vectors/embeddings.db` | **主存储** (SQLite) |
| 嵌入脚本 | `{SKILL_DIR}/scripts/embed.py` | 向量生成/搜索工具 |

### 向量生成配置

| 项目 | 配置 |
|------|------|
| API Provider | 硅基流动 (SiliconFlow) |
| 嵌入模型 | `BAAI/bge-m3` |
| 向量维度 | 1024 |
| API KEY 环境变量 | `SILICONFLOW_API_KEY` |

### ⚠️ exec 调用规范(严格遵循)

**环境变量传递**：embed.py 自动继承宿主环境变量 `SILICONFLOW_API_KEY`，不需要显式传递。

```
# ✅ 正确（不传 env，子进程继承环境变量）
exec: command="/usr/bin/python3 {SKILL_DIR}/scripts/embed.py init", workdir="{WORKSPACE}"

# ❌ 错误（${VAR} 不会展开，传的是字面字符串）
exec: command="/usr/bin/python3 {SKILL_DIR}/scripts/embed.py init", env={"SILICONFLOW_API_KEY": "${SILICONFLOW_API_KEY}"}
```

**规则**:
- `embed.py init` 和 `embed.py search` **一律不传 `env` 参数**
- 只要命令不需要额外的自定义环境变量,就用最简单形式:只传 `command` + `workdir`
- 只有需要传**明确的、硬编码的**变量值时才用 `env` 参数

### ⚠️ exec 命令规范(严格遵循)

exec-approvals.json 的 pattern 只匹配**命令的第一个词**。以下写法会导致审批失败:

**❌ 禁止写法**(pattern 匹配失败):
```bash
cd /path && python3 embed.py init        # 第一个词是 cd
source .env && python3 embed.py init     # 第一个词是 source
export KEY=val && cmd                    # 第一个词是 export
```

**✅ 正确写法**(使用 exec 参数代替):
| 场景 | 使用 exec 参数 | 示例 |
|------|---------------|------|
| 切换目录 | `workdir` | `command="python3 embed.py init", workdir="{WORKSPACE}"` |
| 管道/组合 | 分开两次 exec | 先 cmd1,再 cmd2 |

**完整示例**:
```
exec: command="/usr/bin/python3 {SKILL_DIR}/scripts/embed.py search 'BADCASE' 3", workdir="{WORKSPACE}"
```

### 检索优先级

当用户要求查阅记录时,按以下顺序检索:

1. **向量搜索** - 使用 embed.py 进行语义检索(首选)
2. **文件名匹配** - 根据文件名中的 category/topic 关键词
3. **全文 grep** - 在 records/ 目录下 grep 关键词

---

## 记录状态管理

### 状态查询工具

使用 `status.py` 管理记录的状态流转：

| 命令 | 用途 | 示例 |
|------|------|------|
| `status.py list [--category X] [--status X]` | 按类别/状态列出记录 | `status.py list --category badcase --status open` |
| `status.py set <record_id> <status>` | 按记录 ID 设置状态 | `status.py set abc123 done` |
| `status.py set-file <文件名> <status>` | 按文件名设置状态 | `status.py set-file "baijin" done` |
| `status.py normalize "原文"` | 测试归一化映射 | `status.py normalize "已完成"` |

**状态值**：`open`、`pending`、`in_progress`、`done`、`deferred`

### 更新记录内容时的状态选择

每次创建或修改记录文件后，必须：
1. 阅读 `references/status-transitions.md` 中的流转表
2. 确认当前类别允许的目标状态
3. 确认从当前状态到目标状态是否合法
4. 执行 `status.py set-file <文件名> <状态>` 更新 SQLite 中的状态

**示例**：badcase 从 open 变为 in_progress：
```
exec: command="/usr/bin/python3 {SKILL_DIR}/scripts/status.py set-file 'zhongju' in_progress", workdir="{WORKSPACE}"
```

### exec 调用规范

- `status.py` 脚本路径：`{SKILL_DIR}/scripts/status.py`
- 使用 workdir 参数指定工作目录：`workdir="{WORKSPACE}"`
- 不传 env 参数（无需额外环境变量）

---

## 模板文件

每个类别的模板详见 references/ 目录下对应文件:

- `references/meeting.md` - 会议记录模板
- `references/requirement.md` - 需求文档模板
- `references/plan.md` - 计划/规划模板
- `references/sop.md` - 标准流程模板
- `references/report.md` - 分析/复盘/总结模板
- `references/admin.md` - 行政/运营事务模板
- `references/badcase.md` - 缺陷案例模板
- `references/task.md` — 任务提醒/待办事项模板
- `references/weekly-report.md` — 周报模板
- `references/monthly-report.md` — 月报模板
- `references/quarterly-report.md` — 季报模板
- `references/yearly-report.md` — 年报模板
- `references/memo.md` — 工作备忘录模板
- `references/vector-index.md` — 向量索引使用指南
- `references/status-transitions.md` — 状态流转规范（时间流转表、各类别允许状态、正常化映射）
