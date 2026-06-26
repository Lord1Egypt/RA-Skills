# 商品匹配示例库 (Product Matching Examples)

## 场景1: 功能型商品搜索

### 用户输入
```
"找一款可以在水上使用的充气游泳圈，要有遮阳伞和安全绳"
```

### 系统处理过程
```json
{
  "step1_entity_extraction": {
    "core_product": "充气游泳圈",
    "features": ["水上使用", "遮阳伞", "安全绳"],
    "safety_requirement": "安全绳"
  },
  "step2_vector_search": {
    "query_embedding": [0.12, -0.34, 0.67, ...],
    "top_k": 20,
    "recall_rate": 0.85
  },
  "step3_filtering": {
    "applied_filters": ["户外水上用品", "价格区间$5-$20"],
    "excluded": ["小尺寸儿童款"]
  },
  "step4_ranking": {
    "final_matches": 8,
    "top_match_score": 0.91
  }
}
```

### 输出结果
```json
{
  "matches": [
    {
      "product_id": "POOL20240089",
      "product_name": "大型成人充气游泳圈 带遮阳伞 安全手柄 直径120cm",
      "price": {"fob_yiwu": 8.50, "moq": 100, "currency": "USD"},
      "supplier": {
        "name": "义乌市海洋户外用品厂",
        "rating": 4.6,
        "verified": true
      },
      "match_score": 0.91,
      "match_reasons": [
        "遮阳伞功能完全匹配",
        "安全绳配置匹配",
        "尺寸适合成人水上使用",
        "价格位于目标区间"
      ]
    }
  ]
}
```

---

## 场景2: 价格敏感型搜索

### 用户输入
```
"我要找批发的发圈，最便宜的那种，要1000个以上"
```

### 系统处理
```json
{
  "query_analysis": {
    "product": "发圈(橡皮筋)",
    "priority": "价格最低",
    "quantity": 1000,
    "flexibility": "数量可协商"
  },
  "search_strategy": {
    "sort_by": "price_asc",
    "filter_moq": "<=1000",
    "include_transport_cost": false
  }
}
```

### 输出结果
```json
{
  "matches": [
    {
      "product_id": "HAIR20240156",
      "product_name": "普通橡皮筋发圈 黑色 10根/包",
      "price": {
        "fob_yiwu": 0.08,
        "moq": 1000,
        "currency": "CNY",
        "total_for_1000": 80
      },
      "supplier": "义乌小商品源头工厂",
      "match_reasons": ["价格最低", "MOQ完全匹配", "支持小额批发"]
    }
  ],
  "market_insight": {
    "avg_price": 0.15,
    "this_price_percentile": 15,
    "negotiation_tip": "此价格已接近成本，可适当提高订单量换取更低单价"
  }
}
```

---

## 场景3: 设计导向型搜索

### 用户输入
```
"有没有适合ins风的北欧简约风格收纳盒，要白色系的，放在梳妆台上"
```

### 系统处理
```json
{
  "query_analysis": {
    "style_tags": ["北欧简约", "ins风", "白色系"],
    "usage": "梳妆台收纳",
    "aesthetic_priority": "高"
  },
  "visual_search": {
    "enabled": true,
    "color_preference": "白色/米白",
    "style_reference": "minimalist"
  }
}
```

### 输出结果
```json
{
  "matches": [
    {
      "product_id": "DORM20240078",
      "product_name": "北欧简约亚克力收纳盒 白色 桌面梳妆台专用",
      "price": {"fob_yiwu": 6.80, "moq": 50, "currency": "USD"},
      "style_tags": ["北欧风", "简约", "ins风", "白色系"],
      "images": ["正面图", "场景图(梳妆台放置)"],
      "match_score": 0.95
    }
  ]
}
```

---

## 场景4: 批量采购搜索

### 用户输入
```
"我们是做亚马逊的，需要找圣诞树灯串工厂，要CE认证，FOB深圳"
```

### 系统处理
```json
{
  "query_analysis": {
    "product": "圣诞树灯串",
    "user_type": "跨境电商(亚马逊)",
    "requirements": ["CE认证", "FOB深圳"],
    "order_potential": "大额"
  },
  "supplier_filter": {
    "certifications": ["CE"],
    "location": "深圳及周边",
    "export_experience": "亚马逊卖家服务经验"
  }
}
```

### 输出结果
```json
{
  "matches": [
    {
      "product_id": "XMAS20240001",
      "product_name": "LED圣诞树灯串 300灯 8模式 CE认证",
      "price": {
        "fob_shenzhen": 3.20,
        "moq": 500,
        "currency": "USD",
        "payment": "T/T 30%"
      },
      "supplier": {
        "name": "深圳光之翼灯饰有限公司",
        "certifications": ["CE", "ROHS", "UL"],
        "export_ratio": "80%",
        "amazon_clients": 45
      },
      "match_score": 0.93
    }
  ],
  "recommendation": {
    "action": "建议联系供应商获取样品",
    "moq_tip": "500个起订，可协商样品单50个"
  }
}
```

---

## 场景5: 以图搜图

### 用户输入
```
上传图片: [一款带有卡通图案的儿童书包]
```

### 系统处理
```json
{
  "image_analysis": {
    "product_type": "儿童书包",
    "features": ["卡通图案", "双肩背", "小学适用"],
    "colors_detected": ["蓝色", "黄色"],
    "style": "可爱卡通"
  },
  "reverse_image_search": {
    "method": "clip_embedding",
    "similarity_threshold": 0.75,
    "max_results": 15
  }
}
```

### 输出结果
```json
{
  "matches": [
    {
      "product_id": "BAG20240112",
      "product_name": "卡通图案双肩儿童书包 1-3年级 防水面料",
      "match_score": 0.89,
      "visual_similarity": 0.89
    }
  ],
  "filters_applied": {
    "category": "箱包 > 学生书包",
    "price_range": "不限"
  }
}
```
