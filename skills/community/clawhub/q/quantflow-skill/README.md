# QuantFlow Skill

面向中文自然语言的量化金融数据研究技能。

## 简介

QuantFlow Skill 是一个基于 Akshare 和 AKQuant 的量化金融数据研究技能，能够将自然语言的财经数据请求转换成可执行的数据获取、清洗、对比、筛选、导出与简要分析流程。

## 功能特性

### 数据获取
- A股、指数、ETF/基金历史行情
- 公司财务数据、估值指标
- 资金流向、北向资金、龙虎榜
- 板块概念、行业轮动
- 公告新闻、研报政策
- 宏观经济数据（CPI、PMI、社融等）

### 量化策略回测
基于 AKQuant 量化投研引擎，支持多种量化策略：
- 双均线策略(期货)
- Alpha对冲(股票+期货)
- 集合竞价选股(股票)
- 多因子选股(股票)
- 网格交易(期货)
- 指数增强(股票)
- 跨品种套利(期货)
- 跨期套利(期货)
- 日内回转交易(股票)
- 做市商交易(期货)
- 海龟交易法(期货)
- 行业轮动(股票)
- 机器学习(股票)

## 安装依赖

```bash
pip install akshare
pip install akquant
```

## 使用示例

### 查看股票走势
```
看看宁德时代最近三个月走势
```

### 财务分析
```
看下比亚迪最近 8 个季度营收和净利润趋势
```

### 量化策略回测
```
用 AKQuant 回测一个简单的趋势策略
```

## Skill 结构

```
quantflow-skill/
├── SKILL.md              # Skill 主文件
├── scripts/              # 脚本目录
│   ├── akquant_strategies.py       # 量化策略实现
│   ├── akquant_strategy_demo.py    # 策略演示
│   ├── stock_data_demo.py         # 股票数据示例
│   ├── fund_data_demo.py          # 基金数据示例
│   ├── macro_data_demo.py         # 宏观数据示例
│   └── other_data_demo.py        # 其他数据示例
└── evals/               # 测试用例
    └── evals.json
```

## 版本

当前版本：1.0.0

## 作者

yejinlei

## 许可证

MIT License
