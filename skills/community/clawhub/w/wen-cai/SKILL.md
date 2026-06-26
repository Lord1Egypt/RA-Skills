---
name: wen-cai
description: 同花顺问财全功能合并技能。集成行情数据查询、指数数据查询、财务数据查询、基本资料查询、事件数据查询、公司经营数据查询、机构研究与评级查询、研报搜索、公告搜索、新闻搜索、问财选A股、问财选板块共12个子功能。只需配置 IWENCAI_BASE_URL 和 IWENCAI_API_KEY 两个环境变量，无需任何外部库依赖（仅使用 Python 标准库）。当用户询问以下任意场景时必须使用此技能：股票价格/涨跌幅/成交量/行情数据、指数行情/点位/成分股、财务指标/营收/净利润/ROE/负债率/现金流/毛利率、公司基本信息/上市日期/行业/费率、业绩预告/增发配股/股权质押/限售解禁/机构调研/监管函/重大事件、主营业务/主要客户/供应商/参控股公司/重大合同、研报评级/目标价/机构评级/业绩预测/ESG/券商金股、研究报告搜索/投研决策、公告查询/年报/分红/回购/资产重组、财经新闻/行业动态/政策资讯、A股股票筛选/选股/板块筛选。
---

# wen-cai — 同花顺问财全功能技能

> 将 12 个同花顺问财子技能合并为单一技能，仅依赖 Python 标准库，配置 `IWENCAI_BASE_URL` 和 `IWENCAI_API_KEY` 即可使用。

---

## 环境变量

| 变量名 | 说明 | 示例 |
|--------|------|------|
| `IWENCAI_API_KEY` | 必填，问财 API Key | `sk-proj-xxx` |
| `IWENCAI_BASE_URL` | 可选，默认 `https://openapi.iwencai.com` | `https://openapi.iwencai.com` |

---

## 功能路由表

根据用户意图自动选择接口和 channel：

| 用户意图 | 接口 | channel / 说明 |
|---------|------|---------------|
| 股票行情、涨跌幅、成交量、技术指标、资金流向 | `/v1/query2data` | — |
| 指数行情、点位、涨跌幅 | `/v1/query2data` | — |
| 财务数据、营收、净利润、ROE、负债率、现金流 | `/v1/query2data` | — |
| 基本资料、公司简介、上市日期、行业归属 | `/v1/query2data` | — |
| 事件数据、业绩预告、增发、解禁、质押、调研、监管函 | `/v1/query2data` | — |
| 公司经营、主营业务、客户、供应商、重大合同 | `/v1/query2data` | — |
| 机构评级、目标价、业绩预测、ESG、券商金股 | `/v1/query2data` | — |
| A股选股、股票筛选 | `/v1/query2data` | — |
| 板块筛选、行业板块、概念板块 | `/v1/query2data` | — |
| 研报搜索、研究报告 | `/v1/comprehensive/search` | `channels: ["report"]` |
| 公告搜索、年报、分红、回购公告 | `/v1/comprehensive/search` | `channels: ["announcement"]` |
| 财经新闻、行业动态、政策资讯 | `/v1/comprehensive/search` | `channels: ["news"]` |

---

## 核心处理流程

### 步骤 1：意图识别与接口路由

分析用户查询，按上面路由表选择接口和参数。

### 步骤 2：Query 改写

将口语化表达转为标准金融查询语句，保留核心意图。如需多维度查询（如同时要行情+财务），可拆分为多次调用。

### 步骤 3：API 调用

```python
import urllib.request
import json
import os

BASE_URL = os.environ.get("IWENCAI_BASE_URL", "https://openapi.iwencai.com")
API_KEY  = os.environ["IWENCAI_API_KEY"]

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def call_query2data(query, page="1", limit="10", is_cache="1", expand_index="true"):
    """适用于：行情、指数、财务、基本资料、事件、经营、机构评级、选股、选板块"""
    url = f"{BASE_URL}/v1/query2data"
    payload = {
        "query": query,
        "page": page,
        "limit": limit,
        "is_cache": is_cache,
        "expand_index": expand_index
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    # status_code=0 为成功
    return result

def call_comprehensive_search(query, channel):
    """适用于：研报(report)、公告(announcement)、新闻(news)"""
    url = f"{BASE_URL}/v1/comprehensive/search"
    payload = {
        "channels": [channel],
        "app_id": "AIME_SKILL",
        "query": query
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=HEADERS, method="POST")
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))
```

### 步骤 4：数据解析

**`/v1/query2data` 响应结构：**
```json
{
  "datas": [...],        // 数据列表
  "code_count": 150,     // 符合条件总数
  "chunks_info": {},     // 查询解析信息
  "status_code": 0,      // 0=成功
  "status_msg": ""
}
```

**`/v1/comprehensive/search` 响应结构：**
```json
{
  "data": [
    {
      "title": "文章标题",
      "summary": "摘要",
      "url": "原文链接",
      "publish_date": "2026-04-15 10:00:00"
    }
  ]
}
```

### 步骤 5：空数据重试

若 `datas` 为空，适当放宽条件重试，**最多2次**。

### 步骤 6：分页说明

- 默认 `limit=10`，`page=1`
- 若 `code_count > len(datas)`，说明有更多数据，可通过 `page` 参数翻页
- 选股/选板块场景下，`code_count` 可能很大，按需分页

### 步骤 7：回答用户

- 结果以表格或列表形式呈现，清晰易读
- **必须标注数据来源：同花顺问财**
- 若无数据，引导用户访问 https://www.iwencai.com/unifiedwap/chat

---

## CLI 使用方式

```bash
# 行情查询
python3 scripts/cli.py --type market --query "比亚迪最新价格涨跌幅"

# 财务数据
python3 scripts/cli.py --type finance --query "比亚迪2025年净利润ROE"

# 事件数据
python3 scripts/cli.py --type event --query "比亚迪业绩预告机构调研"

# 机构评级
python3 scripts/cli.py --type rating --query "比亚迪券商评级目标价"

# 研报搜索
python3 scripts/cli.py --type report --query "比亚迪研报投资评级"

# 公告搜索
python3 scripts/cli.py --type announcement --query "比亚迪最新公告"

# 新闻搜索
python3 scripts/cli.py --type news --query "比亚迪最新动态"

# A股选股
python3 scripts/cli.py --type stock-select --query "今日涨幅超5%且成交量放大的A股"

# 板块筛选
python3 scripts/cli.py --type sector-select --query "今日资金净流入最多的板块"

# 翻页
python3 scripts/cli.py --type market --query "沪深300成分股行情" --page 2 --limit 20
```

---

## 子功能速查

| 子功能 | `--type` 参数 | 接口 |
|--------|--------------|------|
| 行情数据查询 | `market` | query2data |
| 指数数据查询 | `index` | query2data |
| 财务数据查询 | `finance` | query2data |
| 基本资料查询 | `basic` | query2data |
| 事件数据查询 | `event` | query2data |
| 公司经营数据 | `business` | query2data |
| 机构研究与评级 | `rating` | query2data |
| 问财选A股 | `stock-select` | query2data |
| 问财选板块 | `sector-select` | query2data |
| 研报搜索 | `report` | comprehensive/search |
| 公告搜索 | `announcement` | comprehensive/search |
| 新闻搜索 | `news` | comprehensive/search |

---

## 错误处理

- `status_code != 0`：显示 `status_msg` 并停止
- 网络超时：友好提示，建议重试
- 无数据：引导用户访问 https://www.iwencai.com/unifiedwap/chat

---

## 数据来源

所有数据均来源于 **同花顺问财**，回答时必须注明来源。
