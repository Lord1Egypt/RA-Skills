---
name: web-novel-creator
description: |
  网文创作兼容协调层。
  定位：不做一个独立的创作引擎，而是让现有的优秀创作Skill（如 novel-generator、open-novel-writing、novel-orchestrator 等）能够无缝对接 Memory Manager Pro 的索引系统。
  核心价值：(1) 提供统一的项目目录规范，让各Skill共享同一个项目空间；(2) 作为创作结束后对接 Memory Manager Pro 索引更新的标准入口。
  Use when: 已有的独立创作Skill（如 novel-generator）已创作完章节，需要归档、更新索引、或继续统筹下一步创作。
  Not when: 用户要从零开始创作小说（用 novel-generator）、需要多角色协作（用 novel-orchestrator）、或需要全流程设定管理（用 open-novel-writing）。
---

# Web Novel Creator

网文创作兼容协调层。不取代 `novel-generator`、`open-novel-writing`、`novel-orchestrator` 等专项 Skill，而是让它们能共享统一的**项目目录规范**和**索引归档流程**。

## 核心定位

```
SkillHub 网文创作生态：

  novel-generator      open-novel-writing      novel-orchestrator
  （从零生成爽文）     （全流程设定管理）       （多角色协作）
        │                      │                       │
        └──────────────────────┼───────────────────────┘
                               ▼
                      web-novel-creator
                  （兼容协调层：统一目录规范 + 索引归档入口）
                               │
                               ▼
                      Memory Manager Pro
                  （语义推导 + 全量索引更新）
```

### 不做什么
- 不自建"从零到一章"的创作引擎 —— 用 `novel-generator`
- 不替代多角色协作 —— 用 `novel-orchestrator`
- 不管理世界观/人设 —— 用 `open-novel-writing`
- 不生成图片 —— 用 `nano-banana-pro`
- 不做索引管理 —— 和 `Memory Manager Pro` 配合，但由后者执行

### 做什么
- 统一项目目录规范（让各 Skill 产出都存到同一位置）
- 创作完成后对接 Memory Manager Pro 更新索引（统一入口）
- 当项目目录规范尚未建立时，初始化标准结构

## 统一目录规范

所有与本 Skill 兼容的创作 Skill 应遵循以下目录结构：

```
novel/{项目名}/
├── 正文/                    # 章节正文（各Skill共同读写）
│   ├── 第001章.md
│   └── 第XXX章.md
├── 规划/                    # 章节规划（兼容层统一管理）
│   ├── 已用标题库.md
│   ├── 第XXX章规划.md
│   └── 规划模板.md
├── 设定/                    # 世界观/人设（open-novel-writing 或其他 Skill 使用）
│   ├── 世界观.md
│   └── 人物/
├── 总纲/                    # 故事总纲（cq-novel-writer 或其他 Skill 使用）
│   └── 故事总纲.md
├── .learnings/              # 记忆系统（novel-generator 使用）
│   ├── CHARACTERS.md
│   ├── LOCATIONS.md
│   └── PLOT_POINTS.md
└── output/                  # 输出目录（novel-generator 使用）
```

> 各 Skill 可选择性地使用目录中的部分结构。例如 novel-generator 使用 `正文/`、`.learnings/`、`output/`；open-novel-writing 使用 `正文/`、`设定/`、`规划/`。

## 快速开始

### 场景A：兼容 Skill 完成创作后归档
```
1. 检测是哪类 Skill 完成了创作
   - novel-generator: 检查 .learnings/ 和 output/
   - open-novel-writing: 检查 设定/ 和 规划/
   - novel-orchestrator: 检查 规划/ 和 正文/

2. 将产出迁移到统一目录（如需要）
   - 正文 → novel/{项目名}/正文/
   - 规划 → novel/{项目名}/规划/

3. 调用 Memory Manager Pro 完成索引更新
   → 传递参数（路径由 Memory Manager Pro 自动推导）
```

### 场景B：初始化项目目录
```
1. 创建标准目录结构
   mkdir -p novel/{项目名}/{正文,规划,设定,总纲,.learnings,output}

2. 初始化标题库
   检查 novel/{项目名}/正文/ 中已存在的文件，生成已用标题库

3. 调用 Memory Manager Pro 初始化记忆索引
   → 传递参数：项目名、创建初始任务
```

## 兼容对接指南

### 对接 novel-generator

**novel-generator 的产出位置**：
- 正文：`output/第X章.md` → 迁移到 `正文/第XXX章.md`
- 记忆：`.learnings/` → 保留在原位（已兼容规范）
- 本 Skill 不干涉 novel-generator 的引导流程，只在其创作完成后接管归档

**对接流程**：
```
1. novel-generator 完成创作后
   → detect: 检测到 .learnings/ 目录和 output/ 文件

2. web-novel-creator 介入归档
   → 将 output/ 中的正文移动到 novel/{项目名}/正文/
   → 检查 规划/ 中是否有对应的规划文件
   → 如没有规划文件，只需要归档正文即可

3. 调用 Memory Manager Pro
   → 更新索引，记录章节完成
```

### 对接 open-novel-writing

**open-novel-writing 的产出位置**：
- 正文：`novel/{项目名}/正文/`（兼容规范）
- 设定：`novel/{项目名}/设定/`（兼容规范）
- 规划：`novel/{项目名}/规划/`（兼容规范）

