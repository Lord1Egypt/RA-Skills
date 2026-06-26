# Datasets - 数据集详解

## CrashChat Dataset

### 数据规模
- 视频数: 18,385
- QA 对数: 96,184
- 来源: D²-City, MM-AU, Nexar, 自采集

### 数据格式

#### 目录结构
```
data/
├── videos/
│   ├── cap_1_001537.mp4
│   ├── cap_1_002004.mp4
│   └── ...
├── crashchat_dada_video_total_cause_reasoning_train.json
├── crashchat_dada_video_total_cause_reasoning_test.json
├── crashchat_dada_video_total_cause_reasoning_val.json
└── ... (其他任务 JSON)
```

#### JSON 格式示例
```json
{
  "video": "cap_1_001537.mp4",
  "QA": [
    {
      "question": "What caused this crash?",
      "answer": "The driver lost control due to slippery road conditions.",
      "task": "causal_reasoning"
    }
  ]
}
```

### 数据集版本
- `CrashChat-original`: 原始分辨率
- `CrashChat-resized`: 统一分辨率（推荐训练使用）

---

## TUMTraf VideoQA Dataset

### 数据规模
- 视频数: 1,000
- 多选 QA: 85,000 对
- 对象描述: 2,300 标注
- 对象定位: 5,700 标注

### 特色场景
- 恶劣天气（雨、雪、雾）
- 交通异常（事故、拥堵）
- 复杂路边监控视角

### 任务类型

#### 1. Multiple-choice Video QA
```json
{
  "video": "traffic_001.mp4",
  "question": "What is the weather condition?",
  "options": ["Clear", "Rainy", "Snowy", "Foggy"],
  "answer": "Rainy"
}
```

#### 2. Object Captioning
```json
{
  "video": "traffic_001.mp4",
  "object_id": "obj_12",
  "caption": "A red sedan moving in the left lane"
}
```

#### 3. Spatio-Temporal Grounding
```json
{
  "video": "traffic_001.mp4",
  "query": "the car that brakes suddenly",
  "temporal": [5.2, 7.8],  // 秒
  "spatial": [0.3, 0.5, 0.6, 0.8]  // bbox [x1, y1, x2, y2]
}
```

---

## 其他相关数据集

### 公开交通数据集
| 数据集 | 规模 | 特色 |
|--------|------|------|
| D²-City | 大规模 | 交通事故标注 |
| MM-AU | 多模态 | 行人-车辆交互 |
| Nexar | 行车记录仪 | 真实碰撞视频 |
| BDD100K | 100K 视频 | 多任务驾驶场景 |
| COCO | 图像 | 通用目标检测基线 |

### 数据集选择建议
- **事故分析**: CrashChat + D²-City
- **时空定位**: TUMTraf + BDD100K
- **恶劣场景**: TUMTraf (专用)
- **综合训练**: 多数据集联合