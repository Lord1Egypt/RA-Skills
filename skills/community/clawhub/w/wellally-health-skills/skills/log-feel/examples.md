# log-feel 技能示例

## 一、完整输入（无需询问）

### 示例 1: 基础记录
```
用户: 肚子不舒服，左腹，轻微疼痛

保存:
{
  "timestamp": "2026-02-03T10:30:00Z",
  "bodyPart": "左腹",
  "symptom": "肚子不舒服",
  "painLevel": "1",
  "severity": 1,
  "tags": ["疼痛", "腹部"]
}
```

### 示例 2: 详细记录
```
用户: 右腹隐隐作痛，钝痛，疼了半天，吃了生冷食物后开始

保存:
{
  "timestamp": "2026-02-03T12:00:00Z",
  "bodyPart": "右腹",
  "symptom": "右腹隐隐作痛",
  "painLevel": "3",
  "severity": 3,
  "painType": "钝痛",
  "duration": "半天",
  "triggers": ["吃了生冷食物"],
  "tags": ["疼痛", "右腹", "钝痛"]
}
```

## 二、交互式询问（信息不完整）

### 示例 3: 仅输入"肚子疼"
```
用户: 肚子疼

AI: 不适的位置在哪里？
    A. 左腹
    B. 右腹
    C. 上腹
    D. 下腹

用户: A (左腹)

AI: 疼痛程度如何？（1-10级）

用户: 3级

保存:
{
  "timestamp": "2026-02-03T14:20:00Z",
  "bodyPart": "左腹",
  "symptom": "肚子疼",
  "painLevel": "3",
  "severity": 3,
  "tags": ["疼痛", "左腹"]
}
```

### 示例 4: 仅输入"头疼"
```
用户: 头疼

AI: 疼痛程度如何？
    A. 轻微 (1-3级)
    B. 中度 (4-6级)
    C. 严重 (7-10级)

用户: A

AI: 持续多长时间了？

用户: 从昨天开始

保存:
{
  "timestamp": "2026-02-03T09:00:00Z",
  "bodyPart": "头部",
  "symptom": "头疼",
  "painLevel": "2",
  "severity": 2,
  "duration": "从昨天开始",
  "tags": ["疼痛", "头部"]
}
```

### 示例 5: 多字段缺失
```
用户: 不舒服

AI: 请详细描述你的症状或不适感觉？

用户: 胃疼

AI: 疼痛程度如何？（1-10级）

用户: 5级，比较疼

AI: 持续多久了？

用户: 2小时

保存:
{
  "timestamp": "2026-02-03T16:30:00Z",
  "bodyPart": "上腹",
  "symptom": "胃疼",
  "painLevel": "5",
  "severity": 5,
  "duration": "2小时",
  "tags": ["疼痛", "胃部"]
}
```

### 示例 6: 疼痛类型推断
```
用户: 脖子感觉针扎似的疼

AI: 疼痛程度如何？（1-10级）

用户: 6级

保存:
{
  "timestamp": "2026-02-03T11:00:00Z",
  "bodyPart": "颈部",
  "symptom": "脖子感觉针扎似的疼",
  "painLevel": "6",
  "severity": 6,
  "painType": "刺痛",
  "tags": ["疼痛", "颈部"]
}
```

### 示例 7: 伴随症状
```
用户: 头疼，还有点恶心

AI: 疼痛程度如何？

用户: 4级

保存:
{
  "timestamp": "2026-02-03T20:00:00Z",
  "bodyPart": "头部",
  "symptom": "头疼",
  "painLevel": "4",
  "severity": 4,
  "accompanyingSymptoms": ["恶心"],
  "tags": ["疼痛", "头部", "恶心"]
}
```

### 示例 8: 情绪状态
```
用户: 肚子疼，有点焦虑

AI: 哪个部位疼？
    A. 左腹
    B. 右腹
    C. 上腹
    D. 下腹

用户: C (上腹)

AI: 疼痛程度？

用户: 2级

保存:
{
  "timestamp": "2026-02-03T15:00:00Z",
  "bodyPart": "上腹",
  "symptom": "肚子疼",
  "painLevel": "2",
  "severity": 2,
  "mood": "焦虑",
  "tags": ["疼痛", "上腹", "焦虑"]
}
```

### 示例 9: 无痛不适
```
用户: 脖子僵硬

AI: 持续多久了？

用户: 今天早上开始

保存:
{
  "timestamp": "2026-02-03T08:00:00Z",
  "bodyPart": "颈部",
  "symptom": "脖子僵硬",
  "painType": "无",
  "painLevel": "1",
  "severity": 1,
  "duration": "今天早上开始",
  "tags": ["颈部", "僵硬"]
}
```

## 三、关键词识别示例

### 身体部位自动识别
| 输入 | 识别结果 |
|-----|---------|
| "左边肚子疼" | bodyPart: "左腹" |
| "胃不舒服" | bodyPart: "上腹" |
| "后背疼" | bodyPart: "背部" |
| "肩膀酸" | bodyPart: "肩部" |

### 疼痛程度自动识别
| 输入 | 识别结果 |
|-----|---------|
| "有点疼" | painLevel: "1", severity: 1 |
| "轻微疼痛" | painLevel: "2", severity: 2 |
| "中度疼痛" | painLevel: "5", severity: 5 |
| "疼得很厉害" | painLevel: "7", severity: 7 |
| "剧烈疼痛" | painLevel: "10", severity: 10 |

### 疼痛类型自动识别
| 输入 | 识别结果 |
|-----|---------|
| "隐隐作痛" | painType: "隐痛" |
| "针扎似的疼" | painType: "刺痛" |
| "胀痛" | painType: "胀痛" |
| "绞痛" | painType: "绞痛" |
| "跳痛" | painType: "跳痛" |
| "灼痛" | painType: "灼痛" |
