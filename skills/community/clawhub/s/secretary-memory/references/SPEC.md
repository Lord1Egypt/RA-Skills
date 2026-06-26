# OpenClaw 秘书式记忆系统规格文档

## 概述

仿生现代秘书的笔记本分类法，将记忆分区管理，各司其职。

## 目录结构

```
memory/
├── daily/              # 每日原始日志（7天内）
│   └── 2026-04-30.md
├── archive/            # 已完成的事（7天前归档）
│   ├── daily/         # 归档日志
│   ├── projects/      # 已结束项目
│   ├── decisions/     # 历史决策
│   └── index.json    # 话题索引
├── agenda/            # 待办事项
│   ├── today/
│   ├── this-week/
│   └── follow-ups/
├── profile/            # 用户偏好档案
│   ├── preferences/
│   ├── habits/
│   └── contacts/
├── projects/           # 进行中项目
│   └── README.md
├── knowledge/         # 知识沉淀
│   ├── tech/
│   └── domain/
├── consolidate.py     # 归档脚本
├── memory_search.py   # 多分区搜索脚本
└── migrate.py         # 迁移脚本
```

## 各分区职责

### daily/ — 每日日志
- **来源**: 每次会话自动追加（从 memory/ 移动过来）
- **格式**: 时间戳 + 会话摘要 + 关键决策点
- **保留**: 7天

### archive/ — 历史档案
- **来源**: daily 定期 consolidation（7天后）
- **内容**: 已完成项目、已定决策、旧日记
- **保留**: 永久

### agenda/ — 待办事项
- **来源**: 用户指令 + 自动提取
- **内容**: today/this-week/follow-ups 三级
- **保留**: 完成即移走

### profile/ — 用户画像
- **来源**: 初始化 + 增量更新
- **内容**: 偏好、习惯、联系人
- **保留**: 只增不改

### projects/ — 项目跟踪
- **来源**: 用户提及项目时创建/更新
- **内容**: 项目状态、进度、关键节点
- **保留**: 结束移至 archive

### knowledge/ — 知识沉淀
- **来源**: 会话中提取的事实性知识
- **内容**: 技术笔记、领域概念
- **保留**: 持久

## 文件格式

### daily/ 日志格式
```markdown
# 2026-04-30

## 14:30 - 会话摘要
- 话题: iOS键盘问题
- 关键: iPhone 8 iOS 15 存储不足

## 15:42 - 项目记忆
- 用户开始设计新记忆系统
- 目录结构: daily/archive/agenda/profile/projects/knowledge
```

### agenda/today.md 格式
```markdown
# 今日待办 - 2026-04-30

## 进行中
- [ ] 完成记忆系统规格文档

## 新增
- [ ] 跟进用户 iOS 升级问题
```

### profile/preferences.md 格式
```markdown
# 用户偏好

## 沟通风格
- 回答风格: 简洁直接，不废话
- 格式: 喜欢列表/表格

## 技术背景
- 熟悉: React Native, Flask
- 了解: LangGraph, RAG, 智能体
```

## 归档触发机制

### archive/ 触发时机

| 触发条件 | 说明 |
|---------|------|
| `--deep` 搜索 | 包含 archive/ |
| `--archive-only` | 仅查 archive/ |
| consolidation 关联 | 归档新内容时，自动关联已有相关归档 |
| 用户显式查询 | 用户问"之前那个XXX"时 |

### 话题自动关联

consolidation 时会：
1. 提取话题关键词（项目名、技术栈、领域词）
2. 扫描已有 archive，建立话题 → 文件的映射
3. 新归档内容时，链接到相关历史归档
4. 生成 `archive/index.json` 索引文件

```json
{
  "topics": {
    "GUI Agent": ["archive/projects/2026-04-26-gui-agent.md"],
    "React Native": ["archive/projects/2026-04-16-react-native.md"]
  },
  "files": {
    "decisions/2026-04-20-采用-minimax-vlm.md": {
      "topics": ["MiniMax", "VLM", "GUI Agent"],
      "type": "decisions"
    }
  }
}
```

### 搜索优先级策略

- **常规搜索**: profile > agenda > projects > knowledge > daily > archive
- **深度搜索 (--deep)**: 包含 archive/
- **仅归档搜索 (--archive-only)**: 仅查 archive/

## consolidation 机制

- **触发**: 每日 18:00 Asia/Shanghai 或手动执行
- **脚本**: `consolidate.py`
- **流程**:
  1. 扫描 daily/ 下超过7天的文件
  2. 提取项目信息 → archive/projects/
  3. 提取决策记录 → archive/decisions/
  4. 提取话题关键词，建立关联索引
  5. 移动日志 → archive/daily/
  6. 更新 memory.md 精选摘要
  7. 更新 archive/index.json 话题索引
