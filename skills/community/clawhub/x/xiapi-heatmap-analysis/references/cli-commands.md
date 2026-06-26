# CLI 命令参考

## 基本命令

### 获取行业板块热力图

```bash
daxiapi sector heatmap
```

**返回数据**：
- 近5个交易日各行业 CS 值（含 ↑↓ 方向）
- 近5个交易日各行业当日涨跌幅（含 ↑↓ 方向）
- 近5个交易日各行业5日涨跌幅（含 ↑↓ 方向）
- 预处理分类数据：cs_gt_5_names、cs_gt_ma20_names、cs_crossover_ma20_names 等

### 获取热门概念板块

```bash
daxiapi sector gn
```

**返回数据**：
- 概念板块名称
- 涨跌幅
- 领涨股

### 获取各板块领涨股

```bash
daxiapi sector top
```

**返回数据**：
- 板块名称
- 领涨股票代码
- 领涨股票名称
- 涨跌幅

## 配置命令

### 设置 Token

```bash
daxiapi config set token YOUR_TOKEN
```

### 查看 Token 配置

```bash
daxiapi config get token
```

## 使用示例

```bash
# 获取热力图（含历史序列和预处理分类数据）
daxiapi sector heatmap

# 获取概念板块
daxiapi sector gn

# 获取领涨股（用于验证板块行情广度）
daxiapi sector top
```
