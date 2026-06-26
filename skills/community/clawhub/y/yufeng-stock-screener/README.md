# 禹锋量化 · A股量化选股助手

## 技能简介

本技能调用「禹锋量化」云端引擎，基于四维评分体系自动筛选 A 股短线机会。

## 功能

- **screen** - 今日选股 TOP5
- **analyze** - 个股深度分析（需 --code）
- **sector** - 热门板块资金流向
- **timing** - 个股择时评分（需 --code）
- **status** - 查询 Token 状态

## 安装

1. 解压后将文件夹放入 `~/.workbuddy/skills/`
2. 安装依赖：`pip install requests`

## 使用

```bash
python3 ~/.workbuddy/skills/a-stock-quant-screener/scripts/query_stocks.py \
  --action screen --token YOUR_TOKEN
```

## Token 获取

访问：http://124.220.59.85:8080 或联系作者购买