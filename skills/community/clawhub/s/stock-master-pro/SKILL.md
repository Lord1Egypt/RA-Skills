---
name: Stock Master Pro
description: A 股智能盯盘与选股系统，基于 QVeris AI 数据源。提供持仓监控（10 分钟自动检查）、实时预警、午盘/尾盘复盘、趋势选股等功能。支持创业板和主板（不含科创板）。
  使用方式：
  - 对话触发：用户说"午盘复盘"、"我的持仓"、"帮我选股"等
  - Web 界面：访问 file:///home/yaoha/.openclaw/workspace/skills/stock-master-pro/web/index.html
read_when:
  - 用户想要监控股票持仓
  - 需要午盘或尾盘复盘
  - 想要选股或获取股票推荐
  - 询问持仓股票怎么样
  - 需要股票预警提醒
  - 想要查看图形化盯盘界面
metadata:
  clawdbot:
    emoji: 📈
    requires:
      env: QVERIS_API_KEY
      skills: qveris-official
allowed-tools: Bash(qveris_tool:*)
---

# Stock Master Pro - A 股智能盯盘与选股系统

## 依赖检查

### 首次运行前必须检查

在使用本技能前，**必须确保已安装 QVeris AI 技能**。

#### 检查命令

```bash
ls ~/.openclaw/skills/qveris-official/SKILL.md 2>/dev/null
```

#### 如果未安装

**提示用户：**

```
⚠️ 检测到未安装 QVeris AI 技能

Stock Master Pro 依赖 QVeris AI 提供股票数据。请按以下步骤安装：

1. 注册 QVeris AI（免费）
   访问：https://qveris.ai/?ref=y9d7PKgdPcPC-A

2. 获取 API Key
   登录后在控制台复制 API Key

3. 安装 QVeris Skill
   执行以下命令：
   
   curl -fSL https://qveris.ai/skill/SKILL.md -o ~/.openclaw/skills/qveris-official/SKILL.md
   curl -fSL https://qveris.ai/skill/scripts/qveris_tool.mjs -o ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs
   curl -fSL https://qveris.ai/skill/scripts/qveris_client.mjs -o ~/.openclaw/skills/qveris-official/scripts/qveris_client.mjs
   curl -fSL https://qveris.ai/skill/scripts/qveris_env.mjs -o ~/.openclaw/skills/qveris-official/scripts/qveris_env.mjs

4. 设置 API Key
   export QVERIS_API_KEY="你的 API Key"

5. 验证安装
   node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs --help
```

---

## 使用方式

### 方式 1：对话触发（推荐日常使用）

```
你："午盘复盘"
→ 系统生成文字报告
→ 附带 Web 界面链接

你："我的持仓怎么样"
→ 显示实时盈亏和预警

你："帮我选股"
→ 返回推荐股票列表
```

### 方式 2：Web Dashboard（推荐盯盘使用）

**直接打开：**
```
file:///home/yaoha/.openclaw/workspace/skills/stock-master-pro/web/index.html
```

**本地服务器：**
```bash
# 启动服务器
~/.openclaw/workspace/skills/stock-master-pro/start-web.sh

# 访问 http://localhost:3000
```

**功能：**
- 📊 大盘实时走势
- 💰 持仓盈亏监控
- 📝 复盘报告查看
- ⚠️ 实时预警推送
- 🔄 每 10 秒自动刷新

---

## 快速开始

### 1. 配置持仓

创建持仓配置文件：

```bash
mkdir -p ~/.openclaw/workspace/skills/stock-master-pro/stocks
```

创建 `~/.openclaw/workspace/skills/stock-master-pro/stocks/holdings.json`：

```json
{
  "holdings": [
    {
      "code": "000531.SZ",
      "name": "穗恒运 A",
      "cost": 7.2572,
      "shares": 700,
      "buy_date": "2026-03-20",
      "notes": "趋势票，电力概念",
      "alerts": {
        "target_price": 8.20,
        "stop_loss": 7.00,
        "change_pct": 5
      }
    }
  ],
  "watchlist": [
    {
      "code": "603259.SH",
      "name": "药明康德",
      "reason": "趋势突破，关注回踩"
    }
  ],
  "settings": {
    "check_interval_minutes": 10,
    "review_times": ["12:30", "15:30", "16:00"],
    "exclude_st": true,
    "exclude_kcb": true
  }
}
```

