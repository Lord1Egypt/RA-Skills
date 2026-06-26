---
name: web-novel-master
description: |
  爆款网文创作助手。分章节创作引人入胜的爆款网文，支持都市爽文/玄幻修仙/穿越重生/甜宠言情等多种类型。每章2000-3000字，强调爽点驱动、名场面设计、金句记忆。
  当用户要求：写网文，写小说、创作故事、分章节写作、连续剧情时使用。
metadata:
  trigger: 爆款网文创作、分章节故事、长篇小说创作、网文写作
  source: 基于爆款网文最佳实践设计
  supported_platforms:
    - claude_code
    - openclaw
---

# Web Novel Master: 爆款网文创作助手

## 四大黄金法则

1. **爽点驱动** - 每章必须有爽点，读者追更是为了"爽"
2. **情绪波动** - 有憋有放，张弛有度，虐后必爽
3. **金句记忆** - 每章必须有让读者想截图的金句
4. **名场面** - 每3-5章必须有让人印象深刻的名场面

## 三种创作模式

| 模式 | Phase数 | 适用场景 |
|------|---------|---------|
| **Fast** | 5 | 爱好者，极简快速 |
| **Professional** | 8 | 作者，质量优先 |
| **Industrial** | 10 | 团队，流水线生产 |

---

## 核心流程

进入每个阶段时，先阅读对应的流程文档以获取详细执行指令。

### Phase 0: 初始化

读取用户偏好，检测未完成项目（中断续写），展示个性化欢迎。
→ 详见 [Phase0_Initialization.md](references/flows/Phase0_Initialization.md)

### 模式选择

→ 详见 [Mode_Selector.md](references/flows/Mode_Selector.md)

用户选择模式后，进入对应模式的 Phase 1。

---

## 模式文件索引

### Fast 快速模式（5 Phase）

| Phase | 文件 | 核心职责 |
|-------|------|---------|
| 0 | Fast/Fast0_Initialization.md | 初始化 |
| 1 | Fast/Fast1_Idea_Clarify.md | 想法明确 |
| 2 | Fast/Fast2_Quick_Draft.md | 快速起草 |
| 3 | Fast/Fast3_Simple_Polish.md | 简单润色 |
| 4 | Fast/Fast4_Final_Validation.md | 最终校验 |

### Professional 专业模式（8 Phase）

| Phase | 文件 | 核心职责 |
|-------|------|---------|
| 0 | Pro/Pro0_Initialization.md | 初始化 |
| 1 | Pro/Pro1_Core_Clarify.md | 核心明确 |
| 2 | Pro/Pro2_World_Character_Setup.md | 世界观与人设 |
| 3 | Pro/Pro3_Outline_Planning.md | 大纲规划 |
| 4 | Pro/Pro4_Full_Draft_Writing.md | 正文撰写 |
| 5 | Pro/Pro5_Polish_Pacing.md | 润色节奏 |
| 6 | Pro/Pro6_Hook_Packaging.md | 钩子包装 |
| 7 | Pro/Pro7_Validation_Release.md | 校验发布 |

### Industrial 工业模式（10 Phase）

| Phase | 文件 | 核心职责 |
|-------|------|---------|
| 0 | Ind/Ind0_Project_Initialize.md | 项目初始化 |
| 1 | Ind/Ind1_Market_Research.md | 市场调研 |
| 2 | Ind/Ind2_Core_Positioning.md | 核心定位 |
| 3 | Ind/Ind3_World_Rule_Setup.md | 世界规则设定 |
| 4 | Ind/Ind4_Character_Standard.md | 人物标准化 |
| 5 | Ind/Ind5_Modular_Outline.md | 模块化大纲 |
| 6 | Ind/Ind6_Team_Writing.md | 团队写作 |
| 7 | Ind/Ind7_Unified_Polish.md | 统一润色 |
| 8 | Ind/Ind8_QC_Validation.md | QC校验 |
| 9 | Ind/Ind9_Release_Operation.md | 发布运营 |

---

## 共享机制

偏好系统、写作计划系统、爆款网文速查表等跨阶段共享机制。
→ 详见 [Shared_Infrastructure.md](references/flows/Shared_Infrastructure.md)
