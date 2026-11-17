---
name: quant-trading-free-datafeed-replacement
description: 量化交易系统免费数据源替换方法论，替换付费数据源，保持接口完全兼容
category: quant-trading
tags: [datafeed, akshare, baostock, yfinance, tqsdk]
author: peterliu-512
license: MIT-0
---

# 量化交易系统免费数据源替换方法论

## 改造目标
彻底摆脱付费数据源依赖（如 TickDB），只重写数据获取层，保持对外接口完全兼容，实现全免费多市场行情支持。

## 改造原则
1. **严格范围限定**：只修改数据获取模块，不改动策略引擎、下单逻辑、风控、Flask接口等其他模块
2. **接口完全兼容**：函数名、入参、返回字段结构完全不变，上层零改动适配
3. **多数据源自动降级**：主源超时自动切备用源，保证可用性
4. **全市场覆盖**：A股、港股、美股、国内期货、国际黄金（XAUUSD/沪金/COMEX黄金）

## 依赖清单
```
flask
pandas
akshare
baostock
yfinance
tqsdk
websockets
```

## 架构设计
```
data/
├── __init__.py
├── data_provider.py      # 主入口，对外兼容原接口
├── providers/
│   ├── __init__.py
│   ├── akshare_provider.py   # AKShare 兜底
│   ├── baostock_provider.py  # Baostock A股历史K线+复权
│   ├── yfinance_provider.py  # Yahoo Finance 港美股补充
│   ├── tqsdk_provider.py     # TqSdk 期货专业数据
│   └── common_utils.py       # 公共工具（缓存、符号转换）
└── health_check.py       # 数据源健康检查
```

## 数据源优先级
1. **实时价格**：AKShare → TqSdk(期货) → yfinance(美股)
2. **历史K线**：Baostock(A股) → AKShare → yfinance
3. **黄金**：AKShare → yfinance
4. **期货**：TqSdk → AKShare

## 关键实现细节
### 符号标准化转换
- `.SH`/`.SZ` 保持不变（A股）
- `.HK` 保持不变（港股）  
- 美股保持原代码（无后缀）
- 沪金：`AU.SHF` → 转换为 `SHFE.AU`
- XAUUSD：`XAUUSD` -> 直接用 AKShare 接口

### 统一内存缓存
- 实时价格缓存 TTL: 30秒
- K线数据缓存 TTL: 5分钟
- 避免重复请求，降低被限流概率

### 健康检查
- 每个数据源维护健康状态
- 连续失败N次自动降级
- 定期重试恢复

## 验收标准
1. 原有调用代码无需任何修改即可运行
2. 所有市场数据可正常获取
3. 主源失败自动降级到备用源
4. 不影响策略、风控、下单任何原有功能
