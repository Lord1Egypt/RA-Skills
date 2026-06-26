# Professional 模式 - Phase 3：大纲规划

**模式**: Professional 专业模式（作者・完整但不繁琐）
**Phase数**: 4/8

---

## 3.1 创建项目文件夹

`./web-novels/{YYYYMMDD-HHmmss}-{小说名称}/`

---

## 3.2 生成大纲

创建 `00-大纲.md`：

### 基本信息

```markdown
# [小说名称]

## 基本信息
- 类型：[网文类型]
- 金手指：[金手指名称]
- 核心爽点：[核心爽点]
- 章节数：[X]章
```

### 核心设定

```markdown
## 核心设定

### 金手指设计
- 类型：
- 激活条件：
- 使用限制：
- 升级方式：

### 势力分布
- 主角阵营：
- 主要反派势力：
```

### 人物档案

```markdown
## 人物档案

### 主角
- 姓名：
- 身份：[初始身份]
- 性格：[主角性格]
- 金手指：[金手指]
- 成长阶段：[废柴→小成→大成→巅峰]

### 女主（如有）
- 姓名：
- 类型：[女主类型]
- 与主角关系：

### 主要反派
- 姓名/代号：
- 特点：[反派特点]
```

### 名场面时间轴

```markdown
## 名场面时间轴

| 章节 | 类型 | 描述 | 效果 |
|------|------|------|------|
| 第1章 | [类型] | [描述] | [效果] |
| ... | ... | ... | ... |
```

### 章节规划

```markdown
## 章节规划

### 第1章：[章节名]
- **核心事件**：
- **爽点设计**：
- **承接**：无（首章）
- **悬念钩子**：
- **情绪弧线**：[压抑→释放]
- **伏笔**：[埋下/回收]

### 第2章：[章节名]
- **核心事件**：
- **爽点设计**：
- **承接**：[上章结尾]
- **悬念钩子**：
- **情绪弧线**：[压抑→释放]
- **伏笔**：[埋下/回收]
```

---

## 3.3 生成写作计划

创建 `03-写作计划.json`：

```json
{
  "version": 2,
  "mode": "professional",
  "novelName": "[小说名称]",
  "projectPath": "./web-novels/{timestamp}-[小说名称]",
  "totalChapters": [章节数],
  "minWordsPerChapter": 2000,
  "maxWordsPerChapter": 3000,
  "status": "planning",
  "writingMode": "[serial|subagent-parallel]",
  "coreSetting": {
    "genre": "[类型]",
    "goldenFinger": "[金手指]",
    "coreTropes": "[爽点]"
  },
  "chapters": [
    {
      "chapterNumber": 1,
      "title": "[章节标题]",
      "filePath": "第01章.md",
      "status": "pending",
      "wordCount": null,
      "famousScene": "[名场面类型]",
      "emotionalArc": "[情绪弧线]",
      "foreshadow": { "seeds": [], "resolves": [] },
      "retryCount": 0
    }
  ]
}
```

---

## 3.4 规划确认 + 写作模式选择

```markdown
## 《[小说名称]》规划确认

📊 规模：[X] 章 | 每章 2000-3000 字
🧑 主角：[主角名称] | [身份]
👥 女主：[女主名称] | [类型]
😈 反派：[反派类型]
⭐ 名场面：[X] 个（每X章1个）
🔥 核心爽点：[核心爽点]
```

**选择写作模式**：
- 【串行】主 Agent 逐章写 ⭐
- 【并行】子 Agent 分批并行

```
Question: 确认规划并选择写作模式
Options:
- 确认，开始创作（串行）
- 确认，使用并行模式
```

---

→ 进入 [Pro4_Full_Draft_Writing.md](./Pro4_Full_Draft_Writing.md)
