# CHANGELOG — todo-list Skill

所有版本变更记录。格式参考 [Keep a Changelog](https://keepachangelog.com/)。

---

## [1.5.0] — 2026-06-11 🆕 WorkBuddy Automation 整合

### Added
- **WorkBuddy Automation 整合**：双后端提醒支持
- reminder.py 重构：workbuddy 通道（默认） + dingtalk 通道（降级）
- 新增 `setup` 子命令：首次使用配置提醒通道
- `todos/config.json` 运行时配置存储
- 输出格式改为 WorkBuddy 对话内友好格式（`[🔴 HIGH]` / `⏰`）

### Changed
- 默认推送通道：workbuddy（替代旧版"无默认"）
- 推送格式：从 Markdown 改为纯文本 + emoji

### Fixed
- 4 个测试适配新格式：test_format_with_todos / test_push_*
- 总测试数：91 → 92

---

## [1.4.0] — 2026-06-11 ⭐ S 级

### 优化
- description 改 TRIGGER when / DO NOT TRIGGER when 格式
- SKILL.md 新增决策树章节（5 大类，16 行表格）
- 拆分 references/（triggers.md / commands.md / errors.md）
- data/ 目录激活 jieba（user_dict.txt 50+ 行业术语）
- test_cases.json 数据驱动测试（20 个 case）
- cliff.toml CHANGELOG 自动化
- 移除未实现的"ETF 量化报告联动"虚标

### 评估
- skill-evaluator：**9.00 / 10 S（卓越）** ⭐
- 6/8 维度提升，1 个维度（D6）达到 10/10 满分

### 测试
- 91/91 测试通过
- nl_parser 覆盖率 88% → 89%

---

## [1.3.1] — 2026-06-11

### 测试
- 补 nl_parser 71% → 88%、reminder 74% → 88%
- 22 个新测试

---

## [1.3.0] — 2026-06-11

### Added
- Phase 6 定时提醒（4 个子命令）
- scripts/cron_setup.sh 一键部署
- 钉钉 Markdown 推送（**bold**）

---

## [1.2.0] — 2026-06-11

### Added
- Phase 5 NLP 解析（regex + dateutil + jieba）
- 16 个 NLP 测试 + 5 个核心 API

---

## [1.1.1] — 2026-06-11

### Fixed
- Phase 4 补缺陷
- console_script 入口
- CLI 73% → 82%

---

## [1.1.0] — 2026-06-11

### Added
- Phase 4 CLI 8 子命令
- 15 个 CLI 测试

---

## [1.0.0] — 2026-06-11

### Added
- 初始版本（11 个文档 + schema）
- 决策支持：添加/查询/完成/删除/更新
- 时间提醒（到期前 1 小时）
- 优先级和标签
- 归档清理（30 天）
- 审计日志（audit_log）
- 优雅降级（DB 异常 → fallback 文件）

---

## [Unreleased] — 规划中

### 计划中（v1.6 — 近期）

| 功能 | 说明 | 优先级 |
|------|------|:------:|
| 重复提醒 | 支持"每天/每周/每月"重复 | P1 |
| 子任务 | 一个 TODO 可拆分子任务（parent_id） | P2 |
| CLI 增强 | `todos edit`（交互式编辑）+ `todos search` | P2 |
| NLP 改进 | 支持"今天下午"等更复杂时间表达式 | P2 |
| 统计面板 | 可视化：完成率/逾期率趋势图 | P3 |

### 计划中（v2.0 — 中期）

| 功能 | 说明 | 优先级 |
|------|------|:------:|
| 评论/备注 | 给 TODO 加备注（新建 todo_notes 表） | P2 |
| 多用户支持 | Q7 扩展（user_id 区分） | P3 |
| 分类/项目 | projects 表，支持 TODO 分组 | P3 |
| 导出/导入 | JSON/CSV 导出，迁移方便 | P3 |
| Webhook 扩展 | 支持企业微信/飞书（非钉钉） | P4 |

### 不会做的（明确排除）

| 功能 | 原因 |
|------|------|
| 团队协作/共享 | 单用户设计，Q7 明确 |
| 日历同步 | 复杂度高，与日历双向同步 |
| AI 智能排序 | 依赖大模型 API，成本高 |

---

## [1.0.0] — 2026-06-11

### Added
- SKILL.md：技能定义 + 最佳实践（含生命周期、错误处理、状态机）
- README.md：用户文档（含 FAQ、故障排查、对话示例）
- DESIGN.md：技术设计（含架构图、接口定义、并发策略、监控 SLO）
- SECURITY.md：安全扫描报告（依赖+代码+权限+隐私分析）
- manifest.yaml：skill 元数据（qwenpaw skills list 识别）
- EXAMPLES.md：触发示例（给 agent 看的完整示例库）
- INSTALL.md：安装指南（含安全扫描前置条件）
- schema/init_todos.sql：数据库 schema（v1.0）

### Features
- 自然语言添加/查询/完成/删除 TODO
- 时间提醒（到期前 1 小时钉钉推送）
- 优先级（high/medium/low）
- 标签（#tag / tag:xxx / 关键词自动）
- 定时提醒（QwenPaw cron）
- 每日逾期检查（00:05）
- ETF 量化报告联动（tag:etf 追加到报告末尾）
- SQLite 持久化（WAL 并发）
- 归档清理（30 天）
- 审计日志（audit_log）
- 优雅降级（DB 异常 → fallback 文件）

### Technical
- 数据层：TodosStore（11 方法 + 4 异常类型）
- NLP 解析：4 步算法（分词→时间→优先级→标签）
- 并发策略：WAL + retry 3 次 + 乐观锁
- 监控 SLO：5 个指标 + 告警规则

### Documentation
- 6 种文档（SKILL + README + DESIGN + SECURITY + EXAMPLES + INSTALL）
- 业界参考：anthropics/skills + GTD + dateutil + Things3 + 12-Factor + OWASP
- 测试计划：94 个用例（store 21 + cli 19 + nl_parser 32 + reminder 19 + nl_regression 3）

---

*格式：Keep a Changelog v1.0*
*版本命名：语义化版本（SemVer）*
*排序：新版本在上*