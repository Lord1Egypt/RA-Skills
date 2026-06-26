# 杨永兴尾盘选股法

专业的尾盘选股策略实现，基于杨永兴尾盘买入法。

## 快速开始

### 1. 安装依赖

```bash
pip install baostock pandas numpy requests
```

### 2. 准备股票列表

```bash
# 安装 query-main-board-stocks skill
clawhub install query-main-board-stocks

# 生成股票列表
cd skills/query-main-board-stocks
python3 query_main_board_stocks.py
```

### 3. 运行选股

```bash
cd skills/yang-selection
python3 yang_selection.py
```

## 筛选流程

```
步骤 1: 加载市值缓存（跳过 30 天内已查询的低市值股票）
  ↓
步骤 2: 腾讯财经快速初筛（涨幅、换手率、市值）
  ↓
步骤 3: Baostock 深度筛选（量比、均线、成交量趋势）
  ↓
步骤 4: 输出最终结果
```

## 预期结果

- 基础筛选：约 50-100 只股票
- 深度筛选：约 5-20 只股票
- 总耗时：6-8 分钟

## 注意事项

1. 首次运行会创建市值缓存，后续运行速度提升 50%
2. 缓存 30 天后自动更新
3. 需要在交易时段运行（获取实时数据）
