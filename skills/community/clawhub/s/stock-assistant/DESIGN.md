# 炒股助手 - 设计方案

## 1. 项目概述

**名称**：炒股助手
**定位**：A股交易辅助工具，集行情查询、交易记录管理、盈亏分析于一体
**代码目录**：`<YOUR_PATH>`

## 2. 技术栈

- **语言**：Python 3.x
- **存储**：SQLite（轻量级，无需配置）
- **接口**：腾讯财经（免费，无需认证）

## 3. 目录结构

```
<YOUR_PATH>/
├── main.py              # CLI 入口
├── fetcher.py           # 行情获取（A股）
├── trader.py            # 交易逻辑
├── db.py                # 数据库操作
├── models.py            # 数据模型
├── exporter.py          # 导出功能
├── requirements.txt     # 依赖
└── data/                # 数据目录
    └── trades.db        # SQLite数据库
```

## 4. 功能设计

### 4.1 行情查询
```bash
# 查询股票行情
python main.py quote 600016
python main.py quote 000001
```

**返回数据**：当前价、涨跌额、涨跌幅、今开、昨收、最高、最低、成交量、成交额、换手率、市盈率、市净率等

### 4.2 交易记录管理
```bash
# 导入CSV
python main.py import trades.csv

# 手动添加交易
python main.py add --code 600016 --name 民生银行 --type buy --quantity 1700 --price 3.90

# 查看持仓
python main.py positions

# 查看指定股票盈亏
python main.py pnl 600016 --current-price 4.15

# 导出记录
python main.py export --format csv
```

### 4.3 费率推算
根据交易记录反推佣金率、印花税率、过户费

## 5. 数据模型

### 交易记录表 (trades)
| 字段 | 类型 | 说明 |
|-----|------|-----|
| id | INTEGER | 主键 |
| trade_date | TEXT | 交易日期 |
| trade_time | TEXT | 交易时间 |
| code | TEXT | 股票代码 |
| name | TEXT | 股票名称 |
| direction | TEXT | 买入/卖出 |
| quantity | INTEGER | 成交数量 |
| price | REAL | 成交均价 |
| amount | REAL | 成交金额 |
| commission | REAL | 佣金 |
| fee | REAL | 其他费用 |
| stamp_tax | REAL | 印花税 |
| transfer_fee | REAL | 过户费 |
| created_at | TEXT | 记录时间 |

### 持仓表 (positions)
| 字段 | 类型 | 说明 |
|-----|------|-----|
| code | TEXT | 股票代码 |
| name | TEXT | 股票名称 |
| quantity | INTEGER | 持仓数量 |
| avg_cost | REAL | 平均成本 |
| total_cost | REAL | 总成本 |

## 6. 开发计划

### Phase 1: 基础功能
- [x] 行情查询（A股）
- [x] CSV导入
- [x] SQLite存储
- [x] 持仓计算
- [x] 盈亏计算

### Phase 2: 增强
- [ ] 费率自动推算
- [ ] 批量查询多只股票
- [ ] 统计报表

### Phase 3: 智能化
- [ ] 股价提醒
- [ ] 持仓预警
