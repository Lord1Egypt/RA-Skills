---
name: fb-hotel-aggregation-skill
description: 酒店聚合助手，整合分贝通、携程、美团、同程、华住会、锦江等多个酒店数据源，提供统一的酒店搜索、房型查询、预订服务。Invoke when user wants to search hotels across multiple platforms or aggregate hotel data from various sources.
version: 1.0.0
metadata: {"openclaw": {"emoji": "🏨", "category": "travel", "tags": ["酒店聚合", "多平台", "统一搜索", "数据整合"], "requires": {"bins": ["python3"]}, "required": true}}
---
# 酒店聚合助手 (fb-hotel-aggregation-skill)

## 技能描述

酒店聚合助手，整合多个酒店数据源（分贝通、携程、美团、同程、华住会、锦江等），提供统一的酒店搜索、房型查询、价格对比、预订服务。通过数据标准化和智能聚合，为用户提供更全面、更优惠的酒店选择。

---

⚠️ 【重要约束】
- 必须调用各平台API获取真实数据
- 禁止自行编造酒店信息、价格或库存
- 数据聚合时需标明数据来源
- 接口返回什么数据就展示什么，不要修改

---

## 技能概述

基于多数据源聚合技术，实现：
- 多平台酒店数据统一搜索
- 数据标准化和去重合并
- 智能排序和推荐
- 统一预订流程

## 技能能力

### 核心能力

1. **多源数据聚合**：整合分贝通、携程、美团、同程、华住会、锦江等平台
2. **统一搜索**：一次搜索，返回所有平台的酒店结果
3. **智能去重**：相同酒店多平台数据合并展示
4. **最优价格**：自动筛选各平台最低价格
5. **统一预订**：支持选择任意平台进行预订

### 触发条件

1. **聚合搜索**：当用户搜索酒店时，同时查询多个平台
   - 返回聚合后的酒店列表
   - 显示各平台价格对比
   - 标注最优价格来源

2. **展示格式示例**：
   ```
   🏨 北京三元桥附近酒店聚合结果（3月15日入住）
   
   | 序号 | 酒店名称 | 星级 | 区域 | 最优价格 | 价格来源 |
   |:---:|---------|:---:|------|---:|:---|
   | 1 | 桔子酒店(北京三元桥店) | 舒适型 | 朝阳区 | ¥483 | 携程 |
   | 2 | 魔方公寓（北京三元桥店） | 经济型 | 朝阳区 | ¥333 | 美团 |
   
   💡 回复"序号"查看房型详情
   💡 回复"序号-比价"查看该酒店各平台价格对比
   ```

## 数据源配置

### 支持的数据源

| 数据源 | 标识 | 类型 | 特点 |
|:---|:---|:---|:---|
| 分贝通 | fenbeitong | B2B | 企业协议价、商旅管理 |
| 携程 | ctrip | OTA | 库存丰富、价格优势 |
| 美团 | meituan | OTA | 本地生活、优惠券多 |
| 同程 | tongcheng | OTA | 微信生态、返现活动 |
| 华住会 | huazhu | 集团直联 | 会员权益、积分价值高 |
| 锦江 | jinjiang | 集团直联 | 会员折扣、品牌多 |

## 核心接口列表

### 一、聚合搜索接口

| 接口名称 | 核心用途 | 必选参数 |
|---------|---------|---------|
| aggregate_search | 多平台酒店聚合搜索 | city, check_in, check_out, keywords |
| get_hotel_detail_aggregate | 聚合酒店详情 | hotel_id, source |
| get_room_prices_aggregate | 聚合房型价格 | hotel_id, check_in, check_out |

### 二、数据管理接口

| 接口名称 | 核心用途 | 说明 |
|---------|---------|------|
| sync_hotel_data | 同步酒店基础数据 | 从各平台同步酒店信息 |
| merge_duplicate_hotels | 合并重复酒店 | 基于名称、地址匹配去重 |
| refresh_prices | 刷新价格数据 | 实时更新各平台价格 |

## 数据模型

### 统一酒店模型

```json
{
  "hotel_id": "聚合ID",
  "name": "酒店名称",
  "name_en": "英文名称",
  "address": "地址",
  "city": "城市",
  "district": "区域",
  "star_level": "星级",
  "score": "评分",
  "images": ["图片URL"],
  "facilities": ["设施"],
  "sources": [
    {
      "platform": "平台标识",
      "external_id": "平台酒店ID",
      "price": "价格",
      "url": "预订链接"
    }
  ]
}
```

### 统一房型模型

```json
{
  "room_id": "房型ID",
  "name": "房型名称",
  "bed_type": "床型",
  "area": "面积",
  "floor": "楼层",
  "capacity": "入住人数",
  "facilities": ["房间设施"],
  "sources": [
    {
      "platform": "平台标识",
      "external_id": "平台房型ID",
      "price": "价格",
      "breakfast": "早餐",
      "cancel_policy": "取消政策"
    }
  ]
}
```

## 聚合算法

### 去重策略

1. **名称匹配**：模糊匹配酒店名称相似度 > 85%
2. **地址匹配**：地址相似度 > 80%
3. **坐标匹配**：距离 < 500米
4. **人工审核**：疑似重复标记待审核

### 排序策略

1. **综合评分**：价格 40% + 评分 30% + 距离 20% + 设施 10%
2. **价格优先**：最低价格优先
3. **评分优先**：最高评分优先
4. **距离优先**：最近距离优先

## 响应规则

### 成功响应

```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "total": 100,
    "page": 1,
    "page_size": 10,
    "hotels": [
      {
        "hotel_id": "AGG_123456",
        "name": "桔子酒店(北京三元桥店)",
        "star_level": "舒适型",
        "score": 4.7,
        "address": "朝阳区三元桥...",
        "best_price": 483,
        "best_source": "携程",
        "sources_count": 3,
        "sources": ["携程", "美团", "分贝通"]
      }
    ],
    "sources_status": {
      "携程": "success",
      "美团": "success",
      "分贝通": "timeout"
    }
  }
}
```

### 失败响应

```json
{
  "code": 500,
  "msg": "错误信息",
  "data": null
}
```
