---
name: wyckoff-screen
version: 1.2.0
description: Wyckoff 2.0 选股系统。全市场扫描，找出处于"积累末期"或"趋势启动"阶段的A股候选股。当用户要求"选股"、"扫市场"、"今日买什么"、"帮我看看有什么可以买的"、"全市场扫描"时触发。输出按评分排序的候选股名单和工作流程说明。
---

# Wyckoff 选股系统

## 工作流程

```
第一步：拉取全市场股票列表
  → akshare stock_info_a_code_name() 获取所有A股代码（约5500只）

第二步：更新日线数据（可选，force=True时全量更新）
  → efinance stock.get_quote_history(code, klt=101, fqt=1)
  → 存 SQLite 本地数据库（stock_daily表）

第三步：逐只分析（评分模型）
  → wyckoff_engine.score_stock() → 计算 Phase + VPOC + 综合评分
  → 筛选条件：评分 ≥ 60 且 Phase/VPOC 方向为积累/突破

第四步：输出结果
  → 按评分降序，输出TOP20候选股名单
  → 每只包含：代码、名称、Phase、VPOC、现价、关键信号、评分
```

## 核心脚本

- `scripts/screen.py` — 选股主脚本，执行全流程
- `scripts/wyckoff_engine.py` — 核心算法（Phase检测 + VP计算 + 评分）

## 评分模型（score_stock）

**Phase 评级逻辑：**
- Phase E 上涨趋势 + 价格在VPOC上方 → ✅ 加分
- Phase B accumulation + 价格在VPOC上方 → ✅ 加分（最佳候选）
- Phase C spring_test + 价格收回VPOC → ✅ 加分（待确认）
- Phase D breakout_up → ✅ 加分（强势）
- Phase B distribution / Phase C upthrust_test → 🔴 扣分（派发，不买）
- Phase E 下跌趋势 → 🔴 扣分（坚决回避）
- 价格在VPOC下方 → 🔴 扣分（重心偏弱）

**评级档位：**
- S（≥75分）：强烈推荐
- A（60~74分）：满足买入条件
- B（40~59分）：观察
- C/D（<40分）：不建议/回避

## 双模式筛选

系统支持**两种交易风格**，通过 `--mode` 参数切换：

### `--mode right`（默认）→ 右侧趋势筛选
**逻辑：** 等趋势确认了才买，核心是"突破跟进"

- Phase E 上涨趋势 + 价格在 VPOC 上方 → ✅
- Phase D 向上突破 → ✅
- Phase C Spring 测试后价格**收回** VPOC → ✅（待确认）
- 价格在 VPOC 下方 → 🔴 回避
- Phase B 派发 / Phase E 下跌 → 🔴 坚决回避

评分阈值：≥60分出结果，S级≥75

### `--mode left` → 左侧积累筛选
**逻辑：** 主力在悄悄收集、价格还在低位，提前埋伏等拉升

- Phase B 积累区间 + 价格在区间低位 → ✅（最佳候选）
- Phase C Spring 测试支撑有效 → ✅
- 价格紧贴 LVN 支撑 → ✅（最佳买点）
- 价格在 VAL/VPOC **下方** → ✅（低位吸筹区，不是缺点）
- 缩量止跌（5日均量 < 20日均量）→ ✅（主力在吸筹）
- Phase E 下跌趋势 → 🔴 不抄底
- 放量下跌 → 🔴 主力在派发

评分阈值：≥55分出结果，S级≥75

### `--mode both` → 两种都跑

---

## 调用方式

```python
# 直接运行（输出到屏幕）
python scripts/screen.py

# 作为模块调用
import sys
sys.path.insert(0, 'scripts')
from screen import screen, init_db, update_daily_data, format_result

conn = init_db()
update_daily_data(conn)
result = screen(conn)
print(format_result(result))
```

## 数据依赖

- **efinance**：东方财富数据（pip install efinance）
- **akshare**：股票列表（pip install akshare）
- **scipy**：Volume Profile 计算（pip install scipy）

## 评分阈值

默认输出评分 ≥ 60 的股票，按评分降序排列，最多输出TOP20。
评分阈值可在 `screen()` 函数中修改 `score >= 60` 条件。

## 限制说明

- 本系统基于日线数据，适合中短线选股
- 不提供实时行情，数据收盘后更新
- Order Flow ，因A股缺乏真实订单流数据，本系统不包含
