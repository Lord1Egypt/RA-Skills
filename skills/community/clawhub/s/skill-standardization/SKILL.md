---
name: skill-standardization
slug: skill-standardization
displayName: skill-standardization
version: 2.102.9
author: wUwproject
license: MIT
description: Skill 标准化规范引擎。支持 R-01~R-26 规范审查（audit / create / update / refactor / bump / readonly 六模式），含权限扫描、数据目录合规检查、渐进式加载、LLM 二次筛分类。
sensitive_access: true
critical_write: false
permission_weight: HIGH
data_dir: ../.standardization/skill-standardization/data
tags: ['standardization', 'skill-builder', 'skill-audit', 'validation', 'json-loader', 'refactor', 'version-bump', 'changelog-auto', 'data-dir']
external_data_dir: true
trigger: ['帮我看看这个技能写得怎么样', '检查这个技能是否规范', '审计 skill', '创建新技能', '更新 skill', '重构技能', 'skill 规范', 'R-规则', '这个 skill 质量怎么样', '帮我检查一下这个 skill 的格式', '看看这个 skill 有没有问题', '给这个 skill 做个体检', '规范一下这个 skill', '标准化这个项目']
trigger_negative: 当用户仅闲聊或问你有什么技能时不触发；单步任务如查看文件不触发
meta_field_sync: true
h1_position: true
data_dir_compliance: true
create_permissions_md: true
---
# skill-standardization

## 约束

- **`.md` 文件禁止使用 Write/Edit 工具更新** — 必须用 `scripts/` 下的 Python 脚本原子写入
- **版本号三端一致** — 更新时同步 `SKILL.md` / `_meta.json` / `references/changelog.md`
- **0 ERROR 0 WARN 铁律强制** — 更新后用 `audit --verify` 验证，非误报项必须全部修复，exit(0) 方可提交
- **LLM 二次筛强制** — audit 输出全部原始问题后，LLM **必须**逐条审查每条 ERROR/WARN。分类为误报时附带 `--reason` 提供具体证据（文件路径/行号/规则编号，证明引擎确实错了或无法判断），不得笼统说"无需处理"。合法误报类别：`engine_mistake`（引擎技术错误）或 `engine_cant_judge`（引擎语义不足）。**`--subtype` 必填，必须在以下枚举表中选择。选择时逐条对照 WARN 的 detail 描述，不匹配的场景不能选：**

  **engine_mistake 类（引擎代码/规则本身出错了，识别错了）：**

  | 子类型 | 适用规则 | 引擎的误报原因（何为真·误报） | 不适用场景（何为真问题） |
  |--------|---------|---------------------------|---------------------|
  | `regex_misidentify` | R-23 | 引擎正则把文档中的 shell 命令/环境变量/URL 误匹配为文件路径，报"文档引用……但文件不存在" | 引擎确实匹配到了真实引用键且文件确实不存在 —— 那是真问题 |
  | `false_classification` | R-01, R-20 | R-01：引擎把合法 frontmatter 字段（如 displayName、slug）标为非标。R-20：引擎把代码标识符/文件名（`novel_state.json`、`is_ending`）误认为自然语言问题，或把领域术语正常使用（SetUser、getData）误报为"术语不一致" | **纯自然语言的「中英文混排缺少空格」或真·术语混用（同一文档混用"更新""修改""变更"）** |
  | `bom_encoding` | R-01 | UTF-8 BOM 或编码声明错误导致 frontmatter 解析错位，字段被误识别 | 没有编码问题，引擎正常解析后报出的非标字段 |
  | `template_convention` | R-11, R-25 C-11 | R-11：正文中的标准化路径说明（models/、data/）是该技能的标准目录结构描述，引擎不应视为路径违规。R-25 C-11：非标章节标题是该技能的固定架构模板 | 非模板内容的违规路径或混乱章节结构 |

  **engine_cant_judge 类（引擎能力不足以判断，LLM 确认是合理的）：**

  | 子类型 | 适用规则 | 引擎判断不了的场景（LLM 确认合理方可放行） | 不适用场景（引擎能判断或 LLM 也无理由放行） |
  |--------|---------|----------------------------------------|-------------------------------------|
  | `domain_convention` | R-17, R-25 C-11 | 技能文档中的特殊章节是该领域（小说写作/色谱分析/项目管理）的标准惯例，引擎缺领域知识无法判断 | 不是因为领域约定，而是文档结构确实混乱 |
  | `architecture_pattern` | R-25 C-14 | 工作流程步骤模式（pipeline/gate/钩子）是该技能的固定架构，引擎无法验证步骤完整性 | C-07 代码块缺语言标识、C-12 约束超上限、C-19 错误处理质量不足 |
  | `context_sensitive` | R-23, R-07 | 函数/触发词是否合理取决于外部上下文，引擎静态分析无法覆盖 | 静态分析能确认的引用缺失或触发词不足 |
  | `data_dependency` | R-11, R-23 | 路径引用依赖运行时数据（模型缓存路径、用户配置），引擎无法静态验证 | 静态路径确实写错了，不是运行时才决定的 |

  **不在枚举表中的子类型 → 代码级拒绝。LLM 不得虚构子类型。WARN/ERROR 的 detail 不匹配任何子类型描述的，不是误报，不能分类，必须真修。** 标记后需重新 audit 确认生效。
