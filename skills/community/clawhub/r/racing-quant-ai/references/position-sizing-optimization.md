# 策略仓位优化回测框架

> 当用户提出策略优化方案（如调整仓位上限、加减仓规则）时使用此框架。
> 典型触发：用户说"优化策略"、"如果持仓超过N只怎么分仓"、"回测对比方案"。

## 1. 数据准备

### 1.1 拉取完整历史持仓

从 MySQL 策略数据库导出全部历史持仓数据（JSON 格式）：

```javascript
// dump_holdings.js — 导出策略全量历史持仓
const mysql = require('mysql2/promise');
const fs = require('fs');

async function main() {
  const conn = await mysql.createConnection({
    host: '47.121.180.199', port: 3306,
    user: 'display', password: 'display999!',
    database: 'db_strategy'
  });
  // 1. 查 strategy_information 获取 strategy_table 名
  const [rows] = await conn.execute(
    "SELECT strategy_table FROM strategy_information WHERE strategy_id = ?",
    [process.argv[2]]
  );
  const table = rows[0].strategy_table;
  // 2. 拉取全部持仓
  const [holdings] = await conn.execute(
    `SELECT trade_date, trading_info FROM ${table} ORDER BY trade_date ASC`
  );
  const result = holdings.map(r => ({
    date: r.trade_date,
    holdings: typeof r.trading_info === 'string'
      ? JSON.parse(r.trading_info)
      : r.trading_info  // mysql2 自动解析 JSON
  }));
  fs.writeFileSync('/tmp/holdings.json', JSON.stringify(result));
  console.log(`OK ${result.length} days`);
  await conn.end();
}
main();
```

⚠️ `trading_info` 在 mysql2 中返回为 Object 而非 String（见 SKILL.md 陷阱 #6）。

### 1.2 获取 ETF/股票历史价格（东方财富 API）

**必须用 `subprocess.run(['curl', ...])` 而非 `urllib`** — 批量请求时 urllib 大量失败，
curl 带 3 次重试可靠。每个请求间隔 0.15 秒。

```python
import subprocess, json, time

def fetch_prices(code, beg='20230601', end='20260701'):
    cn = code.split('.')[0]
    market = "1" if code.endswith('.SH') else "0"
    url = (f"https://push2his.eastmoney.com/api/qt/stock/kline/get?"
           f"secid={market}.{cn}&fields1=f1,f2,f3&fields2=f51,f52,f53"
           f"&klt=101&fqt=1&beg={beg}&end={end}")
    prices = {}
    for attempt in range(3):
        try:
            result = subprocess.run(
                ['curl', '-s', '--connect-timeout', '10', '--max-time', '15', url],
                capture_output=True, text=True, timeout=20
            )
            if result.stdout and result.stdout.strip():
                data = json.loads(result.stdout)
                klines = data.get('data', {}).get('klines', [])
                for k in klines:
                    parts = k.split(',')
                    if len(parts) >= 3:
                        prices[parts[0]] = float(parts[2])  # date → close
                if prices:
                    break
        except:
            pass
        time.sleep(1)
    return prices
```

fields2 说明：`f51=date, f52=open, f53=close`（还有 f54=high, f55=low, f56=volume）。
`klt=101` = 日线，`fqt=1` = 前复权。

### 1.3 缓存价格数据

价格数据获取耗时较长（66 只 ETF × 3 次重试 ≈ 2 分钟），务必缓存到 JSON 文件供后续复用：

```python
with open('/tmp/etf_prices.json', 'w') as f:
    json.dump(etf_prices, f)
```

## 2. 回测引擎

### 2.1 核心逻辑

