# 🎉 Stock Master Pro 技能创建完成！

## ✅ 已完成

### 技能文件结构

```
~/.openclaw/workspace/skills/stock-master-pro/
├── SKILL.md                          # 技能说明文档（9.3 KB）
├── README.md                         # 使用指南（4.2 KB）
├── SETUP.md                          # 安装指南（4.3 KB）
├── _meta.json                        # 技能元数据
├── scripts/
│   ├── check_dependency.mjs          # 依赖检查脚本
│   ├── check_holdings.mjs            # 持仓检查脚本（10 分钟）
│   └── stock_screener.mjs            # 选股器脚本
├── references/                       # 参考资料目录（待填充）
└── stocks/
    └── holdings.example.json         # 持仓配置模板
```

### 核心功能

| 功能 | 状态 | 说明 |
|------|------|------|
| 依赖检查 | ✅ 完成 | 检查 QVeris AI 安装和 API Key |
| 持仓监控 | ✅ 完成 | 10 分钟自动检查，盈亏计算 |
| 预警系统 | ✅ 完成 | 目标价、止损、涨跌幅、放量 |
| 趋势选股 | ✅ 完成 | 右侧交易策略，智能评分 |
| 配置文件 | ✅ 完成 | holdings.json 模板 |

### 待实现功能（脚本框架已创建）

| 功能 | 状态 | 说明 |
|------|------|------|
| 午盘复盘 | ⏸️ 待实现 | 12:30 自动生成复盘报告 |
| 尾盘复盘 | ⏸️ 待实现 | 15:30 自动生成复盘报告 |
| 公告监控 | ⏸️ 待实现 | 监控持仓股公告 |
| 龙虎榜分析 | ⏸️ 待实现 | 分析机构动向 |
| 财报日历 | ⏸️ 待实现 | 财报发布提醒 |

---

## 🚀 立即开始使用

### 步骤 1：设置 API Key

```bash
# 临时设置（当前会话）
export QVERIS_API_KEY="sk-Gc4yItJDkM3vBSJhnNPM_Ri4d1F6mar1YxdzK8RxOZI"

# 或永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export QVERIS_API_KEY="sk-Gc4yItJDkM3vBSJhnNPM_Ri4d1F6mar1YxdzK8RxOZI"' >> ~/.bashrc
source ~/.bashrc
```

### 步骤 2：检查依赖

```bash
node ~/.openclaw/workspace/skills/stock-master-pro/scripts/check_dependency.mjs
```

应该显示：
```
✅ QVeris AI 依赖已就绪
✨ 所有依赖已就绪，可以开始使用 Stock Master Pro！
```

### 步骤 3：配置持仓

```bash
# 复制配置模板
cp ~/.openclaw/workspace/skills/stock-master-pro/stocks/holdings.example.json \
   ~/.openclaw/workspace/skills/stock-master-pro/stocks/holdings.json

# 编辑持仓配置（已包含穗恒运 A 示例）
nano ~/.openclaw/workspace/skills/stock-master-pro/stocks/holdings.json
```

### 步骤 4：开始盯盘

```bash
# 检查持仓
node ~/.openclaw/workspace/skills/stock-master-pro/scripts/check_holdings.mjs

# 选股
node ~/.openclaw/workspace/skills/stock-master-pro/scripts/stock_screener.mjs
```

---

## 📋 配置文件说明

### holdings.json

```json
{
  "holdings": [
    {
      "code": "000531.SZ",        // 股票代码（必须带后缀）
      "name": "穗恒运 A",          // 股票名称
      "cost": 7.2572,             // 成本价
      "shares": 700,              // 股数
      "buy_date": "2026-03-20",   // 买入日期
      "notes": "趋势票，电力概念", // 备注
      "alerts": {
        "target_price": 8.20,     // 目标价
        "stop_loss": 7.00,        // 止损价
        "change_pct": 5           // 涨跌幅预警阈值（%）
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
    "check_interval_minutes": 10,  // 检查间隔（分钟）
    "review_times": ["12:30", "15:30", "16:00"],  // 复盘时间
    "exclude_st": true,            // 排除 ST 股票
    "exclude_kcb": true            // 排除科创板
  }
}
```

---

## 🎯 选股策略

### 评分系统（满分 100 分）

| 维度 | 分值 | 条件 |
|------|------|------|
| 趋势向上 | 25 分 | 均线多头排列，股价在 60 日线上方 |
| 温和放量 | 20 分 | 量比 1.2-2.5 |
| 筹码集中 | 15 分 | 获利比例 30%-80% |
| MACD 金叉 | 15 分 | DIF > DEA，红柱放大 |
| 板块共振 | 5 分 | 个股强于板块 |
| 业绩增长 | 10 分 | 营收、净利润双增 |
| 市值适中 | 5 分 | 50 亿 -500 亿 |
| 非科创板 | 5 分 | 排除 688 开头 |

### 评级标准

- ⭐⭐⭐⭐⭐ 80+ 分：强烈推荐
- ⭐⭐⭐⭐ 70-79 分：推荐
- ⭐⭐⭐ 60-69 分：关注
- < 60 分：观望

---

## ⚠️ 预警类型

| 类型 | 触发条件 | 等级 | 示例 |
|------|----------|------|------|
| 目标价 | 现价 >= 目标价 | ℹ️ 提示 | 🎯 达到目标价 8.20 元 |
| 止损价 | 现价 <= 止损价 | 🚨 紧急 | ⚠️ 触及止损价 7.00 元 |
| 涨跌幅 | 绝对值 >= 阈值 | ⚠️ 警告 | 📈 涨跌幅 +7.06% |
| 放量 | 量比 >= 3 | ⚠️ 警告 | 🔥 放量！量比 3.50 |

---

## 📝 下一步

### 1. 测试现有功能

```bash
# 检查持仓
node ~/.openclaw/workspace/skills/stock-master-pro/scripts/check_holdings.mjs

# 选股
node ~/.openclaw/workspace/skills/stock-master-pro/scripts/stock_screener.mjs
```

### 2. 完善复盘功能

需要创建：
- `scripts/market_review.mjs` - 午盘/尾盘复盘
- `scripts/announcement_monitor.mjs` - 公告监控
- `scripts/dragon_tiger.mjs` - 龙虎榜分析
- `scripts/earnings_calendar.mjs` - 财报日历

### 3. 设置定时任务

```bash
# 编辑 crontab
crontab -e

# 添加（交易时段每 10 分钟检查）
*/10 * 9-15 * * 1-5 export QVERIS_API_KEY="sk-xxx" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/check_holdings.mjs
```

---

## 📚 文档

- **SKILL.md** - 技能完整说明
- **README.md** - 快速开始指南
- **SETUP.md** - 详细安装步骤

---

## 🎉 创建者

Stock Master Pro v1.0.0
创建时间：2026-03-24

---

## ⚠️ 免责声明

本技能提供的分析仅供参考，不构成投资建议。
股市有风险，投资需谨慎。