### 2. 开始盯盘

**用户告诉系统持仓：**

```
"我买了穗恒运 A"
→ 系统询问："成本价是多少？持有多少股？"
→ 用户："7.2572 元，700 股"
→ 系统：保存到 holdings.json，开始 10 分钟自动检查
```

### 3. 查看持仓状态

```
"我的持仓怎么样"
→ 显示所有持仓的实时行情、盈亏、预警
```

### 4. 选股

```
"帮我选股"、"推荐几只趋势票"
→ 根据右侧交易策略筛选股票
→ 返回 Top 5-10 推荐
```

### 5. 复盘

```
"午盘复盘"、"尾盘复盘"
→ 生成大盘分析、热点板块、持仓表现、操作建议
```

---

## 核心功能

### 1. 持仓监控（10 分钟自动检查）

**检查内容：**
- ✅ 实时价格、涨跌幅
- ✅ 盈亏计算（浮动盈亏、盈亏比例）
- ✅ 预警检测（目标价、止损价、涨跌幅、放量）
- ✅ 公告监控（增减持、合同、处罚）
- ✅ 财报日历（发布前提醒）
- ✅ 龙虎榜数据（机构动向）

**预警类型：**
- 🎯 目标价预警
- ⚠️ 止损预警
- 📈/📉 涨跌幅预警
- 🔥 放量预警
- 📢 公告预警
- 📅 财报提醒

### 2. 午盘/尾盘复盘

**复盘时间：**
- 午盘：12:30
- 尾盘：15:30
- 收盘总结：16:00

**复盘内容：**
- 大盘指数概览
- 热点板块分析
- 持仓表现
- 选股池推荐
- 明日策略

### 3. 趋势选股

**选股范围：**
- ✅ 主板 (600xxx, 000xxx, 001xxx, 002xxx, 003xxx)
- ✅ 创业板 (300xxx, 301xxx)
- ❌ 科创板 (688xxx) - 排除

**选股策略（右侧交易）：**
1. 趋势向上（均线多头排列）
2. 温和放量（量比 1.2-2.5）
3. 筹码集中（获利比例 30%-80%）
4. MACD 金叉（零轴上方）
5. 板块共振（个股强于板块）
6. 业绩增长（营收、净利润双增）
7. 近期涨停（近 20 日有涨停）
8. 市值适中（50 亿 -500 亿）

**评分系统：**
- >= 80 分 → 强烈推荐 ⭐⭐⭐⭐⭐
- >= 70 分 → 推荐 ⭐⭐⭐⭐
- >= 60 分 → 关注 ⭐⭐⭐
- < 60 分 → 观望

### 4. 事件驱动监控（仅持仓股）

**监控内容：**
- 📊 财报发布（提前 5 天提醒）
- 📢 公司公告（增减持、合同、处罚）
- 📰 新闻舆情（利好/利空）
- 🐉 龙虎榜（机构/游资动向）

**风险等级：**
- 🟢 LOW：无重大利空，正常持仓
- 🟡 MEDIUM：临近财报/小额减持，减仓观望
- 🔴 HIGH：业绩预减/大股东减持，建议减仓
- ⛔ EXTREME：立案调查/财务造假，坚决清仓

---

## 脚本说明

### check_holdings.mjs
持仓检查脚本（每 10 分钟执行）
- 读取持仓配置
- 获取实时行情
- 计算盈亏
- 检测预警

### market_review.mjs
复盘报告生成
- 午盘复盘（12:30）
- 尾盘复盘（15:30）
- 收盘总结（16:00）

### stock_screener.mjs
选股器
- 根据策略筛选股票
- 计算评分
- 返回推荐列表

### alert_checker.mjs
预警检测
- 价格预警
- 涨跌幅预警
- 放量预警
- 公告预警

### announcement_monitor.mjs
公告监控
- 获取最新公告
- 分析公告类型
- 判断利好/利空