```python
def run_backtest(holdings_data, etf_returns, cap_pct, floor_pct=0):
    """
    cap_pct: 单仓上限百分比（0 = 无上限，等权满仓）
    floor_pct: 总仓位下限百分比（0 = 无保底）
    """
    nav = 1.0
    peak = 1.0
    mdd = 0.0
    daily_nav = [1.0]

    for i in range(1, len(holdings_data)):
        holdings = holdings_data[i-1]['holdings']  # 上一日持仓决定今日收益
        date = holdings_data[i]['date']
        n = len(holdings)

        # 获取每只持仓当日收益率
        rets = [etf_returns.get(code, {}).get(date, 0.0) for code in holdings]

        if cap_pct == 0:
            # 原始策略：等权满仓
            weights = [1.0/n] * n
        else:
            cap = cap_pct / 100.0
            floor = floor_pct / 100.0
            raw_w = [min(cap, 1.0/n)] * n
            raw_total = sum(raw_w)
            # 如果总仓位 < 保底，拉到保底（等权放大）
            target_total = max(floor, min(1.0, raw_total))
            if raw_total > 0:
                weights = [w * (target_total / raw_total) for w in raw_w]
            else:
                weights = []

        daily_ret = sum(r * w for r, w in zip(rets, weights))
        nav *= (1 + daily_ret)
        if nav > peak: peak = nav
        dd = (nav - peak) / peak
        if dd < mdd: mdd = dd
        daily_nav.append(nav)

    return nav, mdd, daily_nav
```

### 2.2 指标计算

```python
import math

years = len(holdings_data) / 252
annualized = (nav ** (1/years) - 1) * 100

daily_rets = [daily_nav[i]/daily_nav[i-1]-1 for i in range(1, len(daily_nav))]
mean_ret = sum(daily_rets) / len(daily_rets)
std_ret = math.sqrt(sum((r - mean_ret)**2 for r in daily_rets) / len(daily_rets))
sharpe = (mean_ret / std_ret) * math.sqrt(252) if std_ret > 0 else 0
```

## 3. 仓位优化方案：10% 单仓上限 + 50% 总仓位保底

### 3.1 规则

| 持仓数 N | 每只权重 | 总仓位 | 现金 |
|----------|---------|--------|------|
| N > 10  | 1/N（等权）| 100%   | 0%   |
| 5 < N ≤ 10 | 10%     | N×10%  | (10-N)×10% |
| N ≤ 5   | 50%/N（等权）| 50%    | 50%  |

### 3.2 回测验证结果（stgetf0001，2023.06-2026.06，690 交易日）

| 指标 | 原始策略 | 10%上限无保底 | **10%上限+50%保底** | 10%上限+70%保底 |
|------|---------|-------------|-------------------|---------------|
| 总收益率 | +51.9% | +38.6% | **+53.0%** | +57.3% |
| 最大回撤 | -23.2% | -20.9% | **-16.5%** | -18.3% |
| Sharpe  | 0.88  | 0.91  | **1.10**  | 1.10  |

**最优方案**：10% 单仓上限 + 50% 总仓位保底
- 收益略高于原始（+1.1%）
- 回撤大幅改善（-6.7 个百分点）
- Sharpe 提升 25%
- 熊市减亏 4.6%，牛市不丢收益

### 3.3 为什么 10% 是最佳单仓上限

测过 15%/20%/25%/30% 上限，全部更差：
- 原因：策略熊市持仓收缩到 5-7 只，10% 上限此时正好留 30-50% 现金缓冲
- 15-20% 上限在 N=6-7 时已满仓，等于熊市里完全没有现金保护

### 3.4 为什么需要保底

无保底的 10% 上限在 924 行情中踏空 14.67%（持仓仅 2 只 → 20% 仓位 vs 100% 满仓）。
50% 保底将仓位拉到 50%，吃回一半涨幅，同时仍保留 50% 现金缓冲。

## 4. 分阶段分析框架

回测对比时按市场阶段拆分，避免整体数字掩盖局部问题：

```python
phases = [
    ('熊市', '2023-06', '2023-12'),   # 持仓收缩期
    ('筑底', '2024-01', '2024-08'),   # 低持仓+低波动
    ('反弹', '2024-09', '2024-12'),   # 关键：踏空测试
    ('牛市', '2025-01', '2026-12'),   # 牛市不丢收益测试
]
```

