# todo-list — 个人待办管理技能

> 版本：v1.5 | 更新：2026-06-11
>
> 📝 **skill-evaluator 评估：9.00 S（卓越）**
> 标杆级 Skill，可作为 QwenPaw 内置 skill 候选
>
> 🆕 **v1.5.0**：WorkBuddy Automation 整合（双后端提醒）

在钉钉对话中维护跨会话 TODO 清单，支持自然语言添加、时间提醒、优先级、标签、定时推送。

---

## 🧠 系统怎么工作的（3 步）

```
你说 → "提醒我明天下午3点检查止损"
         ↓
助手理解（NL 解析）
  • 动作：添加（不是查询/删除）
  • 内容：检查止损
  • 时间：明天 15:00（到期前 1h = 14:00 提醒）
  • 优先级：默认 medium
         ↓
存入数据库 + 注册定时提醒
  • 数据：todos.db（永久存储）
  • 提醒：cron 一次性任务（到期前 1h 钉钉通知）
  • 审计：audit_log 记录操作
```

**关键**：数据存在本地，重启不丢失；提醒通过钉钉推送，不需要你盯着。

---

## 快速开始

### 在钉钉对话中这样说

```
提醒我明天下午3点检查止损
今天有什么待办
完成了：检查止损
加个待办，周五前复盘ETF
```

### 命令行使用

```bash
cd ~/workspaces/default/todos

# 初始化
python -m src.cli init

# 添加
python -m src.cli add "检查515070止损" --due "2026-06-11T15:00" --priority high --tag etf

# 列表
python -m src.cli list

# 完成
python -m src.cli done 1

# 删除
python -m src.cli del 2

# 统计
python -m src.cli stats

# 推送钉钉
python -m src.cli push

# 检查逾期
python -m src.cli check_overdue
```

---

## 自然语言示例

| 你说 | 系统理解 |
|------|----------|
| "提醒我明天下午3点检查止损" | 添加：检查止损（明天 15:00）[MEDIUM] |
| "紧急！周五前必须完成" | 添加：完成（周五前）[HIGH] |
| "加个待办：买ETF #投资" | 添加：买ETF [MEDIUM] #投资 |
| "今天有什么待办" | 列出今日 pending |
| "完成了：检查止损" | 标记"检查止损"为已完成 |
| "不重要了，删除那条" | 软删除最近的 pending |
| "改成高优先级" | 更新最近 pending 为 HIGH |

---

## 完整命令参考

### todos add — 添加待办

```bash
todos add "检查止损" --priority high --tag etf
todos add "复盘ETF" --due "2026-06-13T09:00"
todos add "工作汇报" --priority medium --tag work
```

| 参数 | 说明 |
|------|------|
| `--priority` | high / medium / low（默认 medium） |
| `--due` | ISO8601 时间（默认空） |
| `--tag` | 标签（可多次，如 `--tag etf --tag work`） |

### todos list — 查询待办

```bash
todos list                          # 默认今日 pending + in_progress
todos list --status pending         # 只看 pending
todos list --status overdue         # 过期项
todos list --priority high          # 高优先级
todos list --tag etf                # 按标签过滤
todos list --overdue                # 过期项
todos list --all                    # 全部（含已完成）
```

### todos done — 完成待办

```bash
todos done 3                        # 按 ID 完成
todos done "检查止损"              # 按内容模糊匹配
```

完成后移到 archive，7 天内可恢复。

### todos del — 删除待办（软删除）

```bash
todos del 4
todos del "复盘ETF"
```

软删除 → 移入 archive，30 天后清理。

### todos update — 更新待办

```bash
todos update 1 --priority high
todos update 2 --due "2026-06-14T09:00"
todos update 3 --tag etf,work
todos update 1 --status in_progress
```

### todos restore — 从归档恢复

```bash
todos restore 3        # 从 archive 恢复到 todos
```

### todos stats — 统计

```bash
todos stats
```

输出示例：
```
总计: 12 | pending: 8 | in_progress: 1 | completed: 3
逾期: 1 | 本周到期: 3
高优: 2 | 中优: 6 | 低优: 4
```

### todos push — 推送钉钉

```bash
todos push                         # 全部 pending
todos push --overdue               # 只推逾期项
todos push --due-soon             # 推 24h 内到期
```

### todos check_overdue — 检查逾期（定时）

```bash
# 每天 00:05 自动调用，标记过期项
todos check_overdue
```

---

## 状态说明

| 状态 | 含义 | 默认可见 |
|------|------|----------|
| `pending` | 待办，未开始 | ✅ |
| `in_progress` | 进行中 | ✅ |
| `completed` | 已完成（7 天内可恢复） | ❌ |
| `cancelled` | 已取消（7 天内可恢复） | ❌ |
| `overdue` | 已过期（可继续操作） | ✅（用 `--overdue`） |

---

## 定时提醒

### 到期前 1 小时提醒

创建带 `due_at` 的 TODO 时，系统自动在到期前 1 小时推送钉钉提醒。

