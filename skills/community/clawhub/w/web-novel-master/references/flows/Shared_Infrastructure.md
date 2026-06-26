# 共享基础设施

本文件定义跨阶段共享的机制、规则和数据结构。

---

## 爆款网文四法则

1. **爽点驱动** — 每章必须有爽点，读者追更是为了"爽"
2. **情绪波动** — 有憋有放，张弛有度，虐后必爽
3. **金句记忆** — 每章必须有让读者想截图的金句
4. **名场面** — 每3-5章必须有让人印象深刻的名场面

---

## 用户偏好系统

### 存储文件

`user-preferences.json`（项目根目录，首次使用后自动创建）

### 数据结构

```json
{
  "version": 2,
  "updatedAt": "2026-04-18",
  "preferences": {
    "favoriteGenres": [],
    "preferredGoldenFinger": "",
    "preferredProtagonist": "",
    "preferredCoreTropes": "",
    "typicalChapterCount": null,
    "styleReferences": [],
    "dislikes": [],
    "creationHistory": []
  }
}
```

### 偏好更新规则

| 时机 | 行为 |
|------|------|
| 每完成一个 Phase | 静默将本 Phase 结果同步到偏好文件 |
| 用户说"记住我的偏好" | 保存当前所有配置到偏好 |
| 用户说"忘记XX偏好" | 清除指定维度的偏好 |
| 用户说"重置偏好" | 清空所有偏好数据 |
| 一部作品创作完成 | 将作品信息追加到 `creationHistory` |

### 偏好如何影响交互

1. **启动欢迎语**：有偏好时显示"欢迎回来！" + 个性化提示
2. **选项排序**：将匹配项排前面并标记⭐
3. **常用标记**：常用选项标记"你的常用"/"上次选择"
4. **随机生成**：优先从偏好范围内随机选取

### 错误恢复

- **回退修改**：用户随时可说"回到QX"、"修改XX"
- **中途暂存**：通过 `03-写作计划.json` 实现自动暂存
- **偏好文件损坏**：忽略偏好，使用默认值

---

## 写作计划系统

### 存储文件

`03-写作计划.json`（项目文件夹内，Phase 5 创建）

### 作用

- **进度跟踪**：记录每章创作状态（pending/in_progress/completed/failed）
- **写作模式**：记录用户选择的写作模式
- **名场面跟踪**：记录每章的名场面类型和描述
- **中断续写**：Phase 0 读取 JSON 检测未完成项目
- **校验依据**：Phase 9 基于 JSON 校验章节完成度

### JSON Schema

```json
{
  "version": 3,
  "novelName": "[小说名称]",
  "projectPath": "./web-novels/{timestamp}-[小说名称]",
  "totalChapters": [章节数],
  "minWordsPerChapter": 2000,
  "maxWordsPerChapter": 3000,
  "createdAt": "[ISO时间]",
  "updatedAt": "[ISO时间]",
  "status": "planning",
  "writingMode": "[serial|subagent-parallel|agent-teams]",
  "coreSetting": {
    "genre": "[网文类型]",
    "goldenFinger": "[金手指类型]",
    "coreTropes": "[核心爽点]"
  },
  "chapters": [
    {
      "chapterNumber": 1,
      "title": "[章节标题]",
      "filePath": "第01章.md",
      "status": "pending",
      "wordCount": null,
      "wordCountPass": null,
      "famousScene": "[名场面类型]",
      "famousSceneDesc": "[名场面描述]",
      "emotionalArc": "[本章情绪弧线]",
      "foreshadow": {
        "seeds": ["[埋下的伏笔]"],
        "resolves": ["[回收的伏笔]"]
      },
      "retryCount": 0
    }
  ]
}
```

### JSON 状态流转

```
planning → in_progress → validating → completed
                              ↓
                           failed (可重试，最多3次)
```

---

## 字数检查脚本

```bash
# 检查单个章节
python scripts/check_chapter_wordcount.py ./web-novels/项目文件夹/第01章.md

# 检查所有章节
python scripts/check_chapter_wordcount.py --all ./web-novels/项目文件夹/

# 自定义最小字数
python scripts/check_chapter_wordcount.py ./web-novels/项目文件夹/第01章.md 2500
```

### 使用场景

| Phase | 用途 |
|-------|------|
| Phase 6（撰写） | 撰写后检查单章字数 |
| Phase 7（润色） | 润色后再次确认 |
| Phase 9（校验） | 批量检查所有章节字数 |

---

## 爽点类型速查

