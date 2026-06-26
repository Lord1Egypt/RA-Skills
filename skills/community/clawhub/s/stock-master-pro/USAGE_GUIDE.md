# Stock Master Pro 使用指南

## 📊 数据策略优化

### 交易时段（9:30-11:30, 13:00-15:00）
- ✅ **每 10 分钟**调用一次 QVeris API
- ✅ **每 10 秒**从本地 JSON 读取数据（不消耗 API 额度）
- ✅ 实时刷新 Dashboard

### 收盘后（15:00-次日 9:30）
- ❌ **停止调用** QVeris API（节省额度）
- ✅ 只读取本地 JSON（展示已有数据）
- ✅ 公告监控继续（重要信息）

### 周末/节假日
- ❌ 停止调用 QVeris API
- ✅ 只读模式展示数据

---

## 🚀 Dashboard 访问

### 方式 1：直接打开
```
file:///home/yaoha/.openclaw/workspace/skills/stock-master-pro/web/index.html
```

### 方式 2：本地服务器
```bash
# 启动
~/.openclaw/workspace/skills/stock-master-pro/start-web.sh

# 访问
http://localhost:3000
```

---

## 📁 数据文件说明

### 核心数据文件

| 文件 | 说明 | 更新频率 |
|------|------|----------|
| `stocks/dashboard_data.json` | Dashboard 主数据 | 每 10 分钟 |
| `stocks/last_check.json` | 持仓检查数据 | 每 10 分钟 |
| `stocks/holdings.json` | 持仓配置 | 手动配置 |

### 功能数据文件

| 文件 | 说明 | 更新频率 |
|------|------|----------|
| `stocks/reviews/*.md` | 复盘报告 | 午盘/尾盘/收盘 |
| `stocks/announcements.json` | 公告数据 | 每日 |
| `stocks/dragon_tiger.json` | 龙虎榜数据 | 每日收盘后 |
| `stocks/earnings_calendar.json` | 财报日历 | 每周 |
| `stocks/screener_results.json` | 选股结果 | 按需 |

---

## 🔧 脚本说明

### 核心脚本

| 脚本 | 功能 | 执行时机 |
|------|------|----------|
| `aggregate_data.mjs` | 数据聚合 | 每 10 分钟（交易时段） |
| `check_holdings.mjs` | 持仓检查 | 每 10 分钟 |
| `generate_demo_data.mjs` | 生成演示数据 | 首次使用 |

### 功能脚本

| 脚本 | 功能 | 执行时机 |
|------|------|----------|
| `market_review.mjs` | 生成复盘报告 | 午盘 12:30/尾盘 15:30/收盘 16:00 |
| `announcement_monitor.mjs` | 公告监控 | 每日 |
| `dragon_tiger.mjs` | 龙虎榜分析 | 每日收盘后 |
| `earnings_calendar.mjs` | 财报日历 | 每周 |
| `stock_screener.mjs` | 趋势选股 | 按需 |

---

## ⏰ 定时任务配置

### Crontab 配置示例

```bash
crontab -e
```

添加以下内容：

```bash
# 交易时段每 10 分钟检查持仓（工作日 9:30-15:00）
*/10 9-15 * * 1-5 export QVERIS_API_KEY="sk-xxx" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/check_holdings.mjs

# 交易时段每 10 分钟聚合数据
*/10 9-15 * * 1-5 export QVERIS_API_KEY="sk-xxx" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/aggregate_data.mjs

# 午盘复盘（12:30）
30 12 * * 1-5 export QVERIS_API_KEY="sk-xxx" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/market_review.mjs noon

# 尾盘复盘（15:30）
30 15 * * 1-5 export QVERIS_API_KEY="sk-xxx" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/market_review.mjs afternoon

# 收盘总结（16:00）
0 16 * * 1-5 export QVERIS_API_KEY="sk-xxx" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/market_review.mjs close

# 公告监控（每日 17:00）
0 17 * * 1-5 export QVERIS_API_KEY="sk-xxx" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/announcement_monitor.mjs

# 龙虎榜（每日收盘后 17:30）
30 17 * * 1-5 export QVERIS_API_KEY="sk-xxx" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/dragon_tiger.mjs

# 财报日历（每周一 9:00）
0 9 * * 1 export QVERIS_API_KEY="sk-xxx" && node ~/.openclaw/workspace/skills/stock-master-pro/scripts/earnings_calendar.mjs
```

