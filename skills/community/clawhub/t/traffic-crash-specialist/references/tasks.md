# Tasks - 六大任务详解

## 任务分类

### Linguistic-centric Tasks（语言中心任务）

需要语义理解和推理能力，输出为自然语言。

---

### 1. Crash Recognition（事故识别）

**目标**: 判断视频是否包含交通事故

**输入**: 交通视频
**输出**: Yes / No + 事故类型

**示例**:
```
Q: Does this video contain a traffic crash?
A: Yes, this video shows a rear-end collision between two vehicles.
```

**评估指标**: Accuracy, F1-score

---

### 2. Crash Description（事故描述）

**目标**: 详细描述事故过程

**输入**: 事故视频
**输出**: 详细描述文本

**示例**:
```
Q: Describe what happened in this crash.
A: A white SUV was traveling in the right lane when a motorcycle 
   attempted to merge. The SUV driver didn't notice the motorcycle 
   and collided with it, causing the motorcycle to fall.
```

**评估指标**: BLEU, ROUGE, human evaluation

---

### 3. Causal Reasoning（因果推理）

**目标**: 分析事故原因

**输入**: 事故视频
**输出**: 原因分析（多因素）

**示例**:
```
Q: What caused this crash?
A: Multiple factors contributed:
   1. Driver distraction (primary cause)
   2. Wet road surface (environmental factor)
   3. Inadequate braking distance (contributing factor)
```

**评估指标**: Cause accuracy, reasoning coherence

---

### 4. Prevention Reasoning（预防推理）

**目标**: 提出预防建议

**输入**: 事故视频
**输出**: 预防措施

**示例**:
```
Q: How could this crash have been prevented?
A: 
   1. Driver should maintain focus on the road
   2. Reduce speed in wet conditions
   3. Increase following distance
   4. Use turn signals before merging
```

**评估指标**: Prevention relevance, completeness

---

### Perception-centric Tasks（感知中心任务）

需要精确的时空定位能力，输出包含时间或空间坐标。

---

### 5. Pre-crash Localization（事故前定位）

**目标**: 定位事故发生前的危险时刻

**输入**: 事故视频
**输出**: 时间戳（秒）

**示例**:
```
Q: When does the dangerous situation start?
A: The dangerous situation begins at 3.2 seconds when the 
   first vehicle starts to brake suddenly.
```

**评估指标**: Temporal IoU, mAP

---

### 6. Crash Localization（事故定位）

**目标**: 定位事故发生的精确时刻

**输入**: 事故视频
**输出**: 时间戳（秒）

**示例**:
```
Q: When does the crash occur?
A: The crash occurs at 5.7 seconds when the two vehicles collide.
```

**评估指标**: Temporal IoU, accuracy

---

## Traffix VideoQA 任务

### 1. Multiple-choice Video QA
- 多选问答
- 覆盖天气、交通状态、事件类型等

### 2. Referred Object Captioning
- 特定对象的描述
- 需要结合时空信息

### 3. Spatio-Temporal Object Grounding
- 时空联合定位
- 输出: (时间区间, 空间 bbox)

---

## 任务组合建议

### 完整分析流程
```
1. Crash Recognition → 判断是否事故
2. Crash Localization → 定位事故时刻
3. Crash Description → 描述事故过程
4. Causal Reasoning → 分析事故原因
5. Prevention Reasoning → 提出预防建议
```

### 简化流程
```
Recognition + Localization + Description (基础版)
```