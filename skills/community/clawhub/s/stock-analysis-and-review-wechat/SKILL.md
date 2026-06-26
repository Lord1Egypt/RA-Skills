---
name: stock-analysis-and-review-wechat
version: 2.0.0
description: 股票分析与自我复盘工具（适配微信插件），用于A股/港股/美股的收盘复盘、持仓盘点、建仓评估和消息面梳理。支持实时数据获取（腾讯财经/新浪财经接口）、持仓盈亏计算、技术分析、定时任务集成和微信推送。适用于个人投资者进行每日盘后分析和投资决策辅助。
changelog: |
  v2.0.0 (2026-04-17)
  - 新增：Cron任务delivery配置错误的详细解决方案（坑5）
  - 新增：微信消息格式适配最佳实践（坑7）
  - 新增：定时任务健康检查机制（坑8）
  - 新增：定时任务管理最佳实践章节
  - 优化：微信格式示例，使用树形结构替代表格
---

# 股市复盘分析工具 📊

专业的股市复盘分析框架，帮助投资者系统性地进行每日盘后总结和投资决策。

## 🎯 适用场景

1. **每日收盘复盘** - 盘后自动/手动执行持仓盘点
2. **建仓时机评估** - 判断标的是否触发建仓/加仓条件
3. **消息面梳理** - 整合国际/国内财经新闻对持仓的影响
4. **定时监控任务** - 设置盘中预警和收盘复盘定时器

## 📋 复盘流程

### 标准复盘五步法

```
Step 1: 大盘概览 → 获取指数数据、成交额、涨跌分布
Step 2: 持仓盘点 → 计算各标的盈亏、收益率、预警状态
Step 3: 建仓评估 → 评估备选标的建仓条件
Step 4: 消息面 → 梳理国内外财经新闻影响
Step 5: 策略建议 → 给出明日操作计划和风险提示
```

## 🔧 工具使用技巧

### 1. 数据获取（腾讯财经接口）

**推荐接口**（稳定、无需认证、实时）：
```bash
# 腾讯财经实时行情接口
curl -s "https://qt.gtimg.cn/q=sh600919,sz159819,sh510310"
```

**返回格式解析**：
```
v_sh600919="1~江苏银行~600919~10.78~...";
# 字段顺序: 0=未知,1=名称,2=代码,3=当前价,4=昨收,5=今开...
```

**ETF代码前缀规则**：
- A股ETF: `sh` (上海) / `sz` (深圳)
- 港股: `hk` (如 hk00700 腾讯)
- 美股: 直接使用代码 (如 AAPL)

### 2. 数据解析技巧

**关键字段索引**（腾讯财经）：
| 索引 | 含义 | 示例 |
|------|------|------|
| 1 | 股票名称 | 江苏银行 |
| 2 | 股票代码 | 600919 |
| 3 | 当前价格 | 10.78 |
| 4 | 昨日收盘 | 10.70 |
| 5 | 今日开盘 | 10.72 |
| 33 | 今日最高 | 10.85 |
| 34 | 今日最低 | 10.65 |
| 38 | 市盈率 | 5.23 |

**解析示例**（Python）：
```python
import requests

def get_stock_data(codes):
    """获取股票实时数据"""
    url = f"https://qt.gtimg.cn/q={','.join(codes)}"
    resp = requests.get(url, timeout=10)
    data = {}
    for line in resp.text.strip().split(';'):
        if not line.strip():
            continue
        parts = line.split('="')
        if len(parts) == 2:
            code = parts[0].replace('v_', '')
            fields = parts[1].rstrip('"').split('~')
            data[code] = {
                'name': fields[1],
                'price': float(fields[3]),
                'prev_close': float(fields[4]),
                'change_pct': round((float(fields[3]) - float(fields[4])) / float(fields[4]) * 100, 2)
            }
    return data
```

### 3. 盈亏计算

**持仓盈亏公式**：
```
持仓盈亏 = (当前价 - 成本价) × 持仓数量
收益率 = (当前价 - 成本价) / 成本价 × 100%
```

**市值计算**（ETF注意单位）：
```python
# ETF份额 vs 股票股数
total_value = sum(position['quantity'] * position['current_price'] for position in portfolio)
```

