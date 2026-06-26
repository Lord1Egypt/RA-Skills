---
name: thinking-spark
description: 记录思考火花与沉淀的系统。用于用户想要记录临时思考、想法、灵感火花，或者将思考整理沉淀为有条理的内容时触发。
---

# Thinking Spark - 思考火花记录系统

## 概述

用于记录临时的思考火花（突然产生，可能不完整），并支持有条后续整理为理的思考沉淀。

## 数据结构

文件位置：`collection/思考火花.json`

```json
{
  "schema_version": "1.0",
  "description": "思考火花与沉淀记录",
  "sparks": [
    {
      "id": "20260310_001",
      "content": "原始思考内容...",
      "polished_content": "整理后的沉淀内容...",
      "tags": ["AI", "Agent"],
      "origin": "spark",
      "status": "polished",
      "priority": 1,
      "confidence": 0.8,
      "source_refs": ["article:20260309_001"],
      "created_at": "2026-03-10T11:51:00Z",
      "updated_at": "2026-03-10T12:00:00Z",
      "refined_at": "2026-03-10T14:00:00Z",
      "history": [
        {"action": "created", "timestamp": "2026-03-10T11:51:00Z"},
        {"action": "refined", "timestamp": "2026-03-10T14:00:00Z"}
      ]
    }
  ]
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| id | string | 唯一标识，格式：YYYYMMDD_NNN |
| content | string | 原始思考内容 |
| polished_content | string | 整理后的沉淀内容（可选） |
| tags | array | 标签 |
| origin | string | 来源：spark(火花) 或 direct(直接沉淀) |
| status | string | 状态：raw → refining → polished → archived |
| priority | number | 优先级 1-5 |
| confidence | number | 确定程度 0-1 |
| source_refs | array | 关联外部ID，如 article:xxx, project:xxx |
| created_at | string | 创建时间 |
| updated_at | string | 更新时间 |
| refined_at | string | 整理完成时间 |
| history | array | 变更历史 |

## 命令列表

| 命令 | 说明 |
|------|------|
| `记录思考：xxx` | 快速记录火花 |
| `沉淀思考：xxx` | 直接沉淀（跳过火花状态） |
| `整理思考 [id]` | 整理指定火花 |
| `整理思考 今天` | 整理今天所有火花 |
| `查看思考` | 查看所有 |
| `查看思考 待整理` | 查看未整理 |
| `查看思考 tag:AI` | 按标签筛选 |
| `关联思考 <id> <外部ID>` | 关联外部 |
| `归档思考 <id>` | 归档已沉淀 |

## 使用示例

### 记录火花
```
记录思考：Agent 的上下文管理能力决定了它的长期记忆效果
```
→ 创建 status=raw 的火花记录

### 直接沉淀
```
沉淀思考：上下文是 Agent 最核心的能力之一，决定了能否保持对话连贯性和任务一致性
```
→ 创建 status=polished 的沉淀记录

### 整理火花
```
整理思考 20260310_001
```
→ 帮你把原始思考内容整理成有条理的文章

### 查看待整理
```
查看思考 待整理
```
→ 列出所有 status=raw 的记录

### 关联外部
```
关联思考 20260310_001 article:20260309_001
```
→ 将思考与待阅文章关联

## 与其他系统整合

- **待阅文章**：`source_refs: ["article:ID"]` 形成"阅读→思考→沉淀"闭环
- **开源项目**：`source_refs: ["project:ID"]`
- **MEMORY.md**：polished + priority≥4 可候选写入长期记忆

## 原子写入

更新 JSON 时使用临时文件 + rename 防止损坏：
```bash
# 伪代码
tmp_file=$(mktemp)
jq . > $tmp_file
mv $tmp_file collection/思考火花.json
```

## 脚本

Scripts 目录提供确定性操作：

| 脚本 | 用法 |
|------|------|
| `create_spark.py` | `python3 create_spark.py "思考内容" "tag1,tag2"` |
| `list_sparks.py` | `python3 list_sparks.py [raw\|polished\|today\|tag:xxx]` |
| `update_spark.py` | `python3 update_spark.py <id> refine "整理后内容"` |
