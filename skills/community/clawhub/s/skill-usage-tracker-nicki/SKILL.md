---
name: skill-usage-tracker
description: 技能调用记录与统计分析。自动追踪所有技能调用，无需用户操作。支持日/周/月/季/年维度的技能使用统计报告。安装后直接使用，无需配置。
---

# 技能使用记录与统计

## 功能

- **自动记录**：每次调用技能时自动记录，无需用户操作
- **手动汇报**：主动告知用户"刚才调用了 XXX 技能"
- **统计报告**：支持日/周/月/季/年维度生成使用报告

## 文件结构

```
skill-usage-tracker/
├── SKILL.md
├── scripts/
│   ├── log.py      # 记录调用
│   └── query.py    # 查询统计
└── data/
    └── usage.json  # 调用记录存储
```

## 记录方式

**自动记录（主要）**：通过 HEARTBEAT 每2小时扫描 session 历史自动补录
**主动汇报**：每次调用技能后在回复末尾告知用户

## 查询统计

当用户请求报告时调用 query.py：

```bash
python3 ~/.openclaw/workspace/skills/skill-usage-tracker/scripts/query.py <维度>
```

**维度选项：**
| 维度 | 说明 |
|------|------|
| 日 | 今天 |
| 周 | 本周一至今（默认） |
| 月 | 本月 |
| 季 | 本季度 |
| 年 | 本年 |

## 输出格式

```
技能使用报告 - 本周（03月24日 至 03月29日）

总调用次数：15次

⏱ 滚动窗口（5小时）
━━━━━━━━━━━━━━━━━━━
🟢 minimax-token-plan
   8次 · 53.3%
🟡 camoufox
   5次 · 33.3%
🔵 feishu-task
   2次 · 13.3%
```

## 数据结构

`usage.json`:
```json
{
  "records": [
    {
      "skill": "minimax-token-plan",
      "called_at": "2026-03-29T16:30:00+00:00",
      "note": ""
    }
  ]
}
```
