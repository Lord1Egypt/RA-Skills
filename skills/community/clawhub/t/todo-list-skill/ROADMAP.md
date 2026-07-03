# todo-list Skill — 开发路线图

> 版本：v1.5 | 日期：2026-06-11 | 状态：v1.5.0 完成，主体功能齐全
>
> skill-evaluator 评估：**9.00 S（卓越）** ⭐
>
> 🆕 v1.5.0 WorkBuddy Automation 整合（双后端提醒）

---

## 📊 当前阶段

| 项目 | 值 |
|------|------|
| **总 Phase 数** | 8 |
| **已完成** | Phase 1 + 2 + 3 + 4 + 5 + 6 + 8（7/8）|
| **当前** | Phase 7：ETF 联动 [暂缓] |
| **版本** | v1.5.0 |
| **评估** | skill-evaluator 9.00 S ⭐ |
| **测试** | 92/92 通过 |

---

## 🗺️ 开发里程碑（已完成）

```
v1.0.0 [文档] ──────────────────────────────── ✅ 完成（2026-06-11）
         11 个文档 + schema + 目录结构

v1.1.0 [核心功能] ──────────────────────────── ✅ 完成
         Phase 2-4：数据层 + CLI + NLP

v1.2.0 [NLP 解析] ───────────────────────────── ✅ 完成
         Phase 5：regex + dateutil + jieba

v1.3.0 [定时提醒] ───────────────────────────── ✅ 完成
         Phase 6：cron 调度 + 钉钉推送

v1.4.0 [Skill 优化] ─────────────────────────── ✅ 完成 ⭐ S 级
         TRIGGER 格式 + 决策树 + references/ + data/

v1.5.0 [WorkBuddy 整合] ─────────────────────── ✅ 完成 🆕
         双后端提醒（workbuddy + dingtalk）+ setup
```

---

## 🗺️ 未来规划

```
v1.6.0 [重复任务] ───────────────────────────── ⬜ 计划中
         支持"每天/每周/每月"重复
         cron 表达 + WorkBuddy automation

v2.0.0 [子任务 + 日历集成] ─────────────────── ⬜ 远期
         parent_id 字段
         Google Calendar / Outlook 同步

Phase 7 [ETF 联动] ──────────────────────────── ⬜ 暂缓
         报告末尾追加 TODO
         自动从持仓计算提醒
```

v1.3.0 [ETF 联动] ─────────────────────────── ⬜ 暂缓
         Phase 7：ETF 报告联动（用户决定暂缓）

v2.0.0 [测试+发布] ────────────────────────── ⬜ 远期
         重复任务 + 子任务 + 日历集成
```

---

## ✅ 已交付（v1.5.0）

### 文档（14 个 + 3 个 references/ + 3 个 data/）

| 文档 | 版本 | 日期 | 说明 |
|------|------|------|------|
| SKILL.md | v1.5 | 2026-06-11 | 技能定义 + 决策树 + WorkBuddy 整合 |
| README.md | v1.5 | 2026-06-11 | 用户文档 + FAQ + 故障排查 |
| DESIGN.md | v1.5 | 2026-06-11 | 技术设计 + 架构图 + 接口定义 |
| SECURITY.md | v1.5 | 2026-06-11 | 安全扫描报告（隐私检查通过）|
| manifest.yaml | 1.5.0 | 2026-06-11 | skill 元数据（含 changelog）|
| EXAMPLES.md | v1.5 | 2026-06-11 | 触发示例 + CLI 用法 + Reminder 用法 |
| INSTALL.md | v1.5 | 2026-06-11 | 安装指南 + 验证步骤 |
| CHANGELOG.md | v1.5 | 2026-06-11 | 版本历史（Keep a Changelog 格式）|
| CONTRIBUTING.md | v1.5 | 2026-06-11 | 贡献指南 + Issue 模板 |
| ROADMAP.md | v1.5 | 2026-06-11 | 开发路线图（v1.0 - v2.0）|
| requirements.txt | v1.0 | 2026-06-11 | Python 依赖清单 |
| pyproject.toml | 1.5.0 | 2026-06-11 | PEP 621 项目元数据 |
| cliff.toml | v1.0 | 2026-06-11 | git-cliff 配置（CHANGELOG 自动化）|
| .gitignore | v1.0 | 2026-06-11 | Git 排除 + 隐私保护 |
| references/triggers.md | v1.0 | 2026-06-11 | 触发词完整列表 |
| references/commands.md | v1.0 | 2026-06-11 | CLI 命令参考 |
| references/errors.md | v1.0 | 2026-06-11 | 错误处理 + 降级路径 |
| data/user_dict.txt | v1.0 | 2026-06-11 | jieba 自定义词典（50+ 术语）|
| data/time_keywords.txt | v1.0 | 2026-06-11 | 时间关键词白名单 |
| data/test_cases.json | v1.0 | 2026-06-11 | 20 个回归测试 case |

### 其他

| 项 | 说明 |
|------|------|
| schema/init_todos.sql | v1.0 数据库 schema |
| scripts/pre_commit_check.sh | 提交前隐私检查脚本 |
| src/__init__.py | 包入口（空文件） |
| tests/ | 测试目录（空目录） |

---

## ⬜ 待开发功能（按优先级）

### P0 — 核心功能（v1.1.0）

| 功能 | Phase | 产出物 | 自评目标 |
|------|:-----:|--------|:--------:|
| 数据层（store.py + init_database.py） | 2 | 15 个单元测试 | ≥90 |
| CLI 8 子命令 | 3 | 每个命令有 --help | ≥90 |
| NLP 解析（nl_parser.py） | 4 | 10 个单元测试 | ≥90 |

### P1 — 提醒功能（v1.2.0）

| 功能 | Phase | 产出物 | 自评目标 |
|------|:-----:|--------|:--------:|
| 定时提醒（reminder.py + cron 注册） | 5 | 集成测试 | ≥90 |
| 每日逾期检查（00:05 cron） | 5 | 集成测试 | ≥90 |

### P2 — ETF 联动（v1.3.0）

| 功能 | Phase | 产出物 | 自评目标 |
|------|:-----:|--------|:--------:|
| ETF 报告追加（etf_integration.py） | 6 | E2E 测试 | ≥90 |

### P3 — 测试+发布（v2.0.0）

| 功能 | Phase | 产出物 | 自评目标 |
|------|:-----:|--------|:--------:|
| 完整测试（33 个用例，覆盖率 ≥85%） | 7 | pytest --cov 报告 | ≥90 |
| SKILL.md materialization | 8 | qwenpaw skills list 识别 | ≥90 |

---

## ❌ 不会做（明确排除）

| 功能 | 原因 |
|------|------|
| 团队协作/共享 | 单用户设计（Q7 明确） |
| 日历同步 | 复杂度高，与日历双向同步 |
| AI 智能排序 | 依赖大模型 API，成本高 |
| 多用户支持 | 当前只有巫师一个人用 |

---

## 🔄 开发节奏（小步迭代）

```
每次开发 → 小步 commit → 推送远程
         ↓
