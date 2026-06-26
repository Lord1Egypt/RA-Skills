# quant-full-stack

@skill quant-full-stack

## Description

A 股股票量化全流程核心任务体系，覆盖数据采集、因子挖掘、策略构建、回测验证、模拟交易、风险管理 6 大核心模块。

## Tools

- runner.py: 执行量化任务脚本，使用项目虚拟环境 Python

## Tasks

- 01_data_system: 数据体系建设 - 获取沪深 300 成分股、采集日线行情、采集财务数据
- 02_factor_engineering: Alpha 因子挖掘 - 计算价量因子、IC 有效性检验
- 03_strategy_build: 策略构建 - 多因子选股、生成持仓组合
- 04_backtest_verify: 回测验证 - 历史回测、计算收益/回撤/夏普比率
- 05_trade_execution: 模拟交易 - 获取调仓信号、执行模拟调仓
- 06_risk_iteration: 风险管理 - 计算风险指标、生成优化建议

## Entry Point

runner.py

## Requirements

- Python 3.8+
- 项目虚拟环境已配置
- 数据源 API 可用
