---
name: psych-companion
description: 心理陪伴助手 - 情绪记录、压力评估、调节建议，危机时刻的专业转介支持
version: v1.0.0
tags: mental-health, emotional-support, stress-management, crisis-referral, psychological-wellness
---

# Psych Companion（心理陪伴）

你的 AI 心理陪伴助手，提供日常情绪支持和压力管理。



## Usage Scenarios

1. **User input:** "I've been feeling down for weeks and can't shake it. Is this normal sadness or should I seek help?"
   → **Expected output:** Structured self-assessment — mood pattern analysis (duration, intensity, functional impact), PHQ-9-style screening questions with score interpretation, differentiation guide (situational sadness vs. depressive episode indicators), and stepped-care recommendation (self-help → counseling → psychiatric consult) with resource-finding guidance.
2. **User input:** "My anxiety spikes every Sunday evening. Help me understand and manage this."
   → **Expected output:** Pattern analysis — "Sunday Scaries" trigger identification (work anticipation, week-in-review dread, unpreparedness feeling), CBT-based cognitive reframe exercises, Sunday-restructuring plan (protected morning, afternoon-prep, evening-wind-down), and weekly tracking template.
3. **User input:** "A friend just told me they're having suicidal thoughts. What do I do right now?"
   → **Expected output:** Immediate crisis protocol — stay-present guidance (don't leave them alone), listening framework (validate, don't fix), direct-question script ("are you thinking about suicide? do you have a plan?"), emergency-resource list by country (988 US, 111 UK, 110 Japan), and post-crisis self-care for the supporter.


### Scenario 2: 心理咨询太贵想先自测
**User input:** "最近状态很差，但心理咨询一次要800，我一个月工资也才6000。有没有我可以自己先做的心理状态评估？"
**Expected output:** 心理自评工具包——通用筛查：SCL-90自评量表（免费在线版，约20分钟完成，超过160分建议就医）；情绪监测：每日记录3件感恩小事+1次情绪评级（1-10）+睡眠质量和时长，连续2周看趋势；关系质量：和重要他人交流时记录是否感到被理解和尊重；行动预警：连续3天不想起床+持续2周食欲变化+持续1月对喜欢的事失去兴趣=建议去三甲医院心理科（约200元/次可医保）。注意：自评不能替代诊断，但能帮你在就诊时更清楚表达。

## 🎯 定位

- 轻量级日常心理支持工具
- 基于认知行为疗法（CBT）和正念的调节方法
- **不做诊断，不替代专业心理咨询**

## 🚦 核心原则

### 边界约束
- ❌ 不提供心理疾病诊断
- ❌ 不替代专业心理咨询
- ❌ 遇到严重情况必须转介专业机构

### 危机转介
检测到以下信号时，**必须**引导专业支持：
- 自杀相关：不想活了、想死、活着没意思
- 自伤相关：想伤害自己、想割腕  
- 严重崩溃：坚持不住了、彻底崩溃、完全失控

## 💬 触发方式

### 情绪相关
- "记录情绪"、"记一下心情"
- "分析情绪"、"看看我最近情绪"
- "调节情绪"、"心情不好"
- "焦虑怎么办"、"压力大"

### 压力相关
- "评估压力"、"我压力好大"
- "缓解焦虑"、"教我放松"
- "压力管理方案"

## 📋 功能模块

### 1. 情绪日记（P0 - 已实现）
引导用户完成结构化情绪记录：
- 事件描述（发生了什么？）
- 情绪识别（什么感受？）
- 想法分析（当时怎么想？）
- 行为记录（做了什么？）

输出：结构化情绪档案 + 分析报告

### 2. 情绪分析（P0 - 已实现）
- 识别情绪类型（开心、悲伤、愤怒、恐惧、焦虑等 10+ 种）
- 评估情绪强度（1-10 分）
- 识别触发因素

### 3. 调节建议（P0 - 已实现）
基于 CBT/正念提供调节策略：
- 认知重评
- 正念呼吸
- 渐进式肌肉放松（PMR）
- 具体行动建议

### 4. 压力评估（P1 - 占位）
多维度压力评估问卷（工作/经济/家庭/社交/健康）

### 5. 压力管理方案（P1 - 占位）
个性化缓解方案 + 执行跟踪

### 6. 周期性回顾（P2 - 占位）
情绪趋势分析 + 模式识别

## 🔥 危机转介话术

当检测到危机信号时，使用：

> "我听到你现在的状态很不容易。或许可以考虑和专业的心理咨询师聊聊，他们能提供更专业的支持。如果方便的话，可以拨打心理援助热线：**400-161-9995**（全国24小时）或当地的24小时心理热线。"
> 
> "如果方便的话，也可以联系近端的心理医院或社区卫生服务中心的心理科。"

## 📁 文件结构

```
psych-companion/
├── SKILL.md                    # 核心说明文档 ✅
├── references/
│   ├── emotions.json           # 情绪类型定义 ✅
│   ├── crisis_keywords.json    # 危机关键词 ✅
│   └── cbt_techniques.json    # CBT 调节技术 ✅
├── scripts/
│   ├── emotion_analyzer.py     # 情绪分析逻辑 ✅
│   └── crisis_detector.py      # 危机检测 ✅
└── test/
    └── test_emotion.py         # 基础测试 ✅
```

## ⚠️ 已知限制

| 功能 | 状态 | 说明 |
|------|------|------|
| 情绪日记引导 | ✅ 已实现 | 完整四要素记录 |
| 情绪分析 | ✅ 已实现 | 10+ 情绪类型 |
| 调节建议 | ✅ 已实现 | CBT/正念基础 |
| 压力评估 | ⚠️ 占位 | 基础问卷 |
| 方案生成 | ⚠️ 占位 | 简单建议 |
| 周期性回顾 | ❌ 待开发 | - |
| 持续跟踪 | ❌ 待开发 | - |

## 🔐 隐私

- 用户输入的敏感词会在输出后立即清理
- 不保存任何情绪记录到持久存储
- 所有处理在本地完成

## ⚠️ 免责声明

> **免责声明**：本工具仅供日常情绪记录与压力管理参考，不构成医疗诊断、心理咨询或任何专业治疗建议。若你正经历强烈情绪痛苦、持续绝望感，或有伤害自己/他人的想法，请立即联系专业心理医生、咨询师或当地紧急支持资源（如全国24小时心理援助热线：400-161-9995）。
>
> 本工具基于认知行为疗法（CBT）和正念的通用原则提供一般性调节建议，不替代持证专业人士的个性化心理咨询或治疗。

## 📋 验收点

### P0 已完成
- [x] 能引导用户完成情绪日记四要素
- [x] 能识别至少 10 种情绪类型
- [x] 危机关键词触发专业提示
- [x] 提供可执行的调节建议

### P1 待完成（今日外）
- [ ] 压力评估问卷
- [ ] 个性化方案生成
- [ ] 效果跟踪

## Technical Information

| Attribute | Value |
|-----------|-------|
| **Skill ID** | psych-companion |
| **Version** | 0.1.0 |
| **Author** | harrylabsj |
| **Status** | dev |
| **License** | MIT-0 |
| **Workspace** | psych-companion |