---
name: "shipping-price-monitor"
description: "Monitor shipping carrier prices from Excel files and send alerts when prices drop below thresholds. Invoke when user mentions shipping price monitoring, price alerts, or wants to track carrier rates."
---

# 海运报价监控助手 (Shipping Price Monitor)

实时监控船司报价数据，当价格低于预警阈值时自动发送通知到企业微信/飞书。

## 目录结构

```
shipping-price-monitor/
├── config/
│   ├── settings.yaml      # 主配置（监控、通知、日志）
│   └── rules.json         # 用户自定义预警规则
├── data/
│   ├── watch/             # 监控目录（八爪鱼输出Excel）
│   └── history/           # 历史数据存档
├── core/
│   ├── monitor.py         # 文件监控引擎
│   ├── analyzer.py        # 价格分析器
│   └── notifier.py        # 通知发送器
├── services/
│   ├── feishu_bot.py      # 飞书机器人（优先长连接）
│   └── wecom_bot.py       # 企业微信机器人（优先长连接）
├── main.py                # 主入口
└── SKILL.md               # 本文档
```

## 激活条件

当用户提到以下内容时激活：
- "船司报价监控" / "运价监控" / "运费监控"
- "特价预警" / "价格预警"
- "开启监控" / "关闭监控"
- "设置预警规则"
- "price alert" / "shipping monitor"

## 功能特性

- ✅ 实时监控 Excel 文件变化（文件监控模式）
- ✅ 支持多箱型价格阈值（20GP/40GP/40HQ）
- ✅ 支持多起运港、目的港、船公司筛选
- ✅ 支持有效期过滤
- ✅ **优先 OpenClaw 长连接通知**（无需配置 Webhook）
- ✅ 自动回退 Webhook 机制
- ✅ 防重复通知机制
- ✅ 多规则管理

## 通知机制

### 发送优先级

```
发送通知
    │
    ▼
┌─────────────────────────────┐
│  1. 优先 OpenClaw 长连接     │
│     无需配置 Webhook         │
│     自动通过 OpenClaw 发送   │
└─────────────┬───────────────┘
              │ 失败
              ▼
┌─────────────────────────────┐
│  2. 回退 Webhook            │
│     需配置 Webhook 地址      │
│     直接调用 API             │
└─────────────┬───────────────┘
              │ 失败
              ▼
┌─────────────────────────────┐
│  3. 返回详细错误信息         │
└─────────────────────────────┘
```

### 通知渠道

| 渠道 | 长连接 | Webhook | 推荐度 |
|------|--------|---------|--------|
| 企业微信 | ✅ 优先使用 | ⚠️ 难获取 | ⭐⭐⭐⭐⭐ |
| 飞书 | ✅ 优先使用 | ✅ 简单 | ⭐⭐⭐⭐⭐ |

**企业微信推荐使用长连接方式**，无需配置 Webhook 地址即可发送通知。

## 使用流程

### 1. 选择通知渠道（可选配置 Webhook）

**方式一：使用 OpenClaw 长连接（推荐，无需配置）**
```
设置通知渠道：企业微信
```

**方式二：配置 Webhook（可选，作为备用）**
```
设置企业微信 Webhook: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
设置飞书 Webhook: https://open.feishu.cn/open-apis/bot/v2/hook/xxx
```

### 2. 设置预警规则

```
添加预警规则：
名称：欧洲航线特价预警
起运港：SHANGHAI, NINGBO, YANTIAN
目的港：LONDON GATEWAY, BREMERHAVEN, WILHELMSHAVEN, GOTHENBURG, ANTWERP, LE HAVRE, ROTTERDAM, HAMBURG, GDANSK
阈值：20GP < 1400，40GP/40HQ < 2400
船公司：MSK, HPL
有效期：03/30-04/05
```

### 3. 设置监控目录

```
设置监控目录：C:\Users\User\.openclaw\media\inbound
```

### 4. 开启监控

```
开启监控
```

## 命令列表