- **LLM 手动修不许退出循环** — 遇到 `.remaining_llm.json` 时，LLM **必须立即读取并手动修复**，然后重新审计直到 0 ERROR 0 WARN。**禁止询问用户**、禁止停止、禁止跳过。`sys.exit(2)` 不是循环结束，是"等 LLM 动手"信号。达到 0/0 前循环不结束，不存在"主观建议/可跳过/无法修复"这些类别。
- **HTML 审计报告强制输出** — 每次 `audit` 执行完毕，**必须**确认 `.audit_report.html` 已生成，**且必须**调用 `present_files` 工具打开报告让用户查看
- **`--fix` 自动修正后** — 将 fix_details 转化为可读 changelog 并用 safe_io 写入
- **★ 模式自检闸门强制（不可跳过）** — 执行任何 CLI 命令前，LLM **必须**完成以下自检流程：
  1. 对照下方「模式映射表」逐条匹配用户意图
     ```
     用户请求关键词             → 模式         → 入口命令
     ───────────────────────────────────────────────────
     查看规则/查看模板          → readonly      → rules / create-template
     仅审查/看看/评估           → audit         → audit
     创建/生成/新建             → create        → create
     审计/检查/更新/部分修      → update        → update（含备份）
     改造/重构/标准化/大规模改  → refactor      → refactor（含备份）
     版本升级（单独调用）       → bump          → bump（需双0确认）
     ```
  2. 在回复中**明确输出选定的模式**，格式：`【模式=xxx】`（如 `【模式=refactor】`）
  3. 如果无法输出 `【模式=xxx】`（即找不到匹配），必须**回退重走步骤1**，不得跳过、不得默认、不得猜
  4. **禁止询问用户**、禁止弹框确认、禁止把选择权交给用户
- **★ 模式-命令映射锁（代码级强制，不可跳过）** — 输出 `【模式=xxx】` 后，执行 CLI 命令时**必须同时传入 `--mode xxx` 参数**：
  - 代码对比 `--mode` 值与当前子命令是否一致，不一致则 `exit(1)` 拒绝执行
  - LLM 说"模式=refactor"但执行 `audit --mode refactor` → ❌ 阻断
  - LLM 说"模式=refactor"且执行 `refactor --mode refactor` → ✅ 放行
  - 不传 `--mode` → ❌ 阻断（exit 1），拒绝执行

## 触发条件

