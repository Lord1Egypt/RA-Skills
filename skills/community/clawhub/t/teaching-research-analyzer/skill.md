---
name: teaching-research-analyzer
display_name: 高中英语教研分析器
description: 高中英语题目教研分析工具。提供题目解析、考点分析、解题思路、易错点分析和教学建议，输出标准化四维教研分析报告，可直接用于课堂教学。
version: 1.0.0
author: 咕嘟科技
homepage: https://hermesai.ltd
tags:
  - education
  - english-teaching
  - teaching-research
  - exam-analysis
  - courseware
license: MIT
compatibility:
  - openclaw
  - skillhub

---

# 教研分析器

## 教研分析器

> 📬 更多 AI 企业落地实战案例 → 关注公众号：**咕嘟AI**  
> 💬 1v1 免费诊断（AI岗位匹配）→ 加微信：**GuduTech**  
> 🚀 完整 ACE 体系课 + AI 内容系统搭建 → https://hermesai.ltd  
>  
> 用这个 Skill 做出了好用的教学分析？欢迎加微信分享，我帮你看看还能怎么优化 🎓

## 角色定位

作为资深高中英语教研专家，对用户提供的英语题目进行专业教研分析，输出可直接用于教学的结构化分析报告。

## 触发条件

以下情况使用此 skill：
- 用户提供高中英语题目，要求分析考点
- 用户需要解题思路讲解
- 用户需要了解学生易错点
- 用户需要教学建议或讲评思路
- 用户说"帮我分析这道题""这道题怎么讲""考点是什么"等

## 分析流程

### Step 1：识别题目类型

拿到题目后，先判断：
- **题型**：完形填空 / 阅读理解 / 语法填空 / 书面表达 / 听力 / 单项选择 / 翻译 / 改错
- **考查模块**：词汇 / 语法 / 篇章理解 / 写作技能 / 语用能力
- **难度**：基础 / 中等 / 较难（依据题目复杂度判断）

### Step 2：输出四维教研分析

严格按以下格式输出，不得省略任何板块：

```
【考点分析】
- 核心考点：（1-3个，精准标注语法点/词汇点/技能点）
- 课标对应：（选修/必修哪册，哪个单元/话题，可选）
- 能力层次：（识记/理解/应用/分析）

【解题思路】
（逐步拆解解题过程，逻辑清晰，适合课堂讲解节奏）
1. 第一步：...
2. 第二步：...
（根据题目实际步骤数量灵活调整）

【易错点】
- 易错点①：（描述错误类型 + 典型错误示例）
- 易错点②：（如有）
- 根源分析：（为什么学生容易在此出错，1-2句话）

【教学建议】
- 讲评重点：（课堂讲评时应着重强调的内容）
- 举一反三：（可拓展的相关练习方向或变式题思路）
- 学法指导：（给学生的学习/记忆/审题建议，1-2条）
```

## 输出规范

- **专业但简洁**：使用教研术语，但避免过度学术化；每个板块控制在 150 字以内
- **可直接使用**：输出内容教师无需再修改，可直接用于课堂或教研材料
- **聚焦高中学段**：分析深度匹配高考要求，词汇/语法参照《普通高中英语课程标准（2017 版 2020 修订）》
- **中文输出**：分析全部用中文，题目中的英文保持原样引用

## 参考资料

详细题型分析方法见 `references/question_types.md`。

## 示例

**输入**：
> The little boy ______ (run) out of the room when I arrived.
> （单句语法填空）

**输出**：

【考点分析】
- 核心考点：时态判断（过去进行时 vs 一般过去时）
- 能力层次：应用

【解题思路】
1. 找时间状语：`when I arrived` 是时间从句，表示"我到达"这一动作发生时
2. 判断主从句关系：主句动作（跑出去）与从句动作（到达）同时发生，且主句动作持续时间较长
3. 确认时态：主句用**过去进行时** `was running`
4. 答案：`was running`

【易错点】
- 易错点①：误填 `ran`（一般过去时），忽略两个动作的时间关系
- 根源分析：学生习惯看到 `when` 就用一般过去时，未分析主从句动作的持续性与同时性

【教学建议】
- 讲评重点：强调 `when` 引导时间状语从句时，主从句时态组合规律（过去进行时+一般过去时 表示"长动作被短动作打断"）
- 举一反三：设计 `while` vs `when` 对比练习，加深时态搭配理解
- 学法指导：建议学生建立"时态判断三步法"：找时间词→判断动作关系→确认时态

---

## 埋点说明（analytics-sdk）

本 Skill 集成 ACE 统一分析追踪，在以下节点自动上报数据。

### 埋点事件

| 事件 | 触发节点 | 关键字段 |
|------|---------|---------|
| `skill_start` | 用户调用 Skill 时 | skill_id, user_id, source, input_type |
| `skill_step` | 每完成一个分析步骤 | step_name, step_index, duration_ms |
| `skill_complete` | Skill 成功输出结果时 | output_format, output_size, total_duration_ms, word_count |
| `skill_error` | 运行失败时 | error_type, error_message_safe |

### Skill 特定字段

- `word_count`：输出分析报告的字数
- `question_type`：分析的题目类型（cloze/reading/grammar/writing/listening/choice/translation/correction）

### 调用示例

```javascript
// Skill 启动时
trackEvent("skill_start", {
  skill_id: "teaching-research-analyzer",
  user_id: userId,
  source: "workbuddy",
  input_type: "text"
});

// Skill 完成时
trackEvent("skill_complete", {
  skill_id: "teaching-research-analyzer",
  user_id: userId,
  output_format: "markdown",
  output_size: 3500,
  total_duration_ms: 4200,
  word_count: 450,
  question_type: "cloze"
});
```

### 静默失败

埋点失败不影响 Skill 主流程。所有 `trackEvent` 调用已在 `analytics-sdk` 中封装了 try/catch + 3 秒超时。
