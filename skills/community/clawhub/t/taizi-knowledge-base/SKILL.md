---
name: taizi-knowledge-base
description: 个人知识库 - 融合向量检索、实体关系、笔记管理
version: 1.0.0
---

# 个人知识库

统一管理：向量检索 + 实体关系 + 笔记存储

## 触发词
- "存入知识库"
- "查知识库"
- "记一笔"
- "帮我记住"

## 存储位置
- 向量库：`~/.openclaw/knowledge_base/`
- 实体库：`~/.openclaw/workspace/memory/ontology/`
- 笔记库：`~/.openclaw/workspace/notes/`

## 命令

### 存入知识库
```bash
python C:\Users\Administrator\.openclaw\scripts\vector_kb.py add --text "内容" --source "来源"
```

### 搜索知识库
```bash
python C:\Users\Administrator\.openclaw\scripts\vector_kb.py search --query "关键词" --top 5
```

### 查看统计
```bash
python C:\Users\Administrator\.openclaw\scripts\vector_kb.py stats
```

### 添加笔记文件
```bash
python C:\Users\Administrator\.openclaw\scripts\vector_kb.py add-file --path "C:\path\to\file.md"
```

## 工作流程
1. 收到用户内容 → 判断类型
2. 实体关系 →存入 ontology
3. 文本内容 → 存入向量库
4. 笔记文件 → 存入 Obsidian 目录

## 自动处理
- 文本：自动分块存入向量库
- 实体：自动提取人物/项目/事件关系
- 文件：自动索引并可检索