**正向触发：**
- [帮我看看这个技能写得怎么样 / 这个技能规范吗 / 质量怎么样]
- [检查/审查/评估一下这个 skill / 跑一遍规范 / 做个体检]
- [创建/生成一个新技能 / 把 xxx 做成 skill / 标准化这个项目]
- [更新/改造一下这个 skill / 重构这个技能 / 升级一下]
- [这个 skill 的 frontmatter/描述/规则怎么写 / 怎么优化]
- [用 skill-standardization 审计/改造某技能]
- [检查某技能的 SKILL.md 是否规范]
- [创建/更新/重构一个 skill]
- [skill 的 frontmatter 怎么写]
- [R-xx 规则是什么意思]

**否定条件：**
- [给这个 skill 做个检查 / 看看有没有问题 / 格式对吗]
- 用户只是问[你有什么技能]——这是闲聊，不是真的要审计/改造
- 用户要求执行某个 skill 的常规功能——应直接调用该 skill 本身，而不是先审计它
- 用户只是提到[skill]这个词，但没有明确的审计/创建/改造意图

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
| -------- |------| ---------- |----------|
| `references/LICENSE.md` | 许可协议 | 开源许可证声明（MIT）。包含：MIT 许可证完整文本。 | R-26 |
| `references/antipatterns.md` | 规范指南 | skill 编写中的常见反模式。包含：错误做法示例、正确做法示例、避坑指引。 | R-18 |
| `references/architecture.md` | 架构设计 | skill-standardization 整体架构。包含：模块关系、数据流、核心设计决策。 | 无 |
| `references/blueprint_flow.md` | 参考文档 | > 定义蓝皮书（Blueprint）、审计（Audit）、修复循环（Fix Loop）三者的关系与流程。 | 无 |
| `references/changelog.md` | 版本管理 | 版本更新日志。包含：版本号、更新类型、修复项、升级说明。 | R-24 |
| `references/data_dir_map.md` | 路径参考 | 数据目录路径对照表。包含：安装目录、标准化目录、备份目录及用途。 | 无 |
| `references/examples.md` | 使用示例 | 各场景完整执行示例。包含：CLI 命令、执行过程、输出结果。 | R-25 C-17 |
| `references/faq.md` | 常见问题 | 常见疑问与解答。包含：问题分类、原因分析、解决方案。 | R-19, R-25 C-19 |
| `references/guide.md` | 使用指南 | 六种执行模式完整操作教程。包含：audit/create/update/refactor/bump/readonly 流程、参数说明、注意事项。 | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描说明与测试结论。包含：风险等级、高权限操作说明、测试概览、计时统计。 | R-15, R-16 |
| `references/reference.md` | 命令参考 | ⛔ **已废弃**。完整命令参考请见 `references/guide.md`，审计规则见 `references/rules.md`。 | 无 |
| `references/rules.md` | 审计规则 | R-01~R-26 审计规则定义。包含：检查逻辑、修复指引、设计背景。 | R-01~R-26 |
## 能力与限制

本技能能做什么、不能做什么，一目了然：

| 能力 | 说明 | 限制 |
| ------ |------| ------ |
| **审计现有 skill** | R-01~R-26 全量检查，输出 PASS/WARN/FAIL 逐条明细及上下文行 | 仅检查 SKILL.md + _meta.json + scripts/ 文件结构和代码静态分析，不检查 Python 运行时行为。参数约束：`<skill-dir>` 为 skill 绝对路径，长度20~260字符|
| **创建新 skill** | 从模板生成标准骨架（SKILL.md / _meta.json / references/ 6文件 / scripts/_paths.py） | 只生成结构模板和占位功能代码，审计规则完整覆盖需运行审计修复。参数：`--desc` 描述文本 ≤120 字 |
| **改造非标 skill** | 自动迁移文件到正确位置、补充 permissions.md、修复格式问题 | 不处理跨技能依赖、不自动生成功能代码。参数：`--changed-files` 文件路径列表（空格分隔）|
| **批量审计** | `audit-all` 子命令扫描 skills/ 下多个 skill | 仅支持一级子目录（不支持嵌套），非技能目录需自行排除。参数：无并行度参数，串行执行 |
| **自动修复** | `--fix` 自动修正 SKILL.md frontmatter / 版本号 / 数据目录 / 触发词 / 反模式 / FAQ / 写作规范 / 路径集中管理 / 代码块格式 / 列表样式 / 节内容补全等格式问题，覆盖 R-01~R-26 共 25+ 条规则（含 R-25 C-05/C-07/C-12/C-19 新增 fix），另有 `code_block_markers`/`list_mixing`/`code_block_lang`/`section_completeness`/`error_handling_faq` 5 个新修复入口 | 仅修复格式/结构/路径/生成类问题，**不修复代码逻辑错误**。<br>修复后需运行 `--verify` + `--show-fix` 两阶段验证确认 |
| **权限安全扫描** | 自动检测脚本中的文件删除/网络请求/subprocess 调用 | 扫描基于 AST 静态分析。参数：无输入参数，自动扫描 `scripts/` 下所有 `.py` 文件 |

