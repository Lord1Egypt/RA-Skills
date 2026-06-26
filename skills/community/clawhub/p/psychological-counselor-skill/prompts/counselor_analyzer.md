
# 心理咨询师分析器提示词

## 任务
分析一位心理咨询师的原材料，提取以下信息：

### 1. 基本信息
- 姓名/代号
- 教育背景
- 受训背景
- 一句话描述

### 2. 理论取向
分析咨询师的理论取向，包括：
- 主要流派（精神分析/认知行为/人本/家庭治疗/整合等）
- 核心理论观点
- 对人性的理解
- 对心理问题的理解

### 3. 咨询风格
分析咨询师的咨询风格，包括：
- 主动 vs 被动
- 指导 vs 陪伴
- 结构化 vs 非结构化
- 理性分析 vs 情感共情
- 语言风格（简洁/温暖/直接/委婉等）

### 4. 常用技术
分析咨询师常用的技术，包括：
- 具体技术（释梦/认知重构/正念/空椅子/家庭格盘等）
- 提问风格（开放式/封闭式/挑战式/澄清式等）
- 干预方式（解释/面质/支持/重构等）

### 5. 伦理边界
分析咨询师的伦理边界，包括：
- 如何设置咨询框架（时间/费用/保密性等）
- 如何处理危机情况
- 如何处理移情和反移情
- 如何处理多重关系

---

## 输出格式
用以下格式输出：

```
【基本信息】
姓名/代号：{name}
教育背景：{education}
受训背景：{training}
一句话描述：{description}

【理论取向】
主要流派：{orientation}
核心理论观点：
- {point1}
- {point2}
- {point3}
对人性的理解：{view-of-human-nature}
对心理问题的理解：{view-of-problems}

【咨询风格】
主动 vs 被动：{active-passive}
指导 vs 陪伴：{directive-supportive}
结构化 vs 非结构化：{structured-unstructured}
理性分析 vs 情感共情：{rational-emotional}
语言风格：{language-style}

【常用技术】
具体技术：
- {technique1}
- {technique2}
- {technique3}
提问风格：{questioning-style}
干预方式：{intervention-style}

【伦理边界】
框架设置：{frame-setting}
危机处理：{crisis-handling}
移情反移情：{transference-countertransference}
多重关系：{multiple-relationships}
```

---

## 注意事项
- 基于提供的原材料进行分析，不要编造
- 如果原材料中没有明确信息，可以注明"未明确提及"
- 保持客观，不要加入个人评判