**对接流程**：
```
1. open-novel-writing 完成创作后
   → detect: 检测到 设定/ 目录

2. web-novel-creator 确认目录规范一致，检查标题库是否更新
   → 如标题库未更新，进行补录

3. 调用 Memory Manager Pro
   → 更新索引，记录章节完成
```

### 对接 novel-orchestrator

**novel-orchestrator 的产出位置**：
- 正文：`novel/{项目名}/正文/`（兼容规范）
- 规划：`novel/{项目名}/规划/`（兼容规范）

**对接流程**：
```
1. novel-orchestrator 的 checker 通过审查后
   → detect: 检测到 writer 产出 + checker 通过记录

2. web-novel-creator 确认目录规范一致，检查标题库是否更新
   → 如标题库未更新，进行补录

3. 调用 Memory Manager Pro
   → 更新索引，记录章节完成
```

### 对接 cq-novel-writer

**cq-novel-writer 的产出位置**：
- 正文：`novel/`（根目录，需迁移）
- 故事总纲：`novel/故事总纲.md`（兼容规范）

**对接流程**：
```
1. cq-novel-writer 完成创作后
   → detect: 检测到 故事总纲.md

2. web-novel-creator 将正文从根目录迁移到 novel/{项目名}/正文/
   → 如正文文件需要重命名，统一为 第XXX章.md 格式

3. 调用 Memory Manager Pro
   → 更新索引，记录章节完成
```

## 创作流程规则

### 规则1：依赖外部创作 Skill

本 Skill **不直接创作正文**（除了在规划不存在时根据上一章生成后续规划）。

**创作正文的触发流程**：
```
用户请求"继续写第X章"
  ↓
检查是否有现成规划
  ↓
有规划 → 判断适合用哪个 Skill 创作
  ├── 从零开始的创作 → 委托 novel-generator
  ├── 需要设定管理 → 委托 open-novel-writing
  ├── 需要审核流程 → 委托 novel-orchestrator
  └── 简单的续写 → 直接创作（fallback）
  ↓
无规划 → 读取上一章末段生成规划
      → 然后按上述流程创作
```

### 规则2：规划预生成
创作完成后，如当前 Skill 没有生成下一章规划，由兼容层补充：
- 存储位置：`novel/{项目名}/规划/第XXX章规划.md`
- 内容：核心冲突、剧情要点、字数目标、伏笔设置

### 规则3：标题去重检验
无论使用哪个外部 Skill 创作，最终都必须通过标题库去重检验：
- 标题库：`novel/{项目名}/规划/已用标题库.md`
- 外部 Skill 创作后，由兼容层检查标题是否已录入
- 未录入时由兼容层补充

### 规则4：索引更新 → 委托给 Memory Manager Pro

创作完成后，**不要自己编辑索引文件**。将索引更新任务交给 **Memory Manager Pro Skill** 完成。

**传递参数格式**（路径由 Memory Manager Pro 自动推导）：
```
Memory Manager Pro 索引更新请求
{
  "操作": "完成创作并更新索引",
  "任务ID": "TASK_NOVEL_YYYYMMDD_XXX",
  "章节": "第XXX章《标题名》",
  "字数": "XXXX字",
  "项目": "天道养殖场",          // 用于语义推导项目目录
  "来源Skill": "novel-generator",  // 标记哪类Skill完成的创作
  "创建下一章任务": true,
  "下一章章节名": "第XXX+1章《标题》"
}
```

**Memory Manager Pro 会负责以下完整流程**：
1. 创建/更新任务详情文件（标记为已完成）
2. 更新已完成任务索引（追加记录、更新统计）
3. 更新活跃任务索引（移除已完成、添加新任务）
4. 更新项目索引进度
5. 更新类型索引
6. 更新已用标题库
7. 更新MEMORY.md
8. 更新核心索引

## 兼容检测模板

用于识别当前使用了哪些外部 Skill：

```markdown
# .skill-detect

当 web-novel-creator 被调用时，检查以下标识文件/目录：

## 检测清单

| 标识文件/目录 | 对应的 Skill | 检测方式 |
|--------------|-------------|---------|
| .learnings/ | novel-generator | 目录是否存在 |
| output/ | novel-generator | 目录是否存在 |
| 设定/世界观.md | open-novel-writing | 文件是否存在 |
| 总纲/故事总纲.md | cq-novel-writer | 文件是否存在 |
| references/agent-setup.md | novel-orchestrator | 引用文件中是否有agent-setup |

## 优先级顺序

同时检测到多个 Skill 时：
1. novel-orchestrator（最复杂，优先尊重其协作流程）
2. novel-generator（有自建记忆系统）
3. open-novel-writing（有设定管理）
4. cq-novel-writer（最简单）
5. 无检测结果 → 使用内置 fallback 创作
```

## 参考文件

详细内容请参阅 references/ 目录：
- `references/规划模板.md` - 章节规划标准模板
- `references/关键词映射.md` - 快速定位关键词表
- `references/标签系统.md` - 多维度标签检索指南
- `references/番茄小说规范.md` - 平台规范详解
- `references/对接规范.md` - 各外部Skill的对接详细说明