### 4. 定时任务集成

**OpenClaw定时任务格式**：
```bash
openclaw cron add \
  --name stock-daily-review \
  --cron "5 15 * * 1-5" \
  --agent main \
  --message "执行股市收盘复盘：1) 获取大盘数据 2) 盘点持仓 3) 评估建仓标的 4) 更新MEMORY.md" \
  --description "工作日收盘后自动复盘"
```

**推荐监控时间点**：
- 早盘: 9:30 / 10:30 / 11:30
- 午盘: 13:00 / 14:00 / 14:30 / 15:00
- 收盘复盘: 15:05

## ⚠️ 常见坑与解决方案

### 坑1: 数据源不稳定

**问题**: 新浪财经接口偶尔返回空数据或格式变化

**解决**: 
- 使用腾讯财经作为主要数据源（`qt.gtimg.cn`）
- 实现双数据源备份机制
- 添加超时和重试逻辑

### 坑2: ETF代码前缀混淆

**问题**: ETF代码有时需要`sh`/`sz`前缀，有时不需要

**解决**:
- A股ETF统一加前缀: `sh510310` / `sz159819`
- 港股加`hk`: `hk00700`
- 美股不加前缀: `AAPL`
- 建立代码映射表

### 坑3: 数据解析失败

**问题**: API返回格式变化导致解析失败

**解决**:
```python
# 健壮的解析代码
try:
    fields = line.split('="')[1].rstrip('"').split('~')
    price = float(fields[3]) if fields[3] else 0.0
except (IndexError, ValueError) as e:
    print(f"解析失败: {line}, 错误: {e}")
    continue
```

### 坑4: 定时任务消息推送失败

**问题**: 使用复杂delivery payload导致消息发送失败

**解决**:
- 简化payload结构
- 避免使用可疑的delivery参数
- 使用message工具直发作为兜底

### 坑5: Cron任务 delivery 配置错误（致命！）

**问题**: 定时任务创建时 `--accountId` 和 `--to` 参数被错误地拼接到 `--message` 中，导致消息无法发送

**错误示例**:
```bash
# ❌ 错误 - accountId和to被当作message内容
openclaw cron add \
  --message "执行任务...,accountId:xxx,to:xxx"  # 这会导致 delivery 缺失！
```

**正确做法**:
```bash
# ✅ 正确 - 使用 announce + last 模式，自动推送到最后活跃通道
openclaw cron add \
  --name stock-monitor-am \
  --cron "0 10,11 * * 1-5" \
  --agent main \
  --message "执行股票监控任务" \
  --description "早盘监控"
# delivery 默认: {mode: "announce", channel: "last"}
```

**排查方法**:
1. 检查任务状态: `openclaw cron list` (状态为 error 表示有问题)
2. 查看日志: `grep "Action send requires a target" /tmp/openclaw/openclaw-*.log`
3. 错误日志出现时间对应任务执行时间，确认是 delivery 问题

**修复步骤**:
```bash
# 1. 删除旧任务
openclaw cron remove stock-monitor-am
openclaw cron remove stock-monitor-pm

# 2. 重新创建（使用正确格式）
openclaw cron add --name stock-monitor-am --cron "0 10,11 * * 1-5" \
  --agent main --message "执行早盘监控" --description "早盘监控 10:00/11:00"
```

**经验**: 不要手动指定 delivery 的 accountId 和 to，使用 `announce` + `last` 模式让系统自动推送到当前对话

### 坑6: 持仓数量与金额混淆

**问题**: 记录时混淆"份数"和"金额"

**解决**:
- ETF用"份数"，股票用"股数"
- 记录格式: `数量|成本价|当前价`
- 明确区分建仓金额和持仓数量

### 坑7: 微信消息格式适配问题

**问题**: Markdown表格在微信手机端显示混乱，需要频繁左右滑动

**解决**: 转换为树形文本格式
- ❌ 避免：7列表格，横向信息过载
- ✅ 推荐：竖排展示，每个标的三行信息