**关键检查点**：反弹阶段（如 924 行情）是否踏空 — 这是仓位优化最容易出问题的地方。

## 5. 生产部署

### 5.1 代码修改位置

> ⚠️ **用户偏好（严格执行）**：仓位调整逻辑必须直接放在**信号生成脚本**中（如 `stgetf0001_huaxia_pool.py`），**绝不在前后端展示层修改**。用户曾要求撤销推送到 fintech 仓库 dev_hermes 分支的所有前后端改动，全部删除后改为只改信号脚本。

修改文件：`strategy_pool/stgetf0001_huaxia_pool.py`（quant-ai-4u 项目）

**原始代码（等权满仓）**：
```python
df_position = pd.DataFrame({'weight': [1/len(stock_pool)]*len(stock_pool)}, index=stock_pool)
```

**优化后代码（分层仓位管理）**：
```python
n = len(stock_pool)
cap_pct = 0.10      # 单仓上限
floor_pct = 0.50     # 总仓位保底
if n * cap_pct >= 1.0:
    weights = [1.0 / n] * n          # N>10: 等权满仓（原始行为）
elif n * cap_pct >= floor_pct:
    weights = [cap_pct] * n           # 5<N≤10: 每只10%
else:
    weights = [floor_pct / n] * n    # N≤5: 总仓50%等权
logging.info(f"仓位管理: N={n}, 单仓={weights[0]:.4f}, 总仓位={sum(weights):.2%}, 现金={1-sum(weights):.2%}")
df_position = pd.DataFrame({'weight': weights}, index=stock_pool)
```

变更量：1 file changed, 15 insertions(+), 1 deletion(-)

### 5.2 Git 部署流程

```bash
cd /tmp/quant-ai-4u
git checkout -b dev_hermes
git add strategy_pool/stgetf0001_huaxia_pool.py
git commit -m "feat(stgetf0001): 仓位优化——10%单仓上限+50%总仓位保底"
git push origin dev_hermes
```

PR 地址：`https://gitee.com/warwickInv/quant-ai-4u/pull/new/warwickInv:dev_hermes...warwickInv:master`

### 5.3 关键注意事项

1. **权重合计不再总是1.0**：当 N≤10 时，`sum(weights) < 1.0`，下游入库和展示链路无需改动（`trading_info` JSON 存储的权重值本身就支持小数）
2. **新增日志输出**：每次调仓时输出仓位管理信息，便于运行时监控：`仓位管理: N=5, 单仓=0.1000, 总仓位=50.00%, 现金=50.00%`
3. **不改变选股逻辑**：信号筛选机制完全不变，只调整仓位分配权重

## 6. 优化完成后工作流

完成仓位优化部署后，用户通常要求生成**总结报告**。报告应包含：
1. 问题发现（回撤现象+根因分析）
2. 优化方向（设计思路+分层规则表）
3. 回测验证（对比指标表+关键发现）
4. 代码实现（修改文件+变更diff+日志输出）
5. 部署状态（git提交+分支+PR地址）
6. 后续优化建议（参数敏感性/动态仓位/止损/行业分散/回测区间扩展）

报告保存到 `/tmp/quant-ai-4u/docs/` 目录下，文件名格式 `{strategy_id}_仓位优化报告.md`。

## 7. 详细报告撰写规范

> ⚠️ **用户偏好（严格执行）**：用户要求"非常详细的记录所有分析内容，不要遗漏任何点"。报告不是概要级，而是完整数据级——每一张表、每一条记录都要呈现。用户曾退回第一版简略报告并要求补充所有遗漏数据点。

### 7.1 报告必须包含的四大部分

用户明确要求以下四个分析阶段，每个都要有完整数据支撑：