> 触发本技能后立即可见的能力输出：读取目标 SKILL.md 中的 frontmatter/正文/references/scripts → 执行 R-01~R-26 规则审查 → 输出审查报告（含每条规则的 PASS/WARN/FAIL 状态 + 详细原因 + 附近代码上下文）。

## 快速开始

以下命令均为 `python -m scripts.skill_audit` 的子命令，需传入 `--mode` 匹配自检闸门输出。

**场景：审计 hug-html 技能** — 全流程演示
```bash
# 只读查询 — 列出 R-01~R-26 共 26 条规则
python -m scripts.skill_audit rules --confirmed --mode readonly
python -m scripts.skill_audit create-template --confirmed --mode readonly

# 审计 hug-html — 扫描 158 行 SKILL.md + 15~20 个脚本（上限50文件)
python -m scripts.skill_audit audit ~/dev/skills/hug-html --confirmed --mode audit

# 审计+修复 — 自动修复 20~50 处格式问题（上限3轮循环）
python -m scripts.skill_audit audit ~/dev/skills/hug-html --fix --confirmed --mode audit

# 审计验证 — 确认 0 ERROR 0 WARN（过滤已分类误判）
python -m scripts.skill_audit audit ~/dev/skills/hug-html --verify --confirmed --mode audit

# 创建新技能 — 5 秒生成完整骨架（=12个必填字段）
python -m scripts.skill_audit create ~/dev/skills/my-new-skill --desc "数据分析工具" --confirmed --mode create

# 轻量更新 — 仅审计 1 个变更文件
python -m scripts.skill_audit update ~/dev/skills/hug-html --changed-files scripts/fix.py --confirmed --mode update

# 全流程改造 — 10 步自动化（35+ fix 函数）
python -m scripts.skill_audit refactor ~/dev/skills/hug-html --confirmed --mode refactor

# 续跑改造 — 从第 5 步继续修复剩余 3~5 个 WARN
python -m scripts.skill_audit refactor ~/dev/skills/hug-html --continue --confirmed --mode refactor

# 版本升级 — 三端同步（SKILL.md + _meta.json + changelog）
python -m scripts.skill_audit bump ~/dev/skills/hug-html --desc "修复R-12路径检测bug" --confirmed --mode bump
```

→ 详见 渐进式文件索引表 获取完整交互示例

## 工作流程

refactor 全流程（10 步）：模式识别为 CLI 前置逻辑，不占流程编号。

