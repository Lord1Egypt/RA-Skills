# VOC-CTQ 数据格式规范

## 目录
- [输入数据格式](#输入数据格式)
- [输出数据格式](#输出数据格式)
- [示例文件](#示例文件)
- [验证规则](#验证规则)

---

## 输入数据格式

### 1. JSON格式(推荐)
```json
{
  "feedbacks": [
    {
      "id": "voc_001",
      "text": "产品做工太差，用了两天就坏了",
      "source": "客服热线",
      "timestamp": "2024-01-15 10:30:00",
      "weight": 1.0
    },
    {
      "id": "voc_002",
      "text": "希望能增加更多颜色选择",
      "source": "问卷调查",
      "timestamp": "2024-01-15 14:22:00",
      "weight": 0.8
    }
  ]
}
```

### 2. CSV格式
| text | source | timestamp | weight |
|------|--------|-----------|--------|
| 产品做工太差，用了两天就坏了 | 客服热线 | 2024-01-15 10:30:00 | 1.0 |
| 希望能增加更多颜色选择 | 问卷调查 | 2024-01-15 14:22:00 | 0.8 |

**约束**：`text`列必填；`id`、`source`、`timestamp`、`weight`可选

### 3. TXT格式
每行一条反馈文本，ID自动生成(从voc_001递增)
```
产品做工太差，用了两天就坏了
希望能增加更多颜色选择
服务态度很好，但发货太慢
```

---

## 输出数据格式

### 1. 分析结果(analyze模式)
```json
{
  "analyzed_vocs": [
    {
      "id": "voc_001",
      "original_text": "产品做工太差，用了两天就坏了",
      "segmented_text": ["产品", "做工", "太差", "用了", "两天", "就", "坏了"],
      "keywords": ["做工", "太差", "坏"],
      "pos_tags": {"做工": "n", "太差": "a", "坏": "v"},
      "sentiment_score": 0.15,
      "sentiment_label": "negative",
      "requirement_type": "quality",
      "entities": {"subject": "产品", "problem": "损坏"}
    }
  ],
  "statistics": {
    "total_count": 50,
    "positive_count": 12,
    "negative_count": 28,
    "neutral_count": 10,
    "word_frequency": {"做工": 15, "质量": 12, "服务": 10}
  }
}
```

### 2. CTQ定义(ctq.json)
```json
{
  "ctqs": [
    {
      "id": "ctq_001",
      "name": "产品耐用性",
      "description": "产品在正常使用条件下的使用寿命",
      "category": "可靠性",
      "keywords": ["耐用", "寿命", "持久", "损坏", "故障"],
      "weight": 1.0,
      "status": "candidate"
    },
    {
      "id": "ctq_002",
      "name": "外观设计多样性",
      "description": "产品外观款式的丰富程度",
      "category": "美学",
      "keywords": ["颜色", "款式", "外观", "选择"],
      "weight": 0.7,
      "status": "confirmed"
    }
  ]
}
```

### 3. 映射关系(map模式)
```json
{
  "mappings": [
    {
      "voc_id": "voc_001",
      "ctq_id": "ctq_001",
      "confidence": 0.95,
      "match_keywords": ["做工", "坏"]
    },
    {
      "voc_id": "voc_002",
      "ctq_id": "ctq_002",
      "confidence": 0.88,
      "match_keywords": ["颜色", "选择"]
    }
  ],
  "mapping_summary": {
    "total_vocs": 50,
    "mapped_vocs": 45,
    "unmapped_vocs": 5,
    "total_ctqs": 10,
    "coverage_rate": 0.90
  }
}
```

### 4. 评分结果(evaluate模式)
```json
{
  "ctq_scores": [
    {
      "ctq_id": "ctq_001",
      "ctq_name": "产品耐用性",
      "frequency_score": 0.85,
      "sentiment_score": 0.72,
      "importance_score": 0.90,
      "final_score": 0.823,
      "priority_rank": 1,
      "priority_level": "P0"
    }
  ],
  "scoring_method": {
    "frequency_weight": 0.4,
    "sentiment_weight": 0.3,
    "importance_weight": 0.3
  }
}
```

---

## 示例文件

### customer_feedback.json
```json
{
  "feedbacks": [
    {
      "id": "voc_001",
      "text": "手机电池续航太差，一天要充两次电",
      "source": "电商评价",
      "weight": 1.0
    },
    {
      "id": "voc_002", 
      "text": "相机拍照效果很满意，就是存储空间太小",
      "source": "客服回访",
      "weight": 0.9
    },
    {
      "id": "voc_003",
      "text": "包装盒设计很好看，送人很有面子",
      "source": "社交媒体",
      "weight": 0.7
    }
  ]
}
```

---

## 验证规则

### 输入验证
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| text | string | 必填, 长度>0 | 反馈文本内容 |
| id | string | 可选, 唯一 | 反馈唯一标识 |
| weight | float | 可选, 0.0-1.0 | 权重值 |
| timestamp | string | 可选, ISO格式 | 时间戳 |

### 输出验证
| 字段 | 类型 | 约束 | 说明 |
|------|------|------|------|
| sentiment_score | float | 0.0-1.0 | 0=极度负面, 1=极度正面 |
| confidence | float | 0.0-1.0 | 映射置信度 |
| final_score | float | 0.0-1.0 | CTQ综合评分 |

### 优先级等级
| 等级 | 分数范围 | 说明 |
|------|----------|------|
| P0 | >=0.8 | 紧急处理，需立即关注 |
| P1 | 0.6-0.8 | 重点改进 |
| P2 | 0.4-0.6 | 持续优化 |
| P3 | <0.4 | 观察暂缓 |