**对比示例**:
```markdown
# ❌ 表格格式（手机端体验差）
| 标的 | 数量 | 成本 | 现价 | 盈亏 | 收益率 | 状态 |
|------|------|------|------|------|--------|------|
| 电池ETF | 15200 | 0.946 | 1.055 | +1656 | +11.5% | 盈利 |

# ✅ 树形格式（手机端友好）
**💼 持仓概览**

🔋 **电池ETF** | 15,200份 | **+11.5%** (+¥1,656)
├─ 成本: ¥0.946 → 现价: ¥1.055
└─ 今日: +2.54% 📈
```

**格式转换原则**:
1. 关键数字前置（盈亏、收益率放第一行）
2. 使用树形符号 `├─ └─` 增强层次感
3. 控制每行长度（不超过20个汉字）
4. 用emoji替代文字状态标记

### 坑8: 定时任务健康检查缺失

**问题**: 任务状态变为 error 后无法及时发现，导致多天收不到监控消息

**解决**: 建立定期检查机制

**检查清单**（每周执行一次）:
```bash
# 1. 检查任务状态
openclaw cron list

# 2. 确认状态为 idle（不是 error/running）
# 3. 检查错误日志
grep "Action send requires a target" /tmp/openclaw/openclaw-*.log
```

**建议**: 将检查命令写入 HEARTBEAT.md，利用 OpenClaw 的 heartbeat 机制定期提醒检查

### 坑9: 时区和交易时间判断

**问题**: 非交易日仍触发监控任务

**解决**:
```python
import datetime

def is_trading_day():
    """判断是否为交易日"""
    today = datetime.datetime.now()
    # 周末休市
    if today.weekday() >= 5:
        return False
    # 可扩展：调用交易日历API
    return True
```

## ⏰ 定时任务管理最佳实践

### 创建任务的标准流程

```bash
# 1. 先列出当前任务，确认没有重复
openclaw cron list

# 2. 删除旧任务（如果有）
openclaw cron remove stock-monitor-am

# 3. 创建新任务（简洁格式）
openclaw cron add \
  --name stock-monitor-am \
  --cron "0 10,11 * * 1-5" \
  --agent main \
  --message "执行早盘股票监控：检查持仓实时行情和建仓条件" \
  --description "早盘监控 10:00/11:00"
```

### 验证任务配置

创建后必须验证：

```bash
# 检查任务列表
openclaw cron list

# 确认以下字段：
# - Status: idle (不是 error)
# - Next: 显示正确的下次执行时间
# - Schedule: 与预期一致
```

### 常见问题排查

**任务状态为 `error`**:
```bash
# 查看日志定位问题
grep "cron\|error\|Action send requires" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log

# 常见错误：
# - "Action send requires a target" → delivery 配置错误
# - "timeout" → 任务执行超时
```

**消息未收到但任务状态正常**:
1. 检查 Gateway 是否运行: `openclaw gateway status`
2. 检查微信插件状态
3. 手动触发测试: `openclaw cron trigger stock-monitor-am`

### 推荐监控时间表

| 任务 | 时间 | 说明 |
|------|------|------|
| stock-monitor-am | 10:00, 11:00 | 早盘监控 |
| stock-monitor-pm | 13:00, 14:00, 15:00 | 午盘监控 |
| stock-daily-review | 15:10 | 收盘深度复盘 |

**注意**: 避免设置 9:30，因为 Gateway 启动可能未完成

---

## 📊 分析框架

### 1. 大盘分析模板

```markdown
**A股大盘表现**
- 上证指数: {sh_index}点 ({change_pct}%)
- 深证成指: {sz_index}点 ({change_pct}%)
- 创业板指: {cy_index}点 ({change_pct}%)
- 两市成交额: {volume}亿元
- 涨跌分布: 上涨{up_count}家 / 下跌{down_count}家
```

### 2. 持仓状态表

**Markdown表格格式（适合PC/文档查看）**：
```markdown
| 标的 | 持仓数量 | 成本价 | 最新价 | 持仓盈亏 | 收益率 | 状态 |
|------|---------|--------|--------|---------|--------|------|
| {name} | {qty} | ¥{cost} | ¥{price} | {pnl} | {return}% | {status} |
```

