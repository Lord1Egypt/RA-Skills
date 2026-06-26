---
name: retail-target-tracking-analysis
description: |
  门店目标追踪分析工具。支持日/周/月三周期目标追踪，T-N数据延迟，黄绿黄灯状态预警。
  
  核心能力：
  1. 三周期追踪（日追踪-晨会/实时预警、周追踪-周会复盘、月追踪-月度考核）
  2. T-N数据延迟支持（默认T-1）
  3. 黄绿黄灯状态（🟢正常、🟡关注、🟠警告、🔴告警/紧急）
  4. 批量告警检查（检查所有门店，按优先级排序）
  5. 定时任务预留接口
  
  触发条件：
  - 用户询问目标达成（如"本月目标达成率"）
  - 用户需要预警（如"哪些门店需要关注"）
  - 用户追踪业绩（如"业绩进度如何"）
---

# 目标追踪分析 Skill

## 技能名称
`target-tracking-analysis`

## 版本
v3.0

## 功能描述
门店目标追踪分析工具，支持日/周/月三周期目标追踪，T-N数据延迟，黄绿黄灯状态预警。

## 核心能力

### 1. 三周期追踪支持
- **日追踪** (`daily`) - 晨会、实时预警
- **周追踪** (`weekly`) - 周会复盘
- **月追踪** (`monthly`) - 月度考核

### 2. T-N数据延迟支持
```python
# T-1数据（默认）
analyze(store_id, store_code, period="daily", current_date="2026-03-25")

# 定时任务检查
check_alerts(store_id, store_code, period="daily", t_minus=1)
```

### 3. 黄绿黄灯状态
| 达成率 | 图标 | 状态 | 告警级别 |
|--------|------|------|----------|
| ≥100% | 🟢 | 正常 | normal |
| 95-100% | 🟡 | 关注 | watch |
| 85-95% | 🟠 | 警告 | warning |
| 70-85% | 🔴 | 告警 | alert |
| <70% | 🔴 | 紧急 | critical |

### 4. 批量告警检查
```python
from analyze import check_alerts_batch

# 检查所有门店
alerts = check_alerts_batch(period="daily", t_minus=1)
# 返回按优先级排序的告警列表
```

## 使用示例

```python
from analyze import analyze, format_report

# 单门店分析
result = analyze(
    store_id="1e7653_1750409683578",
    store_code="420111020",
    period="monthly",
    current_date="2026-03-25"
)

print(format_report(result))
```

## 定时任务预留接口

```bash
# 每日9:00检查T-1数据
0 9 * * * python3 -c "
from target_tracking.analyze import check_alerts_batch
alerts = check_alerts_batch('daily', t_minus=1)
# 接入通知渠道
"
```

## 数据文件

- **每日目标**: `~/.openclaw/workspace-store-ops-analyst/targets/daily_targets.json`
- **门店映射**: `~/.openclaw/cache/user_stores_114.json`

## 版本
v3.0.0 - 三周期追踪、T-N数据延迟、黄绿黄灯预警