| 爽点类型 | 适用场景 | 关键词 |
|---------|---------|-------|
| 打脸爽 | 退婚/羞辱/质疑 | "你不是说我废物吗？" |
| 升级爽 | 突破/获得传承 | "境界突破！" |
| 装逼爽 | 被逼展示/身份反差 | "不是我想装..." |
| 甜宠爽 | 吃醋/护短/撒糖 | "以后离他远点" |
| 复仇爽 | 清算/打脸仇人 | "该还了" |
| 燃点爽 | 守护/热血/战斗 | "谁都不能动..." |

---

## 金句公式

```
打脸金句："你说的XX...好像有点短？"
装逼金句："不是我想装，是你们逼我的。"
燃点金句："谁都不能动我在乎的人。"
甜点金句："以后离他远点，听见没？"
```

---

## 开篇公式

```
第1章 = 觉醒爽点 + 大钩子

退婚流：废物开局 → 退婚羞辱 → 意外觉醒
系统流：濒死危机 → 系统激活 → 新手任务
重生流：死亡/失败 → 重生节点 → 先知优势
```

---

## 流程状态转换图

```
┌─────────────────────────────────────────────────────────────────┐
│                    爆款网文创作10阶段流程                         │
└─────────────────────────────────────────────────────────────────┘

Phase 0 ──→ Phase 1 ──→ Phase 2 ──→ Phase 3 ──→ Phase 4
 初始化      市场调研    核心明确    世界人设    风格定制
    │          │           │           │           │
    │           ↓           ↓           ↓           ↓
    │      ┌─────────────────────────────────────────┐
    │      │           快捷入口/问答入口              │
    │      └─────────────────────────────────────────┘
    │                                               │
    ↓                                               ↓
Phase 9 ←─ Phase 8 ←─ Phase 7 ←─ Phase 6 ←──── Phase 5
 校验发布     钩子包装     润色节奏     大纲规划 ←┘
                                          ↑
                               用户确认后进入
```

### 阶段状态流转

| 当前 Phase | 触发条件 | 下一 Phase | 可返回 |
|-----------|---------|-----------|--------|
| Phase 0 | 完成初始化 | Phase 1 或 Phase 5（跳过） | - |
| Phase 1 | 完成市场分析 | Phase 2 | Phase 0 |
| Phase 2 | Q1-Q4 完成 | Phase 3 | Phase 1 |
| Phase 3 | Q5-Q8 完成 | Phase 4 | Phase 2 |
| Phase 4 | 用户确认配置 | Phase 5 | Phase 3 |
| Phase 5 | 用户确认大纲+写作模式 | Phase 6 | Phase 4 |
| Phase 6 | 所有章节完成 | Phase 7 | - |
| Phase 7 | 所有章节润色完成 | Phase 8 | - |
| Phase 8 | 包装完成 | Phase 9 | Phase 7 |
| Phase 9 | 校验完成 | 完成 | Phase 6 |

### 写作模式

| 模式 | 说明 | 适用场景 |
|------|------|---------|
| `serial` | 主 Agent 逐章串行写 | 短中篇，默认推荐 |
| `subagent-parallel` | 子 Agent 分批并行写 | 中长篇，追求速度 |
| `agent-teams` | Claude Code 多 Agent 协作 | 大型长篇，需手动开启 |

---

## 项目目录结构

```
web-novels/
└── {timestamp}-{小说名称}/
    ├── 00-大纲.md                    # 故事大纲 + 章节规划
    ├── 01-人物档案.md                # 主角/女主/反派档案
    ├── 03-写作计划.json              # 写作进度状态
    └── 第XX章-xxx.md                # 各章正文
```

---

## 阶段文件索引

| Phase | 文件 | 核心职责 |
|-------|------|---------|
| Phase 0 | Phase0_Initialization.md | 初始化、偏好加载、中断续写检测 |
| Phase 1 | Phase1_Market_Research.md | 市场分析、套路速查、意向提取 |
| Phase 2 | Phase2_Core_Clarify.md | 类型、金手指、爽点、主角 |
| Phase 3 | Phase3_World_Character_Setup.md | 世界观、情感线、反派、名场面 |
| Phase 4 | Phase4_Style_Customization.md | 读者定位、章节数量、特殊要求 |
| Phase 5 | Phase5_Outline_Planning.md | 大纲生成、人物档案、写作计划 |
| Phase 6 | Phase6_Full_Draft_Writing.md | 逐章创作、三种写作模式 |
| Phase 7 | Phase7_Polish_Pacing.md | AI味清除、语言质量、节奏调整 |
| Phase 8 | Phase8_Hook_Packaging.md | 标题优化、章节简介、连载钩子 |
| Phase 9 | Phase9_Validation_Release.md | 自动校验、自动修复、完成报告 |
| - | Shared_Infrastructure.md | 共享机制、偏好系统、写作计划 |
