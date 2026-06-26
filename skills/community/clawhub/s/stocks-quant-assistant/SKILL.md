# 📈 stocks-quant-assistant

**⚠️ 安全说明**

本技能本地配置文件（`config.local.yaml`）**不会**随技能发布，包含您的私人凭证和持仓数据，请放心使用。  
定时任务健康检查**不会**自动重建含私密凭证的配置，仅生成空白模板引导用户填写。

首次运行自动安装依赖 + 注册定时任务，每日 4 次自动推送。

---

## 功能特性

✅ **自动分析**
- 股票：MA/MACD/RSI/布林带技术指标分析
- 基金：估算净值实时跟踪（以博时黄金ETF为例）
- 信号评分和操作建议

✅ **定时推送**
- 每日 4 次自动推送（09:15/10:00/13:00/14:50）
- 支持飞书/Telegram 推送

✅ **持仓跟踪**
- 持仓盈亏计算
- 止盈止损建议

---

## 快速开始

### 安装

```bash
cd ~/.openclaw/workspace/skills/stocks-quant-assistant
pip install -r requirements.txt
```

### 配置

编辑 `config.yaml`，填写股票和凭证：

```yaml
stocks:
  - code: "000001"          # 股票代码
    name: "平安银行"         # 显示名称
    market: "sz"             # sz=深交所，sh=上交所
    emoji: "🏦"              # 自定义图标

  - code: "002611"          # 基金代码
    name: "博时黄金ETF联接C"
    type: "fund"             # 类型：fund = 基金，默认或 type: stock = 股票
    emoji: "🥇"
    position:               # 可选：持仓信息
      cost: 3.05
      quantity: 4100

push:
  channel: "feishu"          # 推送渠道
  feishu:
    app_id: "cli_xxxxxxxx"   # 飞书 App ID
    app_secret: "xxxxxxxx"   # 飞书 App Secret
    chat_id: "oc_xxxxxxx"    # 飞群 chat_id
```

### 使用

```bash
# 手动触发推送
python3 stock_monitor.py morning    # 开盘前
python3 stock_monitor.py noon        # 早盘
python3 stock_monitor.py afternoon   # 午后
python3 stock_monitor.py evening    # 尾盘
```

---

## 常见问题

### ❌ 报错 "Feishu push failed" / 飞书没收到

**原因：** 凭证填写不完整

**解决：**
1. 确认 `config.yaml` 中 `feishu` 区块三个字段都有值
2. 检查 `app_id`（格式：`cli_xxxxxxxx`）
3. 检查 `chat_id`（格式：`oc_xxxxxxxx`）

### ❌ 报错 "launchd 注册失败" / 定时推送没收到

**原因：** macOS 权限限制

**解决：**
```bash
launchctl load ~/Library/LaunchAgents/com.openclaw.stock-monitor.plist
# 如需管理员权限，加上 sudo
sudo launchctl load ~/Library/LaunchAgents/com.openclaw.stock-monitor.plist
```

### ❌ 提示「实时数据获取失败」

**原因：** 网络波动，新浪财经接口超时

**解决：** 系统会自动降级为简化模式，下次定时任务会自动恢复

---

## 定时任务状态检查

```bash
# macOS - 查看 launchd 任务
launchctl list | grep stock

# 查看最近一次推送日志
cat logs/launchd.log
cat logs/launchd.err
```

---

## 信号评分规则

| 分数 | 信号 | 含义 |
|------|------|------|
| ≥7 | 🟢 强烈买入 | 多个指标共振，看涨信号强 |
| 4~6 | 🟢 买入 | 技术面不错，可以考虑买入 |
| -3~3 | 🟡 持有 | 中性信号，建议观望 |
| -6~-4 | 🔴 卖出 | 技术面偏弱，考虑减仓 |
| ≤-7 | 🔴 强烈卖出 | 技术面很弱，建议清仓 |

---

## 技术指标

| 指标 | 是什么 | 怎么看 |
|------|--------|--------|
| **MA（均线）** | 过去N天平均价格连线 | 多头排列（短>长）= 上涨；空头排列 = 下跌 |
| **MACD** | 快线、慢线、红绿柱 | **金叉**=买入信号；**死叉**=卖出信号 |
| **RSI** | 涨跌强度，0~100 | >70超买可能回调；<30超卖可能反弹 |
| **布林带** | 价格通道（上轨/中轨/下轨） | 价格碰下轨可能反弹；碰上轨可能回落 |

---

## 市场代码

| 市场 | 代码 | 示例 |
|------|------|------|
| 上交所 | `sh` | 600519（茅台）、588080（科创50ETF） |
| 深交所 | `sz` | 000001（平安）、002131（利欧） |
| 北交所 | `bj` | 8开头股票 |

## 基金监控

基金（如黄金ETF联接基金）与股票使用不同的数据接口：

- 基金使用**天天基金网**实时估算净值接口
- 基金**不需要**技术指标（MA/MACD/RSI），主要看净值走势
- 基金支持**黄金价格参考**（与黄金现货价格联动）

```yaml
- code: "002611"      # 基金代码（天天基金网代码）
  name: "博时黄金ETF联接C"
  type: "fund"         # 关键：声明为 fund 类型
  emoji: "🥇"
  position:
    cost: 3.0592       # 单位净值成本
    quantity: 4118.69  # 持有份额
```

---

## 文件结构

```
stocks-quant-assistant/
├── SKILL.md              # 本文件
├── stock_monitor.py      # 主脚本
├── config.yaml           # 配置文件
├── config.local.yaml     # 私人配置（不会被覆盖）
├── requirements.txt      # Python依赖
├── health_check.py       # 健康检查脚本
├── logs/                 # 日志目录
│   ├── launchd.log
│   └── launchd.err
└── LaunchAgents/         # macOS 定时任务
    └── com.openclaw.stock-monitor.plist
```

---

*版本：3.1.0*  
*最后更新：2026-03-26*
