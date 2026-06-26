---
name: fund-monitor
description: |
  T+0 基金 5 分钟级别实时监控，支持批量代码输入，自动生成买入/卖出信号。
  
  **触发场景：**
  - "监控基金 XXX"
  - "开始监控这些代码：xxx, xxx, xxx"
  - "添加 XXX 到监控列表"
  - "查看监控信号"
  - "停止监控 XXX"
  
  支持场内 ETF、跨境 QDII、债券 ETF 等 T+0 基金。
  技术指标：MACD、KDJ、RSI、布林带、成交量。
  通知方式：终端提醒、钉钉、企业微信（可配置）。
  
  ⚠️ 数据有延迟，不构成投资建议。
homepage: https://github.com/openclaw/skills
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["python3", "pip3"] },
        "install":
          [
            {
              "id": "dependencies",
              "kind": "pip",
              "package": "akshare pandas pandas-ta APScheduler requests pyyaml",
              "label": "Install dependencies: pip3 install akshare pandas pandas-ta APScheduler requests pyyaml",
            },
          ],
      },
  }
---

# Fund Monitor Skill

T+0 基金 5 分钟级别实时监控系统。

## 快速开始

### 1. 安装依赖

```bash
pip3 install akshare pandas pandas-ta APScheduler requests pyyaml
```

### 2. 配置通知（可选）

编辑 `~/.openclaw/skills/fund-monitor/config/default.yaml`

### 3. 开始监控

```bash
# 添加基金到监控列表
~/.openclaw/skills/fund-monitor/tools/monitor.py add 512880,513050,159915

# 查看监控列表
~/.openclaw/skills/fund-monitor/tools/monitor.py list

# 启动监控
~/.openclaw/skills/fund-monitor/tools/monitor.py start

# 查看最新信号
~/.openclaw/skills/fund-monitor/tools/monitor.py signals

# 停止监控
~/.openclaw/skills/fund-monitor/tools/monitor.py stop
```

## 命令行接口

| 命令 | 说明 | 示例 |
|------|------|------|
| `add <codes>` | 添加基金到监控列表 | `add 512880,513050` |
| `list` | 查看监控列表 | `list` |
| `start` | 启动监控 | `start` |
| `stop` | 停止监控 | `stop` |
| `signals` | 查看最新信号 | `signals` |
| `remove <code>` | 移除基金 | `remove 512880` |
| `status` | 查看监控状态 | `status` |

## 信号策略

### 买入信号（同时满足）
- MACD 金叉（DIF 上穿 DEA）
- KDJ < 20（超卖区）
- 成交量 > 5 日均量 1.5 倍

### 卖出信号（满足任一）
- MACD 死叉（DIF 下穿 DEA）
- KDJ > 80（超买区）
- 跌破 5 日均线 2%

## 注意事项

⚠️ 数据有 1-5 分钟延迟，不构成投资建议
