---
name: product-matching
description: 当用户需要搜索商品、查找相似产品、进行模糊查询或获取商品推荐时触发
version: 1.0.0
tools_required:
  - vector_search
  - semantic_understand
  - collaborative_filter
---

# 商品匹配技能 (Product Matching)

## 触发条件

以下场景自动触发商品匹配技能：
- 用户输入商品名称、品牌、描述性关键词
- 用户上传图片进行以图搜图
- 用户选择"找相似商品"功能
- 用户浏览某商品后点击"相关推荐"
- 冷启动：无历史数据时的新用户推荐

## 执行步骤

### Step 1: 语义解析
```
输入: "找那种带LED灯的瑜伽垫，要防滑的"
处理:
  1. 分词: LED灯 | 瑜伽垫 | 防滑
  2. 实体识别: 产品=瑜伽垫, 特性=LED灯/防滑
  3. 同义词扩展: LED灯→发光/夜光, 防滑→止滑/抓地力
```

### Step 2: 向量检索
```
1. 生成查询向量 Q_embed
2. 在商品向量库中执行近似最近邻(ANN)搜索
3. 召回Top-K候选商品（K=20）
4. 计算余弦相似度得分
```

### Step 3: 协同过滤增强
```
1. 查询该用户的历史浏览/购买数据
2. 找到相似用户的偏好商品
3. 将协同过滤结果与向量检索结果融合
4. 公式: Final_Score = α * Vector_Score + β * CF_Score
   (α=0.7, β=0.3，冷启动时 α=1, β=0)
```

### Step 4: 过滤与排序
```
1. 应用筛选条件（类目/价格/MOQ/地区）
2. 排除已下架/库存不足商品
3. 按综合得分排序
4. 返回Top-10结果
```

### Step 5: 结果组装
```
对每个匹配商品，补全以下信息:
- 商品名称、价格、MOQ
- 供应商名称、评分、响应速度
- 商品图片URL
- 匹配理由说明
```

## 输出格式

### 成功响应
```json
{
  "success": true,
  "skill": "product-matching",
  "data": {
    "query_analysis": {
      "original_query": "LED瑜伽垫防滑",
      "parsed_entities": ["瑜伽垫", "LED灯", "防滑"],
      "intent": "商品搜索"
    },
    "matches": [
      {
        "product_id": "WP2024001234",
        "product_name": "智能LED发光防滑瑜伽垫 8mm加厚",
        "price": {
          "fob_shanghai": 12.50,
          "moq": 50,
          "currency": "USD"
        },
        "supplier": {
          "id": "SUP2024YIWU001",
          "name": "义乌市优品体育用品有限公司",
          "rating": 4.7,
          "response_time": "<2h"
        },
        "match_score": 0.92,
        "match_reasons": ["LED发光功能匹配", "防滑材质匹配", "价格低于市场均价15%"],
        "images": ["https://cdn.example.com/products/women/pants_001.jpg"]
      }
    ],
    "metadata": {
      "total_found": 156,
      "returned_count": 10,
      "search_time_ms": 145,
      "search_method": "hybrid(vector+cf)"
    }
  },
  "confidence": 0.88
}
```

### 无结果响应
```json
{
  "success": true,
  "skill": "product-matching",
  "data": {
    "matches": [],
    "suggestions": [
      {
        "type": "category_broaden",
        "message": "未找到精确匹配，试试这些替代品：",
        "suggestions": ["瑜伽垫", "健身垫", "静音垫"]
      }
    ]
  },
  "confidence": 0.3
}
```

## 异常处理

### 异常1: 查询为空或无效
```
处理:
  1. 返回引导问题: "您好，请问您想找什么商品？"
  2. 提供热门类目入口
  3. 记录为"空查询"用于后续分析
```

### 异常2: 向量服务不可用
```
降级策略:
  1. 切换到关键词全文检索
  2. 使用简化的TF-IDF相似度计算
  3. 在结果中标注"降级模式"
```

### 异常3: 结果置信度低
```
判断: match_score < 0.5
处理:
  1. 扩展搜索范围（模糊匹配）
  2. 询问用户是否接受更多相似商品
  3. 提供"猜你喜欢"兜底推荐
```

## 示例

### 示例1: 描述性查询
```
用户: "有没有那种可以折叠的野餐垫，要防水的，带收纳袋"
系统:
  1. 解析实体: 野餐垫 | 折叠 | 防水 | 收纳袋
  2. 检索匹配商品
  3. 返回3-5款最优匹配，附带匹配理由
```

### 示例2: 模糊查询
```
用户: "那家做收纳盒很好的义乌工厂"
系统:
  1. 识别为"找特定供应商的商品"
  2. 定位供应商后，返回其全品类商品
  3. 标注为"供应商关联推荐"
```

### 示例3: 跨语言查询
```
用户: "I need some Christmas ornaments with LED lights"
系统:
  1. 翻译并解析: 圣诞装饰品 | LED灯
  2. 在中文商品库中检索
  3. 返回结果时保持英文商品名称
```