1. **📊 策略回撤分析** — 问题发现+持仓变化+根因诊断
2. **📊 策略全周期回测分析：直觉是否正确？** — 原始 vs 简单降仓方案对比
3. **📊 优化方案回测报告：不同单仓上限对比** — 多种cap参数网格搜索
4. **📊 方案D深度回测报告：单仓上限+总仓位保底** — cap+floor组合寻优

### 7.2 必须包含的分析维度

| 维度 | 内容 | 说明 |
|------|------|------|
| 持仓数量"市场温度计" | 月度平均持仓数ASCII柱状图 | 用█字符绘制，直观展示持仓数随市场周期变化 |
| 月度持仓统计明细 | 月份/平均持仓/最小/最大/交易日数 | 37个月完整表格，附阶段特征标注 |
| 分阶段持仓集中度分析 | 7阶段划分，含N≤2/N≤5/N=1占比 | 按市场周期分段（熊市下跌/极端收缩/底部蛰伏/924觉醒/牛市扩张/牛市爆发/稳健高位） |
| N=1单票满仓连续记录 | 起止日期/连续天数/持仓ETF代码 | 所有连续≥2天的N=1记录，标注最极端的streak |
| 关键事件逐日持仓详情 | 如924行情期间每日持仓 | 日期/持仓数N/持仓ETF/单仓权重，展示策略在大涨前夜的状态 |
| 高频持仓ETF分析 | ETF代码/出现天数/占比 | Top 20 ETF频率表 |
| 全周期持仓数量分布 | N=1/2/3-5/6-10/11-15/16+ | 含N≤5占比、N≤10占比统计 |
| 月度收益逐月对比 | 37个月原始vs优化逐月对比 | 每月：持仓数N/现金占比/原始收益/优化收益/差异 |
| 分阶段收益对比 | 4阶段（熊市/筑底/反弹/牛市） | 原始vs优化vs各方案 |

### 7.3 "市场温度计"ASCII可视化模板

```
2023.06 ████████████████████ 9只（启动即山顶）
2023.07 ██████ 4只（急缩）
...
2024.08 ██ 1只（最低点！）
─────────── 924行情分界线 ───────────
2024.10 ████████████████ 8只（猛醒！）
...
2025.09 ██████████████████████████████████████████████████ 20只
```

绘制规则：
- 每月一行，█数量≈月度平均持仓数
- 标注关键转折点（山顶/急缩/最低点/猛醒/巅峰）
- 用`─────────── 分界线 ───────────`分隔重大市场事件（如924行情）

### 7.4 回测数据获取方法

持仓数据已缓存在 `/tmp/holdings_stgetf0001.json`（从MySQL策略数据库导出）。
价格数据已缓存在 `/tmp/etf_prices.json`（东财API获取，66只ETF×690交易日）。
回测脚本在 `/tmp/backtest_option_d2.py`（方案D深度回测，7组cap+floor组合）。

重新运行回测获取完整输出：
```python
# 在 execute_code 中直接运行缓存脚本
import json, math
with open('/tmp/holdings_stgetf0001.json') as f: hd = json.load(f)
with open('/tmp/etf_prices.json') as f: ep = json.load(f)
# ... 运行 run_backtest(cap, floor) 获取各方案指标
# ... 运行月度/分阶段对比获取详细数据
```

### 7.5 飞书文档上传

报告完成后，用户通常要求"整理成一个飞书文档"。使用 `feishu-docs` 技能的 `md_to_feishu_blocks.py` 脚本：

```python
import sys
sys.path.insert(0, '/home/ubuntu/.hermes/skills/productivity/feishu-docs/scripts')
from md_to_feishu_blocks import convert_and_upload, get_credentials_from_env

app_id, app_secret = get_credentials_from_env()
convert_and_upload('/tmp/stgetf0001_report.md', doc_id, app_id, app_secret)
```

典型规模：174个block，35批次×5块/批次，上传约23秒。
表格在飞书中以代码块（block_type 14）呈现，因飞书Table API不稳定（见 feishu-docs 技能说明）。
