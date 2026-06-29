# Changelog

All notable changes to qa-team-skills will be documented in this file.

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