### dragon_tiger.mjs
龙虎榜分析
- 获取龙虎榜数据
- 分析机构动向
- 判断资金偏好

### earnings_calendar.mjs
财报日历
- 获取财报发布日期
- 提前提醒
- 业绩预测分析

---

## 配置文件

### holdings.json

```json
{
  "holdings": [
    {
      "code": "股票代码（带后缀）",
      "name": "股票名称",
      "cost": 成本价，
      "shares": 股数，
      "buy_date": "买入日期",
      "notes": "备注",
      "alerts": {
        "target_price": 目标价，
        "stop_loss": 止损价，
        "change_pct": 涨跌幅阈值（百分比）
      }
    }
  ],
  "watchlist": [
    {
      "code": "股票代码",
      "name": "股票名称",
      "reason": "关注理由"
    }
  ],
  "settings": {
    "check_interval_minutes": 10,
    "review_times": ["12:30", "15:30", "16:00"],
    "exclude_st": true,
    "exclude_kcb": true
  }
}
```

---

## 使用示例

### 添加持仓

```
用户："我买了穗恒运 A"
系统："好的，请问您的成本价是多少？持有多少股？"
用户："7.2572 元，700 股"
系统："已记录：穗恒运 A (000531.SZ)，成本 7.2572 元，700 股。开始为您盯盘，每 10 分钟检查一次。"
```

### 查看持仓

```
用户："我的持仓怎么样"
系统：
【持仓概览】
1. 穗恒运 A (000531.SZ)
   现价：7.73 元
   成本：7.2572 元
   盈亏：+330.96 元 (+6.51%)
   今日：+7.06%
   状态：✅ 正常
```

### 选股

```
用户："帮我选股"
系统：
【趋势股推荐】2026-03-24

1. 药明康德 (603259.SH) ⭐⭐⭐⭐⭐
   现价：93.14 元
   今日：+6.09%
   评分：85/100
   理由：放量突破 + 缠论向上段 + 机构净买入

2. 天齐锂业 (002466.SZ) ⭐⭐⭐⭐⭐
   现价：50.43 元
   今日：+2.92%
   评分：82/100
   理由：底部反转 + 筹码集中 + 量能温和
```

### 复盘

```
用户："午盘复盘"
系统：
【午盘复盘】2026-03-24 12:30

📊 大盘概览
上证指数：3849.34 (+0.95%)
深证成指：13380.05 (+0.26%)
创业板指：3209.76 (-0.79%)

🔥 热点板块
1. 金融板块 (+1.5%)
2. 白酒板块 (+0.8%)
3. 新能源板块 (-0.5%)

💰 持仓表现
穗恒运 A：+7.06% ✅ 强势

📌 下午策略
仓位：6-7 成
关注：金融板块持续性
```

---

## 免责声明

⚠️ **本技能提供的分析仅供参考，不构成投资建议。**

- 股市有风险，投资需谨慎
- 历史表现不代表未来
- 请结合个人风险承受能力决策
- 建议设置止损位（如 -8%）
- 避免满仓单只股票
- 本技能不保证数据完全准确，请以交易所官方数据为准

---

## 故障排查

### QVeris API 调用失败

```bash
# 检查 API Key 是否设置
echo $QVERIS_API_KEY

# 检查 QVeris Skill 是否安装
ls ~/.openclaw/skills/qveris-official/SKILL.md

# 测试 QVeris CLI
node ~/.openclaw/skills/qveris-official/scripts/qveris_tool.mjs --help
```

### 持仓配置文件不存在

```bash
# 创建配置文件
mkdir -p ~/.openclaw/workspace/skills/stock-master-pro/stocks
# 然后按照上面的模板创建 holdings.json
```

### 脚本执行失败

```bash
# 检查 Node.js 版本
node -v  # 需要 >= 18.0.0

# 检查脚本权限
chmod +x ~/.openclaw/workspace/skills/stock-master-pro/scripts/*.mjs
```

---

## 更新日志

### v1.0.0 (2026-03-24)
- 初始版本
- 持仓监控（10 分钟检查）
- 午盘/尾盘复盘
- 趋势选股
- 预警系统
- 公告监控
- 龙虎榜分析
- 财报日历