**微信适配格式（推荐手机查看）**：
```markdown
**💼 持仓概览**

🎯 **电池ETF** | 15,200份 | **+11.1%** (+¥1,594)
├─ 成本: ¥0.946 → 现价: ¥1.051
└─ 今日: +2.54% 📈

📈 **沪深300ETF** | 4,400份 | **+3.6%** (+¥704)
├─ 成本: ¥4.40 → 现价: ¥4.56
└─ 今日: +1.22% ✅

🏦 **江苏银行** | 700股 | **+20.2%** (+¥1,278)
├─ 成本: ¥8.99 → 现价: ¥10.82
└─ 距止盈¥11.50还差6.3%

**📊 汇总**: 市值¥64,213 | 总盈亏+¥4,685 (+7.87%)
```

**微信格式优化要点**：
1. **减少列数**：将7列表格压缩为3-4行文本
2. **竖排展示**：每个标的独立成块，避免横向滑动
3. **关键信息前置**：收益率和盈亏金额放第一行
4. **使用树形符号**：├─ └─ 让层次更清晰
5. **控制行长度**：每行不超过20个汉字，确保不换行显示

**状态标记**：
- 🎯 盈利丰厚（>15%）
- 📈 盈利持有（>0%）
- 🔄 基本平盘（-3%~0%）
- 🟡 接近预警（-5%~-3%）
- 🔴 需要关注（<-5%）

### 3. 建仓评估框架

| 标的 | 当前价 | 建仓线 | 触发条件 | 建议 |
|------|--------|--------|----------|------|
| {name} | ¥{price} | ¥{line} | 跌3%以上 | 首次建仓500元 |

### 4. 消息面分析维度

1. **地缘政治** - 战争、冲突、外交事件
2. **宏观经济** - GDP、通胀、利率、就业
3. **行业政策** - 监管变化、产业政策
4. **公司事件** - 财报、并购、管理层变动
5. **全球市场** - 美股、欧股、大宗商品

## 💡 策略建议模板

### 现有持仓建议
- **止盈标的**: 涨至目标价，建议减仓/清仓
- **持有标的**: 趋势良好，继续持有
- **关注标的**: 接近预警线，密切关注

### 建仓/加仓计划
- **明日建仓**: 标的名称、建仓金额、触发条件
- **加仓计划**: 标的名称、加仓金额、触发价位

### 风险提示
- 市场系统性风险
- 行业特定风险
- 个股风险
- 流动性风险

## 📝 MEMORY.md更新规范

每次复盘后更新以下章节：

1. **当前持仓状态表** - 最新数据
2. **交易记录** - 新增交易
3. **关键监控点位** - 调整止盈止损线
4. **状态机** - 更新进行中的事项

## 📱 微信推送集成

复盘报告可通过微信推送给用户。使用微信推送时请注意：

### 前置检查
1. **检查微信插件版本**: 执行前确认 `openclaw-weixin` 插件版本 >= 1.0.x
2. **提醒更新**: 版本过低时提醒用户更新 `pnpm update -g openclaw`

### 推送方式
**Delivery推送（推荐用于定时任务）**:
```yaml
delivery:
  mode: announce
  channel: openclaw-weixin
  to: "{user_id}@im.wechat"    # 必填
  accountId: "{account_id}"     # 必填
```

**Message工具推送（用于临时推送）**:
```json
{
  "action": "send",
  "channel": "openclaw-weixin",
  "to": "user_id@im.wechat",
  "message": "复盘报告内容..."
}
```

### 格式适配
- 微信不支持Markdown表格，转换为列表格式
- 使用微信支持的emoji（📈 📉 🎯）
- 单条消息控制在2000字以内

详细指南参见 [wechat_push.md](references/wechat_push.md)

## 🔗 相关资源

- [腾讯财经API](https://qt.gtimg.cn/)
- [新浪财经API](https://hq.sinajs.cn/)
- [东方财富](https://www.eastmoney.com/)
- [OpenClaw定时任务](https://docs.openclaw.ai/cron)

---

*提醒：本工具仅供学习交流，不构成投资建议。投资有风险，入市需谨慎。*
