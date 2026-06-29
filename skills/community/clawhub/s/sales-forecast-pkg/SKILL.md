---
name: sales-forecast
description: AI销量预测助手。基于 Amazon Chronos-2 (120M) 零样本时序大模型，输入历史销量数据（CSV/Excel），自动生成多分位数概率预测、置信区间和交互式HTML可视化报告。当用户询问销量预测、销售预测、趋势预测、时序预测时使用。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env: []
    emoji: "📈"
    homepage: https://github.com/bettermen/sales-forecast
---

# Sales Forecast - Chronos-2 销量预测

基于 Amazon Chronos-2 零样本时序大模型（120M 参数），零训练、开箱即用的销量预测工具。

## 功能

- 零样本概率预测：无需训练，直接对历史销量数据推理
- 多分位数输出：默认 10%/50%/90% 分位数，自带置信区间
- 自动数据校验：智能检测列名、推断时间频率、处理缺失值
- 交互式报告：Plotly 生成 HTML 可视化报告，含趋势图和逐期明细
- 多格式输入：CSV、Excel (.xlsx/.xls)、JSON、Parquet

## 输入数据格式

CSV 文件至少包含两列：日期和时间序列数值。

```csv
timestamp,sales
2024-01-01,245
2024-01-02,238
2024-01-03,252
```

## 使用方法

```bash
# 安装依赖
pip install chronos-forecasting pandas plotly openpyxl

# 运行预测（预测未来 30 期）
python3 {baseDir}/scripts/forecast.py \
  --input sales.csv \
  --output results/ \
  --prediction-length 30 \
  --quantiles 0.1,0.5,0.9

# 生成 HTML 报告
python3 {baseDir}/scripts/report_gen.py \
  --data results/forecast_data.json \
  --output report.html
```

## 命令行参数

### forecast.py

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-i, --input` | 输入数据文件路径 | 必填 |
| `-o, --output` | 输出目录 | 必填 |
| `-p, --prediction-length` | 预测步数 | 30 |
| `-q, --quantiles` | 分位数（逗号分隔） | 0.1,0.5,0.9 |
| `-c, --context-length` | 最大上下文长度 | 2048 |
| `--hf-endpoint` | HuggingFace 镜像地址 | hf-mirror.com |

### report_gen.py

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-d, --data` | forecast_data.json 路径 | 必填 |
| `-o, --output` | 输出 HTML 文件路径 | 必填 |

## 模型信息

- 模型：amazon/chronos-2
- 参数量：120M
- 上下文长度：默认 2048
- 支持 CPU/GPU 推理
- 论文：Chronos-2: From Univariate to Universal Forecasting

## 注意事项

- 首次运行会下载模型（~500MB），国内建议设置 `HF_ENDPOINT=https://hf-mirror.com`
- 建议最少 30 个历史数据点
- CPU 推理约 10-30 秒/序列
- 所有发布到 ClawHub 的技能使用 MIT-0 许可