---

## 💡 使用场景

### 场景 1：日常盯盘

**Dashboard 自动刷新**
- 打开 Dashboard
- 每 10 秒自动更新数据
- 预警信息即时显示

**对话触发**
```
你："我的持仓怎么样"
→ 显示实时盈亏和预警
```

### 场景 2：午盘复盘

**自动运行**
- 12:30 自动运行复盘脚本
- 生成复盘报告

**查看报告**
- Dashboard 点击"午盘复盘"按钮
- 或对话："午盘复盘"

### 场景 3：收盘总结

**自动运行**
- 16:00 自动运行复盘脚本
- 生成龙虎榜数据
- 更新公告数据

**查看报告**
- Dashboard 点击"收盘总结"按钮
- 或对话："今日复盘"

### 场景 4：选股分析

**运行选股**
```bash
node ~/.openclaw/workspace/skills/stock-master-pro/scripts/stock_screener.mjs
```

**查看结果**
- Dashboard 查看选股结果（待实现）
- 或对话："帮我选股"

---

## 📊 Dashboard 模块

### 已实现模块

| 模块 | 状态 | 说明 |
|------|------|------|
| 大盘概览 | ✅ 完成 | 四大指数 + K 线图 |
| 持仓监控 | ✅ 完成 | 盈亏计算 + 预警 |
| 复盘报告 | ✅ 完成 | 午盘/尾盘/收盘 |
| 实时预警 | ✅ 完成 | 闪烁提示 |

### 待实现模块

| 模块 | 状态 | 说明 |
|------|------|------|
| 公告监控 | 📁 数据已生成 | Dashboard 展示 |
| 龙虎榜 | 📁 数据已生成 | Dashboard 展示 |
| 财报日历 | 📁 数据已生成 | Dashboard 展示 |
| 选股池 | 📁 数据已生成 | Dashboard 展示 |

---

## ⚠️ 注意事项

### 1. API 额度节省

**收盘后自动停止调用**
- `aggregate_data.mjs` 会检测是否收盘
- 收盘后读取本地缓存，不调用 API
- 每日可节省大量 API 调用

### 2. 数据更新

**确保定时任务运行**
- 检查 crontab 配置
- 查看日志确认执行
- 故障时手动运行脚本

### 3. Dashboard 缓存

**浏览器缓存问题**
- Dashboard 会自动添加时间戳参数
- 如果数据不更新，强制刷新（Ctrl+F5）

---

## 🎯 快速上手

### 第一步：配置持仓

编辑 `stocks/holdings.json`：

```json
{
  "holdings": [
    {
      "code": "000531.SZ",
      "name": "穗恒运 A",
      "cost": 7.2572,
      "shares": 700
    }
  ]
}
```

### 第二步：生成演示数据

```bash
node ~/.openclaw/workspace/skills/stock-master-pro/scripts/generate_demo_data.mjs
```

### 第三步：启动 Dashboard

```bash
~/.openclaw/workspace/skills/stock-master-pro/start-web.sh
```

### 第四步：访问 Dashboard

浏览器打开：
```
http://localhost:3000
```

---

## 📝 总结

### 数据策略
- ✅ 交易时段：每 10 分钟调用 API + 每 10 秒读取本地
- ✅ 收盘后：只读本地（节省额度）
- ✅ 公告监控：持续进行（重要信息）

### Dashboard 功能
- ✅ 大盘概览（实时指数 + K 线图）
- ✅ 持仓监控（盈亏 + 预警）
- ✅ 复盘报告（午盘/尾盘/收盘）
- ✅ 实时预警（闪烁提示）
- 📁 公告/龙虎榜/财报/选股（数据已生成，待 Dashboard 展示）

### 下一步
1. 完善 Dashboard 其他模块展示
2. 配置定时任务
3. 日常使用

---

**Stock Master Pro v1.0.0** | 2026-03-24
