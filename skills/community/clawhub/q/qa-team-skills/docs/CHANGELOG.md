# Changelog

All notable changes to qa-team-skills will be documented in this file.

## v1.7.0

### Trellis 式触发重构（2026-08-18）

- **架构**：从"单技能包 + /qa 逻辑指令 + intent-rules 路由表"重构为 **7 个独立 Skill**（skills/ 目录，各带 SKILL.md）
- **触发**：每个 skill 采用双段式 description（何时用 + 何时不用），AI 按自然语言语义自动挑选加载，用户无需记命令名
- **记忆**：跨会话历史加载下沉到各 skill（先询问用户确认后才扫描），读写映射按 skill 收敛，写入确认规则保留
- **删除**：prompts/ 目录（/qa 入口 + intent-rules + 8 个 prompt 文件），validation-rules.md 迁移至 docs/
- **评测**：trigger-eval 期望改为 skill 路由（41 → 51 条，新增 10 条免指令名用例）；functional/security-eval 提示词改为自然语言触发；契约断言迁移到 skills/
- **CI**：validate.sh / run-evals.sh 改查 skills/ 结构 + 双段式 description + 历史加载断言
- **文档**：README / user-manual / process-integration / 仓库级 SKILL.md 全面适配 7 skill 结构

## v1.6.0

### 版本号更新（2026-08-17）

- 版本号从 v1.5.4 升级至 v1.6.0
- 修复 /qa-agent 16 维度定义不一致（维度表 vs 覆盖确认清单 vs 用例格式模板）
- run-evals.sh 新增 agent 维度名一致性断言，防回归
- memory/data/ 加入 .gitignore 并从 git 移除跟踪（防止真实测试数据入库泄漏）
- README 补充 /qa 逻辑指令说明（非注册斜杠命令，可自行注册）
- 评测集版本号统一为 v1.6.0（functional/security/trigger）
- trigger-eval.json 补 explore 正/反例，run-evals.sh 新增 explore 路由分支

## v1.5.4

### 版本号更新（2026-07-17）

- 版本号从 v1.5.3 升级至 v1.5.4

## v1.5.3

### 版本号更新（2026-07-16）

- 版本号从 v1.5.2 升级至 v1.5.3

## v1.5.2

### ClawHub 安全审计修复（2026-07-16）

修复 ClawHub 32 项安全审计发现：

#### 指令冲突修复
- 规范库写入统一为"先询问用户确认后"追加，消除"自动追加"与"先询问"的指令矛盾
- `/qa` 单步任务"自动写入"改为"询问用户是否写入"
- `/qa-team` 漏测复盘输出模板增加"需用户确认后写入"标注

#### 触发词收紧
- 移除 trigger 列表中的"周报""测试任务""探索测试"3 个泛化词
- 移除自动规划匹配中的"帮我看看"、"收尾一下"等日常用词
- 强化 trigger 注释说明：仅当用户明确指向测试任务时激活

