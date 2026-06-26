---
name: travel-planner
description: "智能旅行规划助手 - 支持行程规划、预算管理、景点推荐、交通查询、酒店比价、 packing清单生成。Use when: (1) 用户需要规划旅行行程或 vacation, (2) 需要推荐目的地或景点, (3) 需要计算旅行预算, (4) 需要查询交通路线/航班/火车, (5) 需要生成 packing 清单, (6) 需要比较酒店价格或寻找住宿"
---

# Travel Planner

智能旅行规划全能工具集，基于 Python + 多数据源 API 实现。

## 核心能力

### 1. 行程规划
- 多目的地行程路线优化
- 每日行程自动生成（考虑交通时间、景点开放时间）
- 兴趣标签匹配（历史/自然/美食/购物/冒险）
- 旅行时长智能建议

### 2. 预算管理
- 分项预算模板（交通/住宿/餐饮/门票/购物）
- 实时汇率转换
- 预算与实际花费对比
- 多人分摊计算

### 3. 景点推荐
- 基于位置和兴趣的景点推荐
- 热门景点 + 小众 hidden gems
- 景点评分、开放时间、门票价格
- 路线距离与时间估算

### 4. 交通查询
- 航班查询与比价
- 火车/高铁时刻查询
- 公交/地铁路线规划
- 租车比价

### 5. 酒店比价
- 多平台价格比较
- 按区域/价格/评分筛选
- 酒店设施标签筛选

### 6. Packing 清单
- 基于目的地气候的衣物建议
- 活动类型装备清单（徒步/潜水/滑雪）
- 证件/电子设备/药品 checklist
- 多人出行清单合并

## 快速开始

```bash
# 生成完整行程
python3 scripts/plan_trip.py --destination "东京" --days 5 --interests "美食,购物,历史" --output trip_plan.json

# 预算计算
python3 scripts/budget_calculator.py --destination "巴黎" --days 7 --travelers 2 --output budget.json

# 景点推荐
python3 scripts/recommend_attractions.py --city "京都" --interests "寺庙,自然" --output attractions.json

# 生成 packing 清单
python3 scripts/packing_list.py --destination "冰岛" --days 10 --activities "徒步,观鲸,温泉" --output packing.json

# 汇率转换
python3 scripts/currency_converter.py --amount 1000 --from USD --to CNY
```

## 依赖安装

```bash
pip install -r requirements.txt
```

核心依赖：requests, geopy, python-dateutil, jinja2, pandas, openpyxl

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `plan_trip.py` | 完整行程规划生成 |
| `budget_calculator.py` | 旅行预算计算与管理 |
| `recommend_attractions.py` | 景点推荐引擎 |
| `transport_query.py` | 交通查询（航班/火车/公交） |
| `hotel_search.py` | 酒店搜索与比价 |
| `packing_list.py` | 智能 packing 清单生成 |
| `currency_converter.py` | 实时汇率转换 |
| `weather_forecast.py` | 目的地天气预报 |
| `itinerary_exporter.py` | 行程导出（PDF/Excel/日历） |
| `trip_share.py` | 行程分享与协作 |

## 详细用法

参见 `references/` 目录：
- `destinations-database.md` - 热门目的地数据库
- `budget-templates.md` - 预算模板参考
- `api-reference.md` - 脚本 API 参考
