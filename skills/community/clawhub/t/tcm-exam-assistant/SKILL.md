---
name: tcm-exam-assistant
description: 中医执业医师考试备考助手 - 生成每日复习计划、评估答案、管理错题集
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins: ["node"]
---

# tcm-exam-assistant 技能 v2.0

## 功能描述

中医执业医师考试备考助手，**专注于复习计划生成、答案评估和错题管理**。

**注意**：文档读取（docx/txt/pdf/表格）由 OpenClaw 主程序/AI 处理，本 skill 通过 simple-memory 持久化存储学习进度。

## 核心功能

1. **每日计划生成** - 根据用户反馈生成次日复习计划（新学 + 复习）
2. **答案评估** - 批改用户提交的真题答案，指出错误点并解析
3. **错题管理** - 记录错题到错题集，支持导出打印
4. **进度追踪** - 记录学习进度，支持笔试→技能考试阶段切换
5. **激进模式** - 支持 conservative/standard/aggressive/crazy 四种学习强度

## 多 Skills 协作架构

```
┌─────────────────────────────────────────────────────────┐
│                    OpenClaw 主程序                       │
│  （AI 理解用户意图，调度各个 skills）                      │
└─────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ OpenClaw AI   │  │ tcm-exam-     │  │ save-to-word  │
│ 文档读取       │  │ assistant     │  │ 导出错题集    │
│ - docx        │  │ - 生成计划     │  │ - docx        │
│ - txt         │  │ - 评估答案     │  │               │
│ - pdf         │  │ - 错题管理     │  │               │
│ - 表格         │  │ - 进度追踪     │  │               │
└───────────────┘  └───────────────┘  └───────────────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            ▼
                  ┌─────────────────┐
                  │  simple-memory  │
                  │  (持久化存储)    │
                  └─────────────────┘
```

## 使用场景

### 场景 1：上传备考文档，生成复习计划
```
用户：上传 2026 执考 -85-中医执考复习大提点.docx
      根据文档内容，生成我的复习计划
```
**流程**：
1. OpenClaw AI 读取 docx 文档
2. 调用 tcm-exam-assistant 生成计划
3. 输出：每日复习计划

### 场景 2：动态提问
```
用户：我目前在中内第三章，昨晚咳嗽没看懂，今天应该看什么？
```
**流程**：
1. OpenClaw AI 理解问题
2. 调用 tcm-exam-assistant 生成针对性计划
3. 输出：今日任务

### 场景 3：提交答案，评估错题
```
用户：今天做了 10 道题，答案：1.A 2.B 3.C 4.A 5.B 6.C 7.A 8.B 9.C 10.A
      正确答案：1.A 2.B 3.A 4.A 5.B 6.C 7.A 8.A 9.C 10.A
```
**流程**：
1. 调用 tcm-exam-assistant 评估答案
2. 记录错题到 simple-memory
3. 输出：正确率 + 错题分析

### 场景 4：导出错题集
```
用户：导出我的错题集为 Word 文档
```
**流程**：
1. 调用 tcm-exam-assistant 获取错题数据
2. 调用 save-to-word 生成 docx 文件
3. 输出：Word 文档路径

## 调用方式

### 1. 生成每日计划

```bash
node <skill-dir>/assistant.js "generate-plan" "{{用户反馈}}"
```

**用户反馈示例**：
```
今天复习了技能第一站，病例分析还不熟
```
```
今天复习了中内肺系病证第 3-4 节（感冒、咳嗽），中午背了麻黄桂枝对比，晚饭后看了方剂学麻黄汤，做了 10 道真题，错了 3 道（第 2、5、8 题）
```

### 2. 评估答案

```bash
node "C:\Users\梁\.openclaw\skills\tcm-exam-assistant\assistant.js" "evaluate-answers" "{{题目}}" "{{用户答案}}" "{{正确答案}}"
```

### 3. 导出错题集

```bash
node "C:\Users\梁\.openclaw\skills\tcm-exam-assistant\assistant.js" "export-wrong-questions"
```

## 核心特性

### 阶段自动判断
- **技能考试阶段**（考前 90 天内）：以技能三站训练为主
- **笔试阶段**：以中医内科学、中药、方剂等笔试科目为主

### 时间适配
- **中午 30 分钟**：只安排背诵内容（口诀、表格、对比）
- **晚上 3 小时**：安排理解、做题、错题分析

### 激进模式
| 模式 | 系数 | 适用场景 |
|------|------|----------|
| conservative | 1.0 | 基础薄弱、时间充裕 |
| standard | 1.2 | 正常复习节奏 |
| aggressive | 1.5 | 时间紧张、冲刺阶段（默认） |
| crazy | 2.0 | 极限冲刺、考前 30 天 |

## 记忆文件

| 文件 | 说明 |
|------|------|
| `memory/stage.json` | 当前备考阶段（skill-exam-prep / written-exam-prep） |
| `memory/progress.json` | 学习进度（按科目） |
| `memory/wrong-questions.json` | 错题集 |
| `memory/review-schedule.json` | 复习调度（艾宾浩斯曲线） |
| `memory/user-profile.json` | 用户画像（偏好/习惯） |
| `memory/doc-cache.json` | 文档缓存（考试信息） |

## 科目列表

| 科目代码 | 科目名称 |
|----------|----------|
| skill-station-1 | 技能第一站（病例分析） |
| skill-station-2 | 技能第二站（操作） |
| skill-station-3 | 技能第三站（答辩） |
| tcm-herbs | 中药学 |
| tcm-formulas | 方剂学 |
| tcm-internal | 中医内科学 |
| acupuncture | 针灸学 |
| tcm-basic | 中医基础理论 |
| tcm-diagnosis | 中医诊断学 |
| western-medicine | 西医综合 |

## 输出路径

- 错题集导出：用户配置的输出目录
- 文档目录：用户配置的备考文档目录

## 考试日期配置

在 `assistant.js` 中修改：
```javascript
const SKILL_EXAM_DATE = new Date('2026-06-06');   // 技能考试
const WRITTEN_EXAM_DATE = new Date('2026-08-15'); // 笔试
