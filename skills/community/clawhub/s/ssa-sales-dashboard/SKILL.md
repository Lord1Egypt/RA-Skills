# Sales Dashboard 销售仪表盘

## 描述
渐进式销售数据概览，从 OKKI CRM 和 Campaign Tracker 采集核心指标，生成周报/月报，通过 Discord 推送。

## 架构

```
scripts/
├── data-collector.js      # 数据采集（OKKI API + 可选数据源）
├── metrics-calculator.js  # 指标计算（漏斗 + 环比 + 异常检测）
├── report-generator.js    # Markdown 报告生成（周报/月报）
└── discord-push.js        # Discord 推送（自动分片 >1800 字符）

config/
└── dashboard-config.json  # KPI 定义 / 数据源映射 / 告警阈值

data/
├── latest.json            # 最新一次采集的指标
├── calculated.json        # 计算后的指标（含漏斗/告警）
├── snapshots/             # 历史快照（{period}-{date}.json）
└── reports/               # Markdown 报告
```

## 数据源

| 数据源 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| OKKI CRM | ✅ | API | 客户/订单/报价/线索/商机 |
| campaign-tracker | ❌ | 文件 | 邮件发送量/回复率 |
| follow-up-engine | ❌ | 文件 | 跟进数据 |
| order-tracker | ❌ | 文件 | 订单跟踪 |
| customer-segmentation | ❌ | 文件 | 客户分群 |
| pricing-engine | ❌ | 文件 | 定价数据 |

缺失的可选数据源显示 N/A，不报错。

## 用法

### 采集数据
```bash
node scripts/data-collector.js --period weekly [--date 2026-03-24] [--dry-run]
node scripts/data-collector.js --period monthly [--date 2026-03-01]
```

### 计算指标
```bash
node scripts/metrics-calculator.js --check-alerts
```

### 生成报告
```bash
node scripts/report-generator.js --period weekly [--dry-run]
node scripts/report-generator.js --period monthly
```

### Discord 推送
```bash
# 推送最新周报
node scripts/discord-push.js --latest-report weekly

# 推送指定报告
node scripts/discord-push.js --report data/reports/weekly-2026-03-24.md

# 手动告警
node scripts/discord-push.js --alert "⚠️ 订单金额异常下降"
```

## 定时任务（OpenClaw cron）

| 任务 | Cron ID | 时间 | 说明 |
|------|---------|------|------|
| 周报 | bbdf51a8-36e0-4ee9-824b-0c92f7a44bf1 | 每周一 09:00 CST | 采集 + 计算 + 生成 + 推送 |
| 月报 | 13e4378e-655e-4082-8bc0-c8fbd8e91c12 | 每月 1 日 09:00 CST | 采集 + 计算 + 生成 + 推送 |

## 告警阈值（保守初始值）

| 指标 | 条件 | 阈值 |
|------|------|------|
| 邮件回复率 | 低于 | 10% |
| 订单金额 | 环比下降超 | 50% |
| 周订单数 | 等于 | 0 |

## 历史快照机制

每次采集保存 `data/snapshots/{period}-{date}.json`，永不覆盖。
`data/latest.json` 每次更新为最新数据。
环比计算自动读取上一期快照。

## 已知问题 & 改进记录

### v1.0.1 (2026-03-25)
- **修复**: Campaign Tracker reply_rate 从小数 (0.667) 正确转换为百分比 (66.7%)
- **修复**: Campaign Tracker JSON 报告嵌套 metrics 字段兼容
- **新增**: OpenClaw cron 定时任务（周报 + 月报）已创建
- **验证**: OKKI API 时间过滤正常工作（start_time/end_time/time_type 参数）
- **验证**: 历史快照机制正常（data/snapshots/）
- **待优化**: OKKI 沙盒环境数据为空（全 0），切换生产环境后验证

---

**版本:** 1.0.1
**创建:** 2026-03-25
**更新:** 2026-03-25