1. **蓝皮书扫描** → 输入 SKILL.md + scripts/ → 输出 蓝皮书 JSON — 提取技能结构：文件名、函数、依赖关系
2. **备份** → 输入 技能目录 → 输出 .zip 备份 — 备份到 .standardization/<skill>/backup/
3. **全量审计** → 输入 SKILL.md + references/ → 输出 审计报告 — R-01~R-26 逐条输出原始问题（ERROR + WARN 全部展示，工具不做自动排除）
4. **★ 前置 LLM 二次筛除（代码级阻断点）** →
   - **代码自动阻断**：`_run_audit_loop()` 首次进入时检查 `--classify` 数据（含 `--category` 和 `--reason`），无 `--reason` 则阻断
   - 阻断输出 3 步操作指引：
     1. `audit <skill> --verify` 查看 FAIL 详情
     2. `audit <skill> --classify ID1,ID2 --category engine_mistake --reason "<具体证据>"` 标记误报
     3. `refactor <skill> --continue --confirmed --mode refactor` 继续
   - 已有 `--classify` 数据时自动放行，进入修复循环
   - **LLM 手动分类**：逐条审查每条 ERROR/WARN。分类时必须附带 `--reason` 提供具体证据。**仅当该 WARN/ERROR 的 detail 明确匹配某个子类型的场景描述时才可分类。不匹配 → 不是误报，不是 engine_mistake 也不是 engine_cant_judge → 此为真问题，必须进入步骤 5 修复。不得通过硬选一个不匹配的子类型来跳过。**
     ```
     误报类别：
       engine_mistake  — 引擎技术性错误（BOM/编码/注释误识别）
       engine_cant_judge — 引擎语义不足，LLM确认后放行（__init__.py约定/格式模板域差异）
     ⚠️ --reason 必须包含具体文件路径/行号/规则编号，缺证据代码级拒绝。
     ```
   - 验证：重新 audit 确认分类已完成，`--classify` 查看已标记列表
5. **细碎修复循环** → 输入 审计 FAIL 列表（真问题）→ 输出 修复后的文件 — auto-fix + LLM 手动修复，代码级确认循环
   - 按 fix key 粒度分离 auto/LLM 路径：
     · fix key 在 _llm_only_fix_keys 中（workflow_completeness/example_quality/capability_boundary/section_names）→ LLM 手动
     · 这些 key 被 BLOCKED 时输出 3 步操作指引（读代码→写结构化JSON→重跑 --fix），切勿跳过
     · fix key 不在其中 → auto-fix
     · 无 fix key → LLM 手动
   - 停滞检测：auto-fix 实际修复数为 0 时清空所有 fix key 不再空转
   - 每次修复后代码自动重新审计 + 过滤已分类误报
6. **双0验证** → 全量审计确认后输出 verify 报告 — `--verify` 过滤已分类误报，展示剩余真问题
7. **全量一致性审查 + 前置二次筛** → 输入 文档 + 代码 → 输出 一致性报告
   - 检查文档-代码双向一致性（函数、参数、目录树、规则编号范围等）
   - **自有 LLM 二次筛阻断点**：检查 `--classify` 中 `C-{type}` 格式的 ID
   - auto-fix 修 outdated_rule_ref 等可自动修复项
   - LLM 手动修语义一致性（流程描述 vs 代码执行）
8. **`--subtype` 二次精筛** → 在 `--classify` 标记误报时，**必须**同时传入 `--subtype` 从枚举表中选择匹配的具体场景。枚举表见本文「约束」章节。不匹配的场景代码级拒绝。
9. **bump + cleanup** → 版本号三端同步 + cleanup session 清理临时文件
   - refactor/update 流程内部调用 `cmd_bump`，也可单独调用
10. **★ 展示报告（强制）** → 审计/改造流程全部结束后，LLM **必须**调用 `present_files` 打开生成的 `.audit_report.html`
## 数据目录说明

本技能的数据文件（审查缓存、进度文件、备份、日志等）存放在：

```text
../.standardization/skill-standardization/
├── data/
│   ├── <target-skill>/              # 被审计技能的数据
│   │   ├── .verify_fp.json          # --classify 标记的误判详情
│   │   ├── .remaining_llm.json      # LLM 手动修复项
│   │   └── outputs/
│   │       ├── .audit_report.html   # HTML 审计报告
│   │       └── .verify_fix_map.json # --verify 输出的修复指引映射
├── backup/
│   └── <skill>_<timestamp>.bak      # auto-fix 操作前的单文件备份
└── ...
```

> 安装目录 `skills/skill-standardization/` 只保留 SKILL.md 和 scripts/，数据文件不越位。