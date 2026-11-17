---
name: xuanhuan-novelist
description: |
  玄幻小说专属分章节创作助手。修炼体系·爽点节奏·势力地图·金手指·越级战斗。支持废柴流/强者归来流/系统流，10-50章长篇，每章字数可配，自动润色去AI痕迹。
  当用户要求：写玄幻小说、创作修仙小说、修真/仙侠/升级流小说时使用。
metadata:
  trigger: 创作玄幻小说、修真修仙小说、升级流小说创作
  source: 基于玄幻小说创作最佳实践设计
---

# Xuanhuan Novelist: 玄幻小说创作助手

## 三大黄金法则

1. **展示而非讲述** - 用动作和对话表现，不要直接陈述。修炼突破要写出身体感受，不要说"他变强了"
2. **爽点驱动剧情** - 每章必须包含至少一个爽点（境界突破/越级挑战/打脸装逼/宝物获取/势力扩张/复仇推进）或为下一个爽点做铺垫
3. **悬念承上启下** - 每章结尾必须留下钩子，让读者迫不及待想看下一章

## 四大玄幻支柱

1. **修炼体系** - 清晰的境界划分、金手指设计、力量边界。详见 [cultivation-system.md](references/guides/cultivation-system.md)
2. **世界观架构** - 地图递进、势力体系、宗门组织。详见 [xuanhuan-worldbuilding.md](references/guides/xuanhuan-worldbuilding.md)
3. **爽点节奏** - 打脸→升级→获宝→越级→势力扩张的波浪式递进。详见 [xuanhuan-plot-patterns.md](references/guides/xuanhuan-plot-patterns.md)
4. **战斗描写** - 境界压制感、越级艰难感、策略博弈感。详见 [battle-writing.md](references/guides/battle-writing.md)

## 特性说明

- **初稿分析与文风学习**：自动检测已有章节，分析用户文风、提取设定信息，确保续写风格一致
- **中断续写**：自动检测未完成项目，从断点继续创作
- **自动校验**：创作完成后自动检查字数和质量，不合格自动修复
- **并行写作**（可选）：支持子Agent并行写作，通过 `02-写作计划.json` 协调状态

## 核心流程

进入每个阶段时，先阅读对应的流程文档以获取详细执行指令。

### 第0步：初始化与偏好加载

读取用户偏好，检测已有初稿（自动分析文风和设定），检测未完成项目（中断续写），展示个性化欢迎。 → 详见 [phase0-initialization.md](references/flows/phase0-initialization.md)

### 初稿分析与文风学习（可选）

当检测到用户有已有章节时触发，或用户主动提供初稿时触发。分析用户写作风格、提取修炼体系/世界观/人物/剧情设定，生成结构化档案供后续创作参照。 → 详见 [draft-analysis.md](references/flows/draft-analysis.md)

### 第一阶段：三层递进式问答

通过递进式问答收集创作需求，确定小说定位与标题：

- **核心定位**（必答，Q1-Q3）：玄幻子类型（废柴流/强者归来流/系统流等）、主角设定与金手指、核心冲突 → 详见 [phase1-layer1-core.md](references/flows/phase1-layer1-core.md)
- **深度定制与规格**（Q4-Q9）：世界观架构、修炼体系、视角基调、核心主题、章节数量、创作规则定制 → 详见 [phase1-layer2-customize.md](references/flows/phase1-layer2-customize.md)
- **标题生成**：AI 基于创意元素生成候选标题，用户选择或自定义 → 详见 [phase1-layer3-title.md](references/flows/phase1-layer3-title.md)

### 第二阶段：规划 + 二次确认

创建项目文件夹（`{base}/{timestamp}-{小说名称}/`），生成修炼体系设定、势力地图、大纲、人物档案和写作计划JSON，等待用户确认。 → 详见 [phase2-planning.md](references/flows/phase2-planning.md)

### 第2.5步：写作模式选择

规划确认后，选择写作模式：
- **逐章串行**（`serial`）：主 Agent 自己逐章写，全程无中断
- **子Agent并行**（`subagent-parallel`）：将章节分成批次，派生子 Agent 并行写作
- **Agent Teams**（`agent-teams`）：多 Agent 协作模式，Agent 间可通讯（需手动开启）

→ 详见 [phase3-writing.md](references/flows/phase3-writing.md)

### 第三阶段：疯狂创作（无需用户确认）
> 切记，一旦进入这个阶段，所有过程都禁止向用户确认。用户就是你的读者，你必须把完整的小说创作完成才能与用户报告

根据用户选择的写作模式逐章执行创作流程。每章创作前必须读取大纲和修炼体系设定，严格按规划创作。支持中断续写。 → 详见 [phase3-writing.md](references/flows/phase3-writing.md)

### 第四阶段：自动校验与修复（无需用户确认）

全程无需用户介入，自动检查所有章节完成度和字数，不合格章节自动重写（最多3轮）。 → 详见 [phase4-validation.md](references/flows/phase4-validation.md)

## 共享机制

偏好系统、写作计划系统、黄金法则详解、字数检查脚本等跨阶段共享机制。 → 详见 [shared-infrastructure.md](references/flows/shared-infrastructure.md)