每次 commit 包含：功能代码 + 测试 + 更新 ROADMAP.md
         ↓
每次推送前：./scripts/pre_commit_check.sh 隐私检查
```

### Git 提交规范

```
feat(store): add TodosStore.add() method
fix(cli): handle empty content validation
docs(readme): update directory structure
test(store): add test for ambiguous done
refactor(nl_parser): extract time patterns
```

### 推送前检查清单

```
[ ] ./scripts/pre_commit_check.sh 通过
[ ] pytest 测试全通过
[ ] ROADMAP.md 已更新
[ ] 文档一致性检查（版本号/目录结构）
```

---

## 📋 当前 Phase 详情

### Phase 2：数据层（store.py + init_database.py）

**目标**：实现 TodosStore 数据访问层

**产出物**：
```
src/store.py          ← TodosStore 类（11 方法 + 4 异常类型）
src/init_database.py  ← 数据库初始化脚本
tests/test_store.py   ← 15 个单元测试
```

**关键接口**（见 DESIGN.md）：
```python
class TodosStore:
    def add(...) -> dict
    def list(...) -> list[dict]
    def done(...) -> dict
    def del(...) -> dict
    def update(...) -> dict
    def restore(...) -> dict
    def stats() -> dict
    def check_overdue() -> list[dict]
    def archive_cleanup(...) -> int
```

**边界用例**（必须覆盖）：
- content 空 → ValueError
- content 超长（>500）→ ValueError
- due_at 过去 → ValueError
- due_at > 1 年 → ValueError
- tags 超过 10 个 → 截断 + WARNING
- 模糊匹配多结果 → TodoAmbiguousError
- 并发写入 → WAL + retry 3 次

**验收标准**：
- [ ] `python -m src.cli init` 正常
- [ ] `python -m pytest tests/test_store.py -v` 全通过
- [ ] `grep -r "token\|secret" src/` 无结果（隐私）

**预计工时**：2h

---

## 📊 开发进度统计

| Phase | 内容 | 状态 | 自评 | 交付物 |
|-------|------|:----:|:----:|--------|
| 1 | 调研 + Q1-Q7 | ✅ | 100 | 调研报告 |
| 2 | 数据层 | ⬜ | — | store.py + 15 测试 |
| 3 | CLI 8 子命令 | ⬜ | — | cli.py |
| 4 | NLP 解析 | ⬜ | — | nl_parser.py + 10 测试 |
| 5 | 定时提醒 | ⬜ | — | reminder.py |
| 6 | ETF 联动 | ⬜ | — | etf_integration.py |
| 7 | 测试（33 用例） | ⬜ | — | pytest --cov |
| 8 | SKILL.md materialization | ⬜ | — | qwenpaw skills list |

---

## 🔗 关联文档

| 文档 | 说明 |
|------|------|
| SKILL.md | 技能定义（开发标准） |
| DESIGN.md | 技术设计（接口定义） |
| README.md | 用户文档（使用说明） |
| CHANGELOG.md | 版本历史（更新记录） |
| SECURITY.md | 安全扫描（安装前必读） |
| INSTALL.md | 安装指南（验证步骤） |

---

## 📝 更新日志

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-06-11 | v1.0.0 | 初始路线图（文档完成，待开发） |