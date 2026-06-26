---
name: task-memory
description: |
  任务遗忘防护系统 — 解决 AI Agent 任务发出但未执行的记忆漏洞问题。
  当需要创建、追踪、管理长期任务时使用，特别是：提出或承诺了某项计划后、设置 cron/自动化任务时、任务状态变更后、晨间/心跳检查时。
  核心功能：通过 todo.json 持久化任务状态，todo_manager.py 管理增/查/改/完成，系统自动追踪不过期。
---

# Task Memory — 任务遗忘防护系统

## 核心原则

**做 A 的同时必须完成 B，不能分开两步。**

AI Agent 的记忆是每次重新初始化，但任务必须是持续的。"发消息给用户说会做 X" ≠ "任务被追踪"。必须写入 todo.json 才能被系统自动管理。

## 触发场景

当以下场景发生时，必须使用本技能：

1. **提出或承诺了某项计划** → 立刻调用 `todo_manager.py --add`
2. **用户交代了任务** → 立即登记，设置 deadline
3. **任务状态变更**（完成/废弃/遇到障碍）→ 调用 `--done` 或 `--remove`
4. **会话开场（晨间）** → 运行 `--check`，报告过期/即将到期的任务
5. **心跳检查** → 运行 `--check`，有过期项推送到 QQ/IM
6. **设置 cron/自动化任务** → 自动化执行的同时必须登记 todo

## 快速命令

```bash
# 登记任务（每次承诺后必须执行）
python3 scripts/todo_manager.py --add "任务描述" --tag <标签> --system --deadline "YYYY-MM-DD"
# 注意：deadline 格式必须为 YYYY-MM-DD，不合法会报错拒绝

# 会话开场 / 心跳检查（自动运行）
python3 scripts/todo_manager.py --check

# 列出所有任务
python3 scripts/todo_manager.py --list

# 任务完成（自动归档，保留30天）
python3 scripts/todo_manager.py --done <id>

# 删除任务
python3 scripts/todo_manager.py --remove <id>

# 查看归档（30天内）
python3 scripts/todo_manager.py --archive

# 清理30天前归档
python3 scripts/todo_manager.py --purge

# 更新任务
python3 scripts/todo_manager.py --update <id> --title "新描述"
```

## 工作流

### 工作流1：主动提出计划

```
用户：我们来做 BTC 监控自动化吧
→ 思考：这是一个持续性任务，需要登记
→ 调用 --add "BTC MACD实盘监控自动化" --tag btc_monitor --system --deadline 今天
→ 写监控脚本
→ 设置 cron
→ --done <id>
```

### 工作流2：用户交代任务

```
用户：帮我验证 ETH 回测策略
→ 调用 --add "验证ETH回测策略" --tag research --deadline "YYYY-MM-DD"
→ 执行
→ --done <id>
→ 告知用户完成
```

### 工作流3：晨间检查

```
会话开场
→ python3 scripts/todo_manager.py --check
→ 输出：
  ⚠️ 已过期:
    [id] A股模拟账户持仓5只 (截止: 昨天)
  📅 即将到期:
    [id] 策略验证 (截止: 今天)
→ 主动报告给用户
```

### 工作流4：任务完成

```
任务完成后
→ --done <id>
→ 同时更新相关状态文件
→ 告知用户"已完成"
```

## 文件结构

```
task-memory/
├── SKILL.md                    ← 本文件
├── scripts/
│   └── todo_manager.py        ← 任务管理工具（Python）
└── references/
    └── todo.json               ← 任务数据库（运行时会创建）
```

## todo.json 结构

```json
{
  "version": "1.0",
  "updated": "2026-04-01T00:00:00+08:00",
  "items": [
    {
      "id": "c3436d4d",
      "title": "A股模拟账户 - 持仓5只",
      "created": "2026-04-01T00:00:00+08:00",
      "deadline": "2026-04-01",
      "status": "pending",
      "tag": "paper_trading",
      "system": true,
      "notes": "每只10万，09:25买入",
      "completed_at": null
    }
  ]
}
```

字段说明：
- `id`: 唯一标识（8位 UUID）
- `title`: 任务描述
- `deadline`: ISO 格式截止日期（YYYY-MM-DD）
- `status`: pending / in_progress / completed / cancelled
- `tag`: 分类标签（见下表）
- `system`: true = agent 主动提出，false = 用户交代
- `notes`: 额外备注
- `completed_at`: 完成时间（自动填充）

## 标签使用

| 标签 | 用途 |
|------|------|
| paper_trading | 模拟交易相关 |
| btc_monitor | 加密货币监控相关 |
| research | 研究调研任务 |
| other | 其他 |

## 知识库

详细版本历史、设计决策、已知局限、未来计划：
→ `references/CHANGELOG.md`

## 重要规则

1. **deadline 格式**：必须是 ISO 格式（YYYY-MM-DD），否则 `--check` 无法识别过期
2. **过期不过期只看 deadline**：`status` 字段不影响过期判断
3. **todo.json 路径**：默认保存在当前目录 `references/todo.json`，部署时可调整
4. **system 标记**：区分"agent 主动提出的"和"用户交代的"
5. **承诺即登记**：任何计划在告诉用户的同时，必须完成 --add 登记

## AGENTS.md 集成

在会话开场规则中加入 Todo 扫描：

```markdown
6. Todo 扫描: 运行 `python3 scripts/todo_manager.py --check`
   有过期/即将到期的系统任务 → 在晨间汇报里报告
```

在 `HEARTBEAT.md` 中加入心跳检查：

```markdown
## Todo 过期检查
每次心跳运行 `python3 scripts/todo_manager.py --check`
有过期项 → 推送提醒到 QQ/IM
```
