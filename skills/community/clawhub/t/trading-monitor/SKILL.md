---
name: trading-monitor
description: 盘中股票盯盘定时任务管理。创建、配置和管理A股交易时段的自动分析任务，包括定时行情播报、深度分析、收盘前最终分析。使用场景：设置盯盘、调整分析频率、查看任务状态、停止/启动任务。触发词：盯盘、设置分析、开盘监控、调整频率、盯盘任务。
---

# 盘中股票盯盘系统

自动化A股交易时段的定时分析任务，通过 OpenClaw Cron 系统驱动。

## 快速开始

### 一键部署（推荐）

运行部署脚本，按提示输入参数：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\setup.ps1 -Channel feishu -Target "ou_你的ID"
```

高级参数：

```powershell
# 深度分析 + 开盘前准备
.\scripts\setup.ps1 -Channel feishu -Target "ou_xxx" -AnalysisDepth full -IncludePreMarket

# 每5分钟高频盯盘
.\scripts\setup.ps1 -Channel feishu -Target "ou_xxx" -Interval 5

# 低频监控（省token）
.\scripts\setup.ps1 -Channel feishu -Target "ou_xxx" -Interval 30 -AnalysisDepth basic
```

### 管理任务

```powershell
# 查看所有任务状态
powershell -ExecutionPolicy Bypass -File scripts\manage.ps1 list

# 查看系统配置
.\scripts\manage.ps1 status

# 手动触发测试
.\scripts\manage.ps1 test

# 停止所有任务
.\scripts\manage.ps1 stop
```

### 手动创建

参考下方"任务类型"和 `references\config-guide.md`，用 `openclaw cron create` 命令手动创建。

## 任务类型

### 1. 盘中定时分析（每N分钟）

交易时段内每N分钟自动分析持仓+大盘+新闻+操作建议。

```
openclaw cron create --name "盘中盯盘" --cron "*/15 9-15 * * 1-5" --tz "Asia/Shanghai" --session isolated --wake now --message "你是水水琪，独立操盘手。执行：1.查询持仓股票行情 2.查询大盘指数 3.搜索今日A股重要新闻 4.分析板块轮动和主线 5.评估持仓并给出操作建议 6.发送报告给方休（股票带代码）" --timeout-seconds 300 --announce --channel <频道> --to <目标ID>
```

### 2. 收盘前最终分析（14:53）

集合竞价前4分钟触发，给操作留时间。

```
openclaw cron create --name "收盘前分析" --cron "53 14 * * 1-5" --tz "Asia/Shanghai" --session isolated --wake now --message "最终分析：1.查询持仓最终行情 2.大盘收盘预判 3.评估集合竞价操作 4.给出明确指令（买/卖/不动）5.发送报告" --timeout-seconds 300 --announce --channel <频道> --to <目标ID>
```

### 3. 开盘前准备（8:30）

每日开盘前选股分析。

```
openclaw cron create --name "开盘前分析" --cron "30 8 * * 1-5" --tz "Asia/Shanghai" --session isolated --wake now --message "开盘前分析：1.搜索overnight重要新闻 2.检查持仓状态 3.预判今日主线 4.制定操作计划 5.发送报告" --timeout-seconds 300 --announce --channel <频道> --to <目标ID>
```

## 管理命令

```powershell
# 查看所有任务
openclaw cron list

# 停用任务（按名称模糊匹配）
openclaw cron list --json | findstr "任务名"

# 删除任务
openclaw cron delete <任务ID>

# 手动触发测试
openclaw cron trigger <任务ID>
```

## 配置参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--cron` | Cron表达式 | `*/15 9-15 * * 1-5` |
| `--channel` | 推送渠道 | `feishu` |
| `--to` | 推送目标ID | 需填写 |
| `--timeout-seconds` | 超时时间 | `300` |
| `--session` | 会话模式 | `isolated` |
| `--message` | 分析指令 | 见上方模板 |

## 常用频率

- `*/5 9-15 * * 1-5` — 每5分钟（高频盯盘）
- `*/15 9-15 * * 1-5` — 每15分钟（推荐）
- `*/30 9-15 * * 1-5` — 每30分钟（低频）
- `0 9,10,11,13,14 * * 1-5` — 每小时整点
- `53 14 * * 1-5` — 每日14:53（收盘前）

## 注意事项

- Cron表达式 `1-5` = 周一到周五，周末自动跳过
- `--session isolated` 让每次分析在独立会话运行，不污染主对话
- `--announce` 确保分析结果推送到指定渠道
- 超时建议300秒（分析需要调用多个工具）
- 收盘前分析设在14:53，给集合竞价（14:57-15:00）留4分钟决策时间

## 常见问题

### 任务报错 "exec denied: allowlist miss"
原因：`tools.exec.security` 设为 `allowlist` 但 `paths` 为空。
修复：`openclaw config set tools.exec.security full` 后重启 gateway。

### 任务报错但 exec 正常
检查是否是超时（默认30秒太短），用 `--timeout-seconds 300`。
