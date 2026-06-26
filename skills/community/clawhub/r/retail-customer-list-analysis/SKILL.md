---
name: retail-customer-list-analysis
description: |
  客户清单分析工具。基于Shop API客户清单数据，快速查询不同类型客户的数量、试用情况汇总、导购匹配情况。
  
  核心能力：
  1. 客户类型分布统计（普通/潜在/意向/成交客户数量及占比）
  2. 客户试用情况汇总（感兴趣商品数、试用商品数、试用后成交转化）
  3. 导购匹配分析（各导购关联客户数、匹配失败数量及原因）
  4. 客户明细列表查询（支持分页、筛选、导出）
  
  数据源：POST /api/v1/customer/list
  
  使用场景：
  - 晨会/周会快速查询客户情况
  - 实时监控客户类型分布
  - 导购客户分配检查
  - 匹配失败客户处理
  
  触发条件：
  - 用户查询客户清单（如"今天有多少意向客户"）
  - 用户统计客户类型（如"各类型客户占比多少"）
  - 用户检查导购匹配（如"有多少客户匹配失败"）
  - 用户查看客户试用情况（如"客户试用情况如何"）
---

# 客户清单分析 Skill

## 技能名称
`customer-list-analysis`

## 版本
v1.0

## 功能描述
基于 Shop API 客户清单数据，快速查询不同类型客户的数量、试用情况汇总、导购匹配情况。

## 数据源

### API 端点
```
POST /api/v1/customer/list
```

### 请求参数
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| storeId | string | 是 | 门店ID |
| fromDate | string | 是 | 开始时间 (YYYY-MM-DD HH:mm:ss) |
| toDate | string | 是 | 结束时间 (YYYY-MM-DD HH:mm:ss) |
| customerType | array | 否 | 客户类型 [1,2,3,4]，空数组=全部 |
| badgeName | string | 否 | 导购姓名，为空查询全部 |
| pageNo | int | 否 | 页码，默认1 |
| pageSize | int | 否 | 每页数量，默认20 |

### 客户类型
| 类型值 | 名称 | 说明 |
|--------|------|------|
| 1 | 普通客户 | 进店浏览但未产生试用行为 |
| 2 | 潜在客户 | 有普通试用行为 |
| 3 | 意向客户 | 有深度试用但未成交 |
| 4 | 成交客户 | 已完成购买 |

### 返回字段
| 字段 | 说明 |
|------|------|
| customerId | 客户ID |
| visitId | 访问ID |
| customerType | 客户类型 (1-4) |
| fromTime | 进店时间 |
| toTime | 离店时间 |
| duration | 停留时长（秒） |
| interestedItems | 感兴趣商品数 |
| trialItems | 试用商品数 |
| trialTransTotal | 试用后成交件数 |
| transMoney | 成交金额 |
| transTotal | 成交件数 |
| badgeName | 关联导购姓名（为空表示匹配失败） |

## 核心能力

### 1. 客户类型分布统计
```
总客户数: XXX人
├── 普通客户: XX人 (XX%) - 进店未试用
├── 潜在客户: XX人 (XX%) - 有普通试用
├── 意向客户: XX人 (XX%) - 深度试用未成交
└── 成交客户: XX人 (XX%) - 已完成购买
```

### 2. 客户试用情况汇总
按客户类型汇总：
- 平均感兴趣商品数
- 平均试用商品数
- 试用后成交转化率
- 平均成交金额

### 3. 导购匹配分析
```
总客户数: XXX人
├── 已匹配导购: XX人 (XX%)
│   ├── 导购A: XX人
│   ├── 导购B: XX人
│   └── ...
└── 匹配失败: XX人 (XX%) - 需处理
```

### 4. 客户明细列表
支持分页查询，可导出客户明细。

## 使用示例

```python
from analyze import analyze_customer_list

# 查询今日客户清单
result = analyze_customer_list(
    store_id="416759_1714379448487",
    from_date="2026-03-25 00:00:00",
    to_date="2026-03-25 23:59:59",
    customer_type=[],  # 全部客户
    badge_name=None    # 全部导购
)

# 查询特定导购的客户
result = analyze_customer_list(
    store_id="416759_1714379448487",
    from_date="2026-03-25 00:00:00",
    to_date="2026-03-25 23:59:59",
    customer_type=[3, 4],  # 意向+成交
    badge_name="杨丽"
)
```

## 输出格式

```json
{
  "status": "ok",
  "store_id": "416759_1714379448487",
  "query_period": {
    "from": "2026-03-25 00:00:00",
    "to": "2026-03-25 23:59:59"
  },
  "summary": {
    "total_customers": 50,
    "by_type": {
      "普通客户": {"count": 10, "percentage": 20.0},
      "潜在客户": {"count": 15, "percentage": 30.0},
      "意向客户": {"count": 15, "percentage": 30.0},
      "成交客户": {"count": 10, "percentage": 20.0}
    },
    "by_badge": {
      "matched": {"count": 45, "percentage": 90.0},
      "unmatched": {"count": 5, "percentage": 10.0},
      "clerks": {
        "杨丽": {"count": 20, "types": {"意向": 10, "成交": 10}},
        "李翠": {"count": 15, "types": {"潜在": 8, "意向": 7}},
        "未匹配": {"count": 5, "types": {"普通": 3, "潜在": 2}}
      }
    }
  },
  "trial_summary": {
    "平均感兴趣商品数": 3.5,
    "平均试用商品数": 2.1,
    "试用后成交转化率": 35.0
  },
  "customer_list": [...],
  "page": {
    "total": 50,
    "size": 20,
    "pages": 3,
    "current": 1
  }
}
```

## 依赖
- `api_client.get_shop_data()` - Shop API 调用
- `~/.openclaw/workspace-front-door/` - API 客户端路径

## 版本
v1.0.0 - 客户清单查询、类型分布、试用汇总、导购匹配
