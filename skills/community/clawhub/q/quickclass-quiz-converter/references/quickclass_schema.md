---
AIGC:
  ContentProducer: '001191110102MAD55U9H0F10002'
  ContentPropagator: '001191110102MAD55U9H0F10002'
  Label: '1'
  ProduceID: '0b299cbf-6182-47db-9b92-1df2a9e707cc'
  PropagateID: '0b299cbf-6182-47db-9b92-1df2a9e707cc'
  ReservedCode1: '346819b0-d81a-4410-ba7a-bf8028cc6e95'
  ReservedCode2: '346819b0-d81a-4410-ba7a-bf8028cc6e95'
---

# QuickClass 作业 JSON Schema 规范

## 顶层结构

```json
{
  "teacher": "教师姓名",
  "grade": "年级学期",
  "subject": "学科",
  "taskTitle": "任务标题（如章节名）",
  "quizTitle": "测验标题（如'前测'、'练习题'）",
  "description": "描述（可为空字符串）",
  "questions": [ ... ]
}
```

## 题目字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | CUID2 格式唯一标识，如 `cmshqbzmd00076t7iq26nt33a` |
| type | string | 是 | `SINGLE_CHOICE` / `MULTIPLE_CHOICE` / `TRUE_FALSE` |
| content | string | 是 | 题目内容 |
| options | string | 是 | JSON 字符串格式的选项（判断题为 `"{}"` ） |
| answer | string | 是 | 单选: `"A"`; 多选: `"A,B,C"`; 判断: `"T"` / `"F"` |
| difficulty | string | 是 | `BASIC` / `INTERMEDIATE` / `ADVANCED` / `EXPANDED` |
| score | number | 是 | 分值（可为 0） |
| explanation | string/null | 否 | 解析（无解析时为 `null`） |
| order | number | 是 | 题目序号（从 0 开始） |

## 题型详解

### SINGLE_CHOICE（单选题）

- `options`: `{"A":"选项A","B":"选项B","C":"选项C","D":"选项D"}` 的 JSON 字符串
- `answer`: 单个字母，如 `"B"`
- 注意: options 字段是 **JSON 字符串**，不是嵌套对象

```json
{
  "id": "cmshqbzmd00076t7iq26nt33a",
  "type": "SINGLE_CHOICE",
  "content": "圆是由（ ）围成的封闭图形。",
  "options": "{\"A\":\"直线\",\"B\":\"曲线\",\"C\":\"折线\",\"D\":\"线段\"}",
  "answer": "B",
  "difficulty": "BASIC",
  "score": 0,
  "explanation": "圆是曲线图形，由一条曲线围成。",
  "order": 0
}
```

### MULTIPLE_CHOICE（多选题）

- `options`: 同单选题格式
- `answer`: 逗号分隔的多个字母，如 `"A,B,C"`

```json
{
  "id": "cmrtak3di000d3xfvoo5kfc1a",
  "type": "MULTIPLE_CHOICE",
  "content": "下面关于圆的说法中，正确的有（ ）。",
  "options": "{\"A\":\"圆有无数条直径\",\"B\":\"圆的直径是半径的2倍\",\"C\":\"圆是轴对称图形\",\"D\":\"圆有4条对称轴\"}",
  "answer": "A,B,C",
  "difficulty": "INTERMEDIATE",
  "score": 0,
  "explanation": "...",
  "order": 2
}
```

### TRUE_FALSE（判断题）

- `options`: 固定为 `"{}"`
- `answer`: `"T"`（正确）或 `"F"`（错误）

```json
{
  "id": "cmrtak3di00073xfvv2uym13e",
  "type": "TRUE_FALSE",
  "content": "同一个圆内，所有的半径都相等。（ ）",
  "options": "{}",
  "answer": "T",
  "difficulty": "BASIC",
  "score": 0,
  "explanation": "在同一个圆中，所有半径长度都相等。",
  "order": 1
}
```

## 难度等级

| 值 | 中文 | 典型场景 |
|----|------|----------|
| `BASIC` | 基础 | 直接记忆、基本概念 |
| `INTERMEDIATE` | 中等 | 简单应用、理解推理 |
| `ADVANCED` | 较难 | 综合应用、多步推理 |
| `EXPANDED` | 拓展 | 跨知识、开放性 |

## 关键注意事项

1. **options 是 JSON 字符串**: 必须是序列化后的字符串（`"{\"A\":\"...\"}"`)，不是对象
2. **id 格式**: 使用 `cm` 开头的 25 位 CUID2 风格字符串
3. **answer 格式**: 判断题的 T/F 是大写；多选答案逗号分隔、按字母序排列
4. **score 为 0**: 课堂作业模式下 score 常设为 0，由系统另行计分
5. **空题目检测**: questions 数组中不应有空 content 的条目

## 文件命名规范

QuickClass 导入时通过文件名解析元信息，格式为:
`{teacher}_{grade}_{subject}_{taskTitle}_课堂作业_{quizTitle}.json`

示例: `脸盆_三年级下学期_数学_圆的认识_课堂作业_圆的练习题.json`

> AI生成