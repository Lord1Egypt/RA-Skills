## 常见标注输出格式

### JSONL 格式（推荐）

每行一个 JSON 对象，适合大规模标注数据：

```jsonl
{"source_file": "images/001.jpg", "annotation_time": "2026-03-19T13:00:00Z", "objects": [{"label": "person", "bbox": [100, 50, 200, 300], "confidence": 0.95}], "scene": "办公室", "risk_level": "low"}
{"source_file": "images/002.jpg", "annotation_time": "2026-03-19T13:01:00Z", "objects": [{"label": "vehicle", "bbox": [50, 80, 400, 250]}], "scene": "停车场", "risk_level": "medium"}
```

### VL 模型微调数据集格式

适用于视觉-语言模型微调：

```jsonl
{"messages": [{"role": "user", "content": "<image>请描述这张图片中的内容，包括场景、人物、行为和潜在风险。"}, {"role": "assistant", "content": "这是一张安防监控画面，场景为..."}], "images": ["images/001.jpg"]}
{"messages": [{"role": "user", "content": "<image>请分析这张图片中的异常行为。"}, {"role": "assistant", "content": "画面中出现一名未授权人员正在..."}], "images": ["images/002.jpg"]}
```

### 分类标注格式

```jsonl
{"source_file": "data/text_001.txt", "category": "positive", "confidence": 0.92, "keywords": ["优秀", "推荐", "满意"]}
{"source_file": "data/text_002.txt", "category": "negative", "confidence": 0.88, "keywords": ["差", "投诉", "不满"]}
```

### 实体识别标注格式

```jsonl
{"source_file": "data/doc_001.txt", "entities": [{"text": "张三", "type": "PERSON", "start": 5, "end": 7}, {"text": "北京", "type": "LOCATION", "start": 20, "end": 22}]}
```

### 通用标注 Schema 字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| source_file | string | ✅ | 原始数据文件路径 |
| annotation_time | string | ✅ | 标注时间（ISO 8601） |
| category/label | string | 视需求 | 分类标签 |
| confidence | number | 视需求 | 置信度 0-1 |
| objects | array | 视需求 | 检测到的对象列表 |
| entities | array | 视需求 | 识别到的实体列表 |
| scene | string | 视需求 | 场景描述 |
| description | string | 视需求 | 详细描述 |
| risk_level | string | 视需求 | 风险等级 |
| custom_fields | object | 视需求 | 需求文档定义的其他字段 |

### summary.json 格式

```json
{
  "task_name": "安防视频标注",
  "created_at": "2026-03-19T13:00:00Z",
  "updated_at": "2026-03-19T14:30:00Z",
  "total_files": 100,
  "annotated_files": 95,
  "failed_files": 2,
  "pending_files": 3,
  "category_distribution": {
    "low_risk": 60,
    "medium_risk": 25,
    "high_risk": 10
  },
  "processing_time_seconds": 320,
  "model_used": "qwen3.5-plus"
}
```
