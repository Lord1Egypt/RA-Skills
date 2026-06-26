# 快速开始指南

## 第一次使用

### 1. 测试单只股票采集

```bash
# 测试采集贵州茅台（A股）
cd skills/stock-data-collector
python3 scripts/fetch_stock.py --code 600519 --market A
```

### 2. 测试批量采集

```bash
# 使用示例列表文件
python3 scripts/batch_fetch.py --file scripts/example_list.txt
```

## 常见使用场景

### 场景1: 采集我的自选股

创建 `my_stocks.txt`：
```
600519,A,贵州茅台
000001,A,平安银行
00700,HK,腾讯控股
```

然后运行：
```bash
python3 scripts/batch_fetch.py --file my_stocks.txt
```

### 场景2: 快速采集几只股票

```bash
python3 scripts/batch_fetch.py --codes 600519,00700 --markets A,HK --names 贵州茅台,腾讯控股
```

### 场景3: 采集不同周期

```bash
# 周线数据
python3 scripts/fetch_stock.py --code 600519 --market A --period weekly

# 月线数据
python3 scripts/fetch_stock.py --code 600519 --market A --period monthly
```

## 输出位置

默认输出到当前目录下的 `stock_data/` 文件夹。

## 获取帮助

```bash
# 单只股票采集帮助
python3 scripts/fetch_stock.py --help

# 批量采集帮助
python3 scripts/batch_fetch.py --help
```
