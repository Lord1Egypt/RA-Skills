# 架构设计文档

## 📐 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                    Unified Memory Architect                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │   API层     │  │   脚本层    │  │   数据层    │             │
│  │             │  │             │  │             │             │
│  │ query.cjs  │  │ migrate.js  │  │ memories    │             │
│  │ demo.cjs   │  │ enhance.js   │  │ index       │             │
│  │ solve.js   │  │ import.js    │  │ stats       │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         └────────────────┼────────────────┘                     │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Unified Memory v5.0.1                     ││
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       ││
│  │  │  记忆   │  │  搜索   │  │  融合   │  │  索引   │       ││
│  │  │  存储   │  │  BM25   │  │  RRF   │  │  多层   │       ││
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘       ││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

## 🗂️ 7层目录结构

```
memory/
├── README.md                     # 项目说明
├── REFACTORING_PLAN.md          # 重构计划
├── FINAL_REPORT.md              # 完成报告
├── integration-config.json      # 集成配置
│
├── raw/                         # 第1层: 原始数据（只读）
│   ├── events/                  # 事件日志
│   ├── session-corpus/          # 会话语料库
│   └── ingestion/               # 摄入数据
│
├── processed/                   # 第2层: 处理后的数据
│   ├── memories.jsonl          # 基础记忆
│   ├── memories-enhanced.jsonl # 增强记忆
│   ├── index.json              # 基础索引
│   ├── index-enhanced.json     # 增强索引
│   ├── stats.json              # 基础统计
│   └── stats-enhanced.json     # 增强统计
│
├── import/                      # 第3层: 导入数据
│   ├── 2026-04-06.jsonl
│   ├── 2026-04-09.jsonl
│   ├── 2026-04-10.jsonl
│   ├── 2026-04-11.jsonl
│   ├── 2026-04-12.jsonl
│   ├── 2026-04-13.jsonl
│   └── manifest.json
│
├── archive/                     # 第4层: 归档数据
│   └── 2026-04/
│       ├── daily-ingestion.json
│       ├── events.jsonl
│       ├── phase-signals.json
│       ├── session-corpus/
│       ├── session-ingestion.json
│       └── short-term-recall.json
│
├── scripts/                     # 第5层: 处理脚本
│   ├── migrate-simple.cjs
│   ├── enhance-tags.cjs
│   ├── integrate-unified-memory.cjs
│   ├── import-memories.cjs
│   ├── query.cjs
│   ├── cleanup.cjs
│   ├── demo.cjs
│   ├── solve-problem.cjs
│   └── verify-system.cjs
│
├── docs/                        # 第6层: 文档
│   ├── integration-guide.md
│   └── format.md
│
└── .dreams/                    # 第7层: 配置
    └── (config files)
```

## 🔧 核心模块

### 1. 数据处理模块

#### 1.1 migrate-simple.cjs
- **功能**: 原始数据迁移
- **输入**: raw/ 目录
- **输出**: processed/ 目录
- **处理**: JSON → JSONL 格式转换

#### 1.2 enhance-tags.cjs
- **功能**: 标签增强
- **输入**: memories.jsonl
- **输出**: memories-enhanced.jsonl
- **处理**: 语义标签提取、实体识别、情感分析

#### 1.3 import-memories.cjs
- **功能**: 导入到统一格式
- **输入**: raw/ 目录
- **输出**: import/ 目录
- **处理**: 按日期分组导入

### 2. 查询模块

#### 2.1 query.cjs
- **功能**: 多模式查询
- **支持查询类型**:
  - `tag <tag> [limit]` - 按标签查询
  - `date <date> [limit]` - 按日期查询
  - `sentiment <sentiment> [limit]` - 按情感查询
  - `search <keyword> [limit]` - 全文搜索
  - `stats` - 统计信息

### 3. 集成模块

#### 3.1 integrate-unified-memory.cjs
- **功能**: Unified Memory v5.0.1 集成
- **特性**:
  - 混合搜索（BM25 + 向量 + RRF）
  - 记忆压缩与清理
  - 关联推荐
  - 泳道隔离

## 📊 数据格式

### 记忆条目格式

```json
{
  "id": "dream:2026-04-12:session-id:line-num",
  "type": "dream",
  "timestamp": "2026-04-12T15:32:00.000Z",
  "source": {
    "file": "session-corpus/2026-04-12.txt",
    "session": "session-id",
    "userLine": "5",
    "assistantLine": "6"
  },
  "content": {
    "user": "用户消息...",
    "assistant": "助手回复...",
    "language": "zh",
    "format": "markdown"
  },
  "metadata": {
    "confidence": 1.0,
    "tags": ["dream", "reflection", "water", "memory"],
    "entities": ["room", "mirror", "water", "surface"],
    "sentiment": "neutral",
    "wordCount": {
      "user": 34,
      "assistant": 25,
      "total": 59
    }
  },
  "attribution": {
    "agent": "xiaozhi",
    "channel": "feishu",
    "user": "ou_7b3a4352f86486ebdaf0de572093afb1"
  },
  "date": "2026-04-12",
  "analysis": {
    "hasReflection": true,
    "hasWaterImagery": true,
    "hasMemoryTheme": false,
    "isTechnical": false
  }
}
```

## 🔍 索引结构

### 多层索引

```json
{
  "byType": { "dream": ["id1", "id2", ...] },
  "byDate": { "2026-04-12": ["id1", "id2", ...] },
  "byTag": { "reflection": ["id1", "id2", ...] },
  "bySentiment": { "neutral": ["id1", "id2", ...] },
  "byLanguage": { "zh": ["id1", "id2", ...] },
  "byEntity": { "water": ["id1", "id2", ...] }
}
```

## ⚡ 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 总记忆数 | 1760 | - |
| 唯一标签 | 49 | - |
| 唯一实体 | 181 | - |
| 检索速度提升 | 5-10x | 混合搜索 |
| 存储节省 | 60% | 压缩归档 |

## 🔗 依赖关系

```
migrate-simple.cjs
    ├── raw/events/
    ├── raw/session-corpus/
    └── raw/ingestion/
            │
            ▼
enhance-tags.cjs
    │
    ├── memories.jsonl
    └── processed/index.json
            │
            ▼
integrate-unified-memory.cjs
    │
    ├── memories-enhanced.jsonl
    └── index-enhanced.json
            │
            ▼
query.cjs
    │
    ├── memories-enhanced.jsonl
    └── index-enhanced.json
```