```
添加：检查止损（明天 15:00）[MEDIUM]
系统：注册 cron 任务（明天 14:00 推送）
到期前 1h 钉钉收到：「【TODO 预警】还有1小时到期：检查止损」
```

### 每日逾期检查

每天凌晨自动标记已过期的 TODO 为 overdue（不影响继续操作）。

---

## 数据存储

- **位置**：`~/workspaces/default/todos/todos.db`
- **备份**：`todos.db.bak`（每日自动备份，保留 7 天）
- **隔离**：独立目录，不与 etf_strategy 混用

---

## 与 ETF 量化报告联动

每次 ETF 策略报告末尾自动追加"今日相关 TODO"（tag:etf 的待办）：

```markdown
## 📌 今日相关待办

- [HIGH] 检查515050止损 @1.125 距今 2h
- [MEDIUM] 159801 持仓复盘 @ 持仓第3天
```

---

## ❓ FAQ（常见问题）

### Q1: 系统说"没理解"，我该怎么办？

**原因**：输入无法被识别为有效命令。

**解决方法**（按优先级）：
1. **换个说法**：更明确地说出动作（如"提醒我"、"添加"）
2. **加关键词**："提醒我明天检查止损"比"检查止损"更容易识别
3. **用 CLI**：`todos add "检查止损" --due "2026-06-12T15:00"`
4. **确认触发词**：

| 动作 | 推荐说法 |
|------|----------|
| 添加 | "提醒我..." / "记一下..." / "加个待办..." |
| 查询 | "我的待办" / "今天有什么" |
| 完成 | "完成了..." / "做完了..." |
| 删除 | "删除..." / "取消..." |

---

### Q2: 系统问"你说的是哪个？"（歧义提示）

**原因**：有多个匹配的 TODO，需要你确认。

**示例**：
```
你："完成那个"
系统："你说的是哪个？
  1. 检查515050止损（今天 15:00）
  2. 复盘ETF持仓（明天 09:00）
请回复编号或完整名称。"
你：回复"1"或"检查515050止损"
```

---

### Q3: 提醒没收到怎么办？

**检查顺序**：
1. **检查钉钉网络**：是否正常接收消息
2. **查看待办状态**：`todos list` 确认 TODO 存在
3. **检查时间**：`due_at` 是否正确（是否已过？）
4. **手动推送**：`todos push --overdue` 立即推送
5. **联系助手**：说"检查 todo 提醒"

---

### Q4: 我想修改提醒时间怎么做？

```bash
# 查看当前待办
todos list

# 更新 due_at
todos update 1 --due "2026-06-13T10:00"

# 如果已注册 cron，系统会自动更新提醒时间
```

---

### Q5: 不小心删错了怎么办？

```bash
# 30 天内可以恢复
todos restore <archive_id>

# 查看归档
todos list --status completed --all
todos list --status cancelled --all
```

---

## 🔧 故障排除

| 问题 | 原因 | 解决方法 |
|------|------|----------|
| "数据库不存在" | 首次使用 | `python -m src.cli init` 初始化 |
| "数据库被锁定" | 多进程冲突 | 等待 5 秒重试 |
| "找不到命令" | 目录错误 | `cd ~/workspaces/default/todos` 再试 |
| 推送失败 | 钉钉 webhook 未配置 | 检查钉钉 channel 配置 |
| 时间显示错误 | 时区问题 | due_at 使用 `+08:00` 格式 |
| 提醒没来 | cron 未注册成功 | `todos push` 手动触发 |
| NL 解析一直失败 | 表达方式不标准 | 改用 CLI：`todos add ...` |
| 数据丢失 | DB 损坏 | `cp todos.db.bak todos.db` 从备份恢复 |

---

## 💬 典型对话示例

### 场景 1：添加带提醒的 TODO

```
你：提醒我明天下午3点检查止损
助手：✅ 已添加：检查止损（明天 15:00）[MEDIUM]
     到期前 1 小时会提醒你
```

### 场景 2：查询今日待办

```
你：今天有什么待办
助手：📋 今日待办（3 项）

  1. [HIGH] 检查515050止损 @1.125（今天 15:00）#etf
  2. [MEDIUM] 复盘ETF持仓（明天 09:00）#etf
  3. [LOW] 写周报（周五前）#work

  逾期：0 项
```

### 场景 3：完成 TODO

```
你：完成了检查止损
助手：✅ 已完成：检查515050止损
     原定时间：今天 15:00
     实际完成：15:23
```

### 场景 4：歧义处理

```
你：完成那个
助手：🤔 你说的是哪个？

  1. 检查515050止损（今天 15:00）
  2. 复盘ETF持仓（明天 09:00）

请回复编号（1-2）或完整名称。
你：1
助手：✅ 已完成：检查515050止损
```

### 场景 5：解析失败

```
你：那个事情处理一下
助手：没太理解你的意思，可以换个说法吗？

推荐说法：
  • "提醒我明天下午3点检查止损"（添加）
  • "我的待办"（查询）
  • "完成了：检查止损"（完成）

或者直接用命令：`todos add "内容"`
```

---

## 版本说明