#### 用户警告补全
- 全部 8 个 examples/*-demo.md 增加持久化风险 ⚠️ 警告
- `/qa` 第零步历史加载前增加数据读取范围提示
- `templates/agent-test.md` 注入 Payload 标注"安全测试，非攻击行为"

## v1.5.1

### ClawHub 安全审计修复（2026-07-06）

修复 ClawHub（NVIDIA SkillSpector）38 项安全审计发现：

#### 信任边界透明化
- `SKILL.md` 新增 **MCP 能力声明表**，明确文件读/写/删除、可选网络调用范围
- 收紧 trigger 列表，移除易误触发的模糊词（"日报""自由探索"等）

#### 持久化操作需用户确认
- 所有自动写入记忆库的操作改为**先询问用户确认**：/qa-case、/qa-bug、/qa-team、/qa-report
- 版本清理（删除旧 v*.json）改为先询问用户，不再静默删除
- 规范库沉淀（standards.json）改为先询问用户确认

#### 文档诚信修复
- README/user-manual 修正"无外部依赖"的不实声明，区分核心 Prompt vs 可选 CI 评测
- 新增**安全与隐私声明**章节到 README、SKILL、user-manual、memory/README
- memory/README.md 新增数据隐私须知，说明本地存储、保留策略、清理方法

#### 上架配置
- 新增 `.clawhubignore`，上架 ClawHub 时排除 `ci/` 和 `evals/` 开发工具

## v1.5.0

### 轻量任务规划：自动编排模式（2026-06-30）

#### 新增"自动规划"模式
- `/qa` 意图解析新增第三种模式 `intent: "auto"`，与 single / multi 并列
- 用户只说模糊目标（如"测一下支付接口"），AI 自动判断最佳步骤组合
- 生成任务规划建议，用户确认后执行，完成后追问"还需要做什么？"

#### 自动规划场景模板
| 场景 | 用户说 | 自动编排 |
|------|--------|---------|
| 有历史模块回归 | "测一下支付接口" | case → report |
| 无历史模块测试 | "测一下这个新功能" | prd → case → report |
| 质量回顾 | "看下支付模块质量" | 读取 summary → 趋势报告 |
| 测试收尾 | "这个版本测完了" | report → team(准出) |

#### 依赖文件更新
- `prompts/qa/intent-rules.md`：新增自动规划匹配规则节
- `prompts/qa/prompt.md`：意图结构新增 auto 类型、自动规划执行流程、场景模板、自检项
- `prompts/qa/validation-rules.md`：自检清单新增自动规划检查项

### 探索性测试 /qa-explore（2026-06-30）

#### 新增 /qa-explore 指令
- 解决团队"不知道怎么测"的问题——AI 充当探索性测试教练
- `prompts/explore/prompt.md`（119行），三阶段设计：
  - **阶段一**：根据用户目标生成探索任务卡（含任务名称/目标/时间盒/3个起点）
  - **阶段二**：Session笔记模板，记录覆盖路径/发现的问题/学到的经验
  - **阶段三**：Debrief报告，汇总发现+沉淀建议
- 内建约束：探索起点不超过3个、鼓励"走异常路径"、区分疑似Bug和学习经验

## v1.4.0

### 交互层：统一入口 `/qa`（2026-06-30）

#### 新增 `/qa` 指令
- 自然语言任务入口："对支付接口做全量回归并输出缺陷报告"等复合指令
- **意图解析**：将用户输入拆解为单步或多步任务结构
- **任务编排**：生成执行计划，用户确认后逐步骤执行
- **指令路由**：自动分派到 `/qa-prd`、`/qa-case`、`/qa-bug`、`/qa-report`、`/qa-team`、`/qa-agent`
- **多步数据传递**：`prd→case` 评审问题自动转化用例；`bug→report` 缺陷数据自动汇入报告；`bug→team` 缺陷分类辅助漏测复盘

#### 新增记忆模块（`memory/`）
- **用例库**（`memory/schema/test-case.json`）：沉淀测试用例，支持按模块/类型/方法检索复用
- **缺陷库**（`memory/schema/bug.json`）：沉淀缺陷分析结果，支持根因归类与趋势分析
- **评审库**（`memory/schema/review.json`）：沉淀需求评审结果，问题清单可转化为用例
- **报告库**（`memory/schema/report.json`）：沉淀历史报告，支持同比/环比趋势
- **规范库**（`memory/schema/standard.json`）：沉淀团队 Checklist、最佳实践、经验教训
- **任务会话**（`memory/schema/task-session.json`）：完整记录每次 `/qa` 任务执行的全过程
- **文件级持久化**：JSON 格式本地存储，无需外部数据库
- **自动读写**：由 `/qa` 统一入口在步骤间自动管理记忆写入与检索

#### 现有指令记忆集成
- `/qa-prd`：输出自动写入评审库
- `/qa-case`：自动从评审库读取评审记录，输出写入用例库
- `/qa-bug`：自动从缺陷库检索历史记录，输出写入缺陷库
- `/qa-report`：自动从报告/用例/缺陷库汇总数据，输出写入报告库
- `/qa-team`：自动从报告/缺陷库读取辅助趋势分析与效能统计
- `/qa-agent`：输出写入用例库（与 `/qa-case` 共用）

#### 架构文档
- `prompts/qa/prompt.md`：统一入口 Prompt（158 行）
- `memory/README.md`：记忆模块完整说明
- `memory/schema/`：6 个 JSON Schema 数据模型定义
- SKILL.md：新增架构概览图、`/qa` 指令、记忆模块章节
- 版本号统一为 v1.4.0

### 记忆模块 P0：存储改版 + 跨会话加载 + 规范库闭环（2026-06-30）

#### 存储结构改版
- 从平铺文件改为按产品模块组织：`data/products/{module}/{库名}/`
- 每个产品模块独立目录（payments、login 等），支持多产品并行
- 新增 `latest.json` 汇总快照机制

#### 跨会话历史加载
- `/qa` 新增**第零步：历史加载**，启动时自动扫描 `data/products/{scope}/`
- 定义**记忆简报**格式：历史迭代/用例概况/缺陷趋势/规范沉淀
- 新增历史数据影响矩阵：对 case/bug/report/team 步骤分别说明行为变化

#### 规范库闭环
- `/qa-bug` 批量模式发现共性根因 → 自动写入 `standards.json`
- `/qa-team` 漏测复盘 → 自动写入检查清单
- `/qa-case` 启动时自动读取规范库，补充到用例中
- 去重保护：同条目已存在时跳过，避免重复沉淀

### 记忆模块 P1：增量合并 + 历史缺陷→补充用例（2026-06-30）

#### 增量合并
- 每轮 `/qa-case` 写入后**必执行** latest.json 合并
- 合并逻辑：去重（同标题同步骤）、优选（同场景更优者）、重编号
- 每条用例标注 `source_version`，追溯来源迭代

#### 历史缺陷→补充用例
- 新增 5 种缺陷→用例映射规则（并发/超时/边界/注入/配置）
- `/qa-case` 自动读取历史缺陷，高频根因转化为新增用例
- 输出**用例继承分析**：新增/继承/覆盖/遗漏差异报告

### 记忆模块 P2：索引文件 + 趋势查询（2026-06-30）

#### 索引文件
- 新增 `memory/schema/summary.json`（113行 Schema）
- 每个产品模块维护 `summary.json`，7 种写入操作自动同步
- 历史加载时读取 1 次 summary 即可获取全貌，无需扫描全部文件

#### 趋势查询
- `/qa` 新增趋势查询意图匹配（"看趋势""同比""环比"）
- 基于 summary.iterations 生成**记忆成长趋势报告**
- 支持缺陷根因分布变化追踪

#### 架构文档
- `prompts/qa/prompt.md`：统一入口 Prompt（158 行）
- `memory/README.md`：记忆模块完整说明
- `memory/schema/`：6 个 JSON Schema 数据模型定义
- SKILL.md：新增架构概览图、`/qa` 指令、记忆模块章节
- 版本号统一为 v1.4.0

## v1.3.3

### 定位与内容清理（2026-06-25）

#### SKILL.md 前端元数据精简
- 移除 `metadata` 嵌套层级，`agents`、`categories` 冗余字段
- 新增 `trigger` 触发关键词字段
- 压缩 `description` 和 `security` 描述长度
- 移除 `/qa-report` 能力矩阵中的"API 拉取"表述
- 整体版本号统一为 v1.3.3

#### /qa-report API 拉取移除
- `prompts/report/prompt.md`：移除整个「API 自动拉取模式」章节（含 curl 示例、Token 安全警告等）
- 数据来源改为"二选一或混合"，新增"系统数据"选项
- 同步在 README 和 user-manual 中清理 API 拉取残留

#### README SEO 过优化清理
- 徽章栏从 10 个精简至 3 个（version / license / skills.sh）
- 删除「搜索关键词」段落（29 个关键词堆砌）
- 「为什么选择 qa-team-skills」35 行精简为 4 行「适用人群」
- 引用语移除"不是替代测试人员"否定表述

#### 定位表述修正
- 移除全站"全流程"夸大表述（SKILL.md description / 1.md）
- CHANGELOG 中 v1.3.0 "pushy"策略改写为中性描述

## v1.3.1

### 平台兼容性（2026-06-24）

#### 多 Agent 安装支持
- README 安装章节按三种方式重构（手动复制 / npx skills / ClawHub），覆盖 Claude Code / OpenCode / Copilot / Codex CLI / Cursor / Windsurf
- 新增 skills.sh 徽章和一键安装命令 `npx skills add Kokxi/qa-team-skills`
- docs/user-manual.md 安装章节同步更新

#### 文档修正
- examples/README.md 描述修正：7 类型 × 6 方法 → 6 类型 × 9 方法
- 全面版本号更新至 v1.3.1

## v1.3.0

### ClawHub 安全审计修复（2026-06-23）

#### security 声明修正
- SKILL.md frontmatter security 字段重写，精确描述"技能自身不发起网络请求 + 引导用户手动调 API"

#### 子能力路由安全
- `/qa-team` 子能力路由从"关键词→直接执行"改为"匹配→用户确认→执行"，消除 Vague Triggers 风险

#### API 凭证安全
- `/qa-report` 新增"API 安全注意事项"区块，含最小权限 Token、域名核实、Token 轮换、报告脱敏建议
- Bash 执行步骤追加凭证安全操作提醒

#### 文件上传敏感数据警告
- `/qa-report` 文件数据源追加 ⚠️ 敏感数据提示

#### 示例来源标注
- `login-demo.md` 中 AI 补充的用例（TC04/TC05）标注 `[AI补充]` 来源，避免虚构需求误解

#### Description 触发优化
- SKILL.md description 补充自然语言触发场景，提升 AI 调起准确性
- 新增「指令路由边界」表格，解决 5 组易混淆指令的选路问题

#### Eval 测试集
- 新增 `evals/trigger-eval.json`，38 条 trigger query（25 should-trigger + 10 should-not-trigger + 3 边界），用于验证 description 触发准确性

#### 版本号统一
- VERSION / SKILL.md / README.md / user-manual.md / CHANGELOG 等全部文件版本号统一为 v1.3.0

## v1.2.0

### 总监视角优化（2026-06-22）

#### 新增文档
- **流程嵌入指南** (`docs/process-integration.md`)：6 指令在研发流程中的触发时机、前置条件、输入输出、过期条件、角色参与
- **版本治理策略** (`docs/version-policy.md`)：语义化版本规范、升级频率、升级通知模板、回滚机制、兼容承诺

#### 人工校验规则
- SKILL.md 新增「人工校验规则」章节，覆盖全部 6 个指令，防止过度依赖 AI

#### 简明摘要
- 全部 6 个 Prompt 的输出结构新增「简明摘要（30 秒速览）」，面向非测试角色（研发总监/产品经理/VP）
- 自检清单增加简明摘要检查项

#### Backlog 更新
- 新增：AI 效能度量闭环、模型能力评测维度、多语言适配、使用统计埋点

### 全面优化（2026-06-22）

#### 安全增强
- 所有 6 个 Prompt 增加「防注入声明」章节，防止用户输入中的对抗性指令修改 AI 行为
- 所有 6 个 Prompt 增加「输出前自检清单」，强制 AI 在输出前逐条核对关键质量项

#### `/qa-agent` 扩展
- 新增 3 个 RAG 专项测试维度：检索准确性（14）、来源归因（15）、上下文窗口（16）
- 总维度从 13 扩展至 16

#### `/qa-case` 增强
- 新增第 9 种黑盒方法：探索性测试
- 黑盒方法总数从 8 扩展至 9

#### `/qa-bug` 增强
- 批量模式新增「缺陷关联分析」：同源缺陷群检测、批次效应检测、依赖影响链

#### `/qa-report` 增强
- 新增「安全测试专项报告」模板
- 新增「兼容性测试专项报告」模板
- API 自动拉取模式完善（Jira JQL + 禅道 API）

#### `/qa-team` 增强
- 新增「子能力路由」：根据用户输入关键词自动匹配 11 项子能力
- 新增「输入标准化」：建议使用 /qa-report 输出作为数据源，定义标准 CSV 字段
- 新增 7 项子能力：漏测复盘、任务分配建议、团队效能统计、新人培训计划、周会纪要、准入准出检查、版本质量评估

#### 模板 & CI
- 新增 `templates/requirement.md`（通用测试用例模板）
- 新增 `templates/agent-test.md`（Agent 专项测试模板）
- CI 增强：检查每个 Prompt 是否包含「防注入声明」「输出前自检」「设计方法」章节

#### Backlog
- `/qa-team` 快捷子指令（如 /qa-team summary 等）——待讨论
- 探索性测试 Session 记录模板——待讨论
- `/qa-case` 与自动化测试框架集成（输出可执行脚本）——远期规划

---

## v1.0.0 (初始发布)

### 6 大指令

| 指令 | 定位 |
|------|------|
| `/qa-prd` | 需求评审：10 维度系统性检查，输出问题清单 + 澄清问题 |
| `/qa-case` | 测试用例设计：6 类型 × 8 黑盒方法交叉矩阵，自动匹配 |
| `/qa-agent` | AI 智能体专项测试：13 维度覆盖 |
| `/qa-bug` | 缺陷分析：先评估描述质量，信息充分后输出根因分析 + 回归要点 |
| `/qa-report` | 报告生成：日报/周报/阶段/季度/专项，支持文本+文件输入 |
| `/qa-team` | 团队管理 V1.0.0：日报汇总/进度看板/缺陷趋势/成员产出 |