| 命令 | 说明 |
|------|------|
| 开启监控 | 启动价格监控 |
| 关闭监控 | 停止价格监控 |
| 立即检查 | 手动触发一次检查 |
| 查看状态 | 查看当前配置和状态 |
| 测试通知 | 测试通知连接 |
| 添加规则 | 添加新的预警规则 |
| 删除规则 | 删除指定规则 |

## Excel 数据格式要求

| 列名 | 说明 | 示例 |
|------|------|------|
| POL | 起运港 | NINGBO |
| POD | 目的港 | ROTTERDAM |
| CARRIER | 船公司 | MSK |
| ETD | 开船日期 | 2026-03-30 |
| 20GP | 20GP价格 | 1350 |
| 40GP | 40GP价格 | 2200 |
| 40HQ | 40HQ价格 | 2250 |

## 预警通知示例

```
🚢 特价预警通知

━━━━━━━━━━━━━━━━━━━━
1. 20GP $1285 (阈值: $1400)
   NINGBO → ROTTERDAM
   船公司: HPL | 开船: 2026-03-27

2. 40GP $2035 (阈值: $2400)
   SHANGHAI → ANTWERP
   船公司: MSK | 开船: 2026-04-02
━━━━━━━━━━━━━━━━━━━━
共发现 2 条特价
```

## 配置文件说明

### settings.yaml

```yaml
monitor:
  enabled: false
  check_interval: 60
  watch_directory: ""
  excel_path: ""

notification:
  channel: wecom      # wecom 或 feishu
  feishu_webhook: ""  # 可选，作为备用
  wecom_webhook: ""   # 可选，作为备用

logging:
  level: INFO
  file: monitor.log

data:
  history_dir: "data/history"
  watch_dir: "data/watch"
```

### rules.json

```json
{
  "rules": [
    {
      "id": "rule_001",
      "name": "欧洲航线特价预警",
      "enabled": true,
      "pol": ["SHANGHAI", "NINGBO", "YANTIAN"],
      "pod": ["LONDON GATEWAY", "BREMERHAVEN", ...],
      "carriers": ["MSK", "HPL"],
      "thresholds": {
        "20GP": 1400,
        "40GP": 2400,
        "40HQ": 2400
      },
      "valid_period": {
        "start": "2026-03-30",
        "end": "2026-04-05"
      },
      "description": "欧洲主要港口运价低于阈值时预警"
    }
  ]
}
```

## 与八爪鱼 RPA 配合

1. 八爪鱼 RPA 定时爬取数据，保存到 `data/watch/` 目录
2. 文件监控检测到新文件，自动触发检查
3. 发现低价自动发送通知（优先长连接）

## 命令行用法

```bash
# 启动监控
python main.py start

# 停止监控
python main.py stop

# 手动检查
python main.py check [excel_path]

# 查看状态
python main.py status

# 测试通知
python main.py test [wecom|feishu]
```

## 状态显示示例

```
==================================================
       海运报价监控助手 - 状态
==================================================

[监控状态]
  已启用: ✅
  运行中: ✅
  监控目录: C:\Users\User\.openclaw\media\inbound
  Excel路径: 
  检查间隔: 60秒
  启用规则数: 1

[通知配置]
  当前渠道: wecom
  默认目标: Liam
  OpenClaw长连接:
    企业微信: ✅ 可用
    飞书: ✅ 可用
  Webhook配置:
    企业微信: ❌ 未配置
    飞书: ❌ 未配置

[预警规则] 共 1 条
  ✅ 欧洲航线特价预警 (ID: rule_001)
      起运港: 3个, 目的港: 9个
      船司: MSK, HPL
      阈值: 20GP=$1400, 40GP=$2400, 40HQ=$2400

==================================================
```

## 错误处理

当通知发送失败时，会返回详细的错误信息：

```
❌ 所有通知方式均失败 - 长连接: OpenClaw 发送失败: xxx | Webhook: 未配置 Webhook
```

这样可以清楚地知道是哪个环节出了问题。