### v1.5.0（2026-06-11）🆕
- ✅ WorkBuddy Automation 整合（双后端提醒）
- ✅ reminder.py 重构：workbuddy（默认） + dingtalk（降级）
- ✅ 新增 setup 子命令 + todos/config.json（运行时配置）
- ✅ 94/94 测试通过（新增 2 个 setup 测试）
- ✅ 提醒输出改为 WorkBuddy 对话内格式（[🔴 HIGH] / ⏰）

### v1.4.0（2026-06-11）⭐
- ✅ 7 项优化：TRIGGER 格式 + 决策树 + references/ + data/ + jieba
- ✅ skill-evaluator 评估：**9.00 S（卓越）**
- ✅ 91/91 测试通过，83% 覆盖率

### v1.3.1（2026-06-11）
- ✅ 覆盖率补足（nl_parser 88%, reminder 88%）

### v1.3.0（2026-06-11）
- ✅ Phase 6 定时提醒

### v1.2.0（2026-06-11）
- ✅ Phase 5 NLP 解析

### v1.1.1（2026-06-11）
- ✅ Phase 4 补缺陷 + console_script

### v1.1.0（2026-06-11）
- ✅ Phase 4 CLI 8 子命令

### v1.0.0（2026-06-11）
- ✅ 初始版本：11 个文档 + schema

---

## 开发路线图

开发进度见 [ROADMAP.md](ROADMAP.md)。

---

## 目录结构

```
todos/                        ← 独立项目目录（不在 etf_strategy 下）
│
├── 文档（面向不同角色）
│   ├── SKILL.md              ← 技能定义 + 最佳实践（开发者视角）
│   ├── README.md             ← 本文件：用户文档
│   ├── DESIGN.md             ← 技术设计（开发者视角）
│   ├── SECURITY.md           ← 安全扫描报告（安装前必读）
│   ├── INSTALL.md            ← 安装指南 + 验证步骤
│   ├── EXAMPLES.md           ← 触发示例（agent 视角）
│   ├── CHANGELOG.md          ← 版本历史 + 未来计划
│   └── CONTRIBUTING.md       ← 贡献指南 + Issue 模板
│
├── 元数据
│   ├── manifest.yaml         ← skill 元数据（qwenpaw skills list 识别）
│   ├── requirements.txt       ← Python 依赖清单
│   └── .gitignore            ← Git 排除规范
│
├── schema/                   ← 数据库 schema（版本控制）
│   └── init_todos.sql        ← v1.0 schema
│
├── src/                      ← 源代码（已完成）
│   ├── __init__.py           ← 包入口
│   ├── exceptions.py         ← 4 个异常类型
│   ├── store.py              ← 数据层（11 个方法 + WAL 并发）
│   ├── cli.py                ← CLI 8 子命令
│   ├── nl_parser.py          ← NLP 解析（regex + dateutil + jieba）
│   ├── reminder.py           ← 定时提醒（4 个子命令）
│   ├── init_database.py      ← 数据库初始化脚本
│   └── etf_integration.py    ← ETF 联动 [未实现 - Phase 7 暂缓]
│
├── tests/                    ← 测试目录（已完成，91 个用例）
│   ├── test_store.py         ← 21 个 store 测试
│   ├── test_cli.py           ← 19 个 CLI 测试
│   ├── test_nl_parser.py     ← 32 个 NLP 测试
│   ├── test_reminder.py      ← 16 个 reminder 测试
│   └── test_nl_regression.py ← 3 个数据驱动回归测试
│
├── references/               ← 渐进式披露文档
│   ├── triggers.md           ← 触发词完整列表
│   ├── commands.md           ← CLI 命令参考
│   └── errors.md             ← 错误处理 + 降级路径
│
├── data/                     ← NLP 数据
│   ├── user_dict.txt         ← jieba 自定义词典
│   ├── time_keywords.txt     ← 时间关键词白名单
│   └── test_cases.json       ← 20 个回归测试 case
│
├── scripts/                  ← 工具脚本
│   ├── pre_commit_check.sh   ← 提交前隐私检查
│   └── cron_setup.sh         ← 定时任务一键部署
│
├── docs/                     ← 文档（占位，详见根目录 .md 文件）
│
├── pyproject.toml            ← PEP 621 项目元数据
├── cliff.toml                ← git-cliff 配置（CHANGELOG 自动化）
│
├── todos/                    ← 运行时数据目录（不入 git）
│   ├── config.json           ← 提醒通道配置（v1.5.0 新增）
│   └── fallback.json         ← DB 异常时的降级文件
│
├── todos.db                  ← SQLite 数据库（不入 git）
├── todos.db.bak              ← 每日备份（7 天滚动，不入 git）
└── LICENSE                   ← AGPL 开源协议
```

**说明**：
- `src/` 含 7 个模块（store/cli/nl_parser/reminder/exceptions/init_database/etf_integration）
- `tests/` 含 5 个测试文件，94 个用例，81% 覆盖率
- `todos.db` 和 `todos.db.bak` 不入 git（见 .gitignore）
- 所有文档版本：v1.5 | 日期：2026-06-11