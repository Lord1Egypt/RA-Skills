# todo-list Skill — CLI 命令参考

> 版本：v1.0 | 更新：2026-06-11
>
> 详细的 CLI 8 子命令文档。SKILL.md 只列决策树，完整参数见此文档。

## 8 个子命令

### add — 添加 TODO

```bash
python3 -m src.cli add "内容" [options]

options:
  --active-form  进行时（默认从 content 推断）
  --due          截止时间（ISO8601 字符串）
  --priority     优先级 high/medium/low（默认 medium）
  --tag          标签（逗号分隔）
  --db-path      数据库路径
```

**示例**：
```bash
python3 -m src.cli add "检查515070止损" --priority high
python3 -m src.cli add "开会" --due "2026-06-12 15:00:00" --tag "work,meeting"
```

### list — 查询 TODO

```bash
python3 -m src.cli list [options]

options:
  --status       按状态过滤
  --tag          按标签过滤
  --priority     按优先级过滤（high/medium/low）
  --overdue      只显示过期
  --all          显示所有状态
  --format       text/json（默认 text）
  --db-path      数据库路径
```

**示例**：
```bash
python3 -m src.cli list                       # 默认
python3 -m src.cli list --priority high       # 高优
python3 -m src.cli list --overdue             # 过期
python3 -m src.cli list --format json         # JSON 输出
```

### done — 完成 TODO

```bash
python3 -m src.cli done "ID 或 content 模糊匹配"

# 退出码 1：如果未找到或歧义
```

**示例**：
```bash
python3 -m src.cli done 1              # 按 ID
python3 -m src.cli done "检查515070"   # 按 content
```

### delete — 软删除

```bash
python3 -m src.cli delete "ID 或 content 模糊匹配"

# 软删除：移入 archive 表，状态改为 cancelled
```

### update — 更新字段

```bash
python3 -m src.cli update ID [options]

options:
  --content      新内容
  --due          新截止时间
  --priority     新优先级
  --tag          新标签
  --status       新状态
```

**示例**：
```bash
python3 -m src.cli update 1 --priority high
python3 -m src.cli update 1 --status in_progress
```

### stats — 统计

```bash
python3 -m src.cli stats [options]
options:
  --format       text/json（默认 text）
```

**输出**：
- 总数 / 待办 / 进行中 / 已完成 / 取消 / 过期
- 高/中/低 优先级
- 本周到期

### init — 初始化数据库

```bash
python3 -m src.cli init
# 幂等，可多次调用
```

### check-overdue — 批量标记过期

```bash
python3 -m src.cli check-overdue
# 每天 00:05 由 cron 调用
```

## 全局参数

```bash
--format {text,json}   输出格式（默认 text）
--db-path PATH         数据库路径
```

## 退出码

| 退出码 | 含义 |
|:---:|------|
| 0 | 成功 |
| 1 | 业务错误（未找到/歧义） |
| 2 | 用法错误（参数/校验） |
| 70 | 系统错误（DB 损坏） |
