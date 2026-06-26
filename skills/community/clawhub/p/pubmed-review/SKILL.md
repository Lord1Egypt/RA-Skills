---
name: pubmed-review
description: 飞书自然语言触发的 PubMed 文献检索与 AI 综述生成系统。支持专业检索式扩展、限定词过滤、AI 结构化综述（brief+full）、飞书通知、追问回答。
---

# PubMed Review Skill

## Skill 说明

当用户在飞书发送 PubMed 相关检索需求时，本 skill 自动完成：

1. 意图识别（pubmed_review vs other）
2. 检索词提取 + 标准化 + OR/AND 扩展
3. PubMed E-utilities 文献检索
4. AI 综述生成（brief + full）
5. 飞书推送 brief
6. 本地存储 full 综述
7. 追问回答（基于 PMID 上下文）

## 所需环境变量

| 变量名 | 必须 | 说明 |
|--------|------|------|
| `MINIMAX_API_KEY` | ✅ | MiniMax API Key |
| `MINIMAX_API_URL` | 否 | 默认为 `https://api.minimax.chat/v1/text/chatcompletion_v2` |
| `MINIMAX_MODEL` | 否 | 默认为 `MiniMax-M2.7-highspeed` |
| `NOTIFY_PATH` | 否 | 飞书 notify 脚本路径，默认为 `which notify` |
| `MINIMAX_ENV_FILE` | 否 | 环境变量文件路径，默认为 `./.env.minimax` |

## 调用方式

### 通过 OpenClaw 飞书（推荐）

用户在飞书向 OpenClaw 发送自然语言消息，系统自动触发 `pubmed_intent_handler.py`。

### 直接命令行

```bash
# 创建任务
python3 scripts/add_pubmed_task.py "瘢痕激光" [max_articles]

# 触发检索（通过调度器）
python3 scripts/task_dispatcher.py

# 直接运行检索
python3 scripts/run_pubmed_review.py <task_id>

# 生成综述
bash scripts/run_pubmed_summary.sh <articles_json> <task_id>

# 追问回答
python3 scripts/pubmed_followup_handler.py "<用户追问>"
```

## 任务队列

任务存储在 `tasks/ablesci_tasks.json`（pubmed_review 类型任务也在此队列）。

字段规范：
```json
{
  "id": "pubmed_<timestamp>_<random>",
  "type": "pubmed_review",
  "status": "pending|running|completed|failed",
  "created_at": "2026-04-10 12:00:00",
  "payload": {
    "topic": "瘢痕激光",
    "max_articles": 10,
    "search_term": "(scar OR keloid...) AND (laser...) AND last 5 years[dp] AND review[pt]"
  }
}
```

## 输出结构

### 飞书通知（brief）

```
📋 PubMed 文献综述完成

主题：acne isotretinoin
摘要提取：10 篇
综述文件：./results/pubmed/pubmed_xxx_summary.md

[brief 正文，约200字，多行显示]
```

### 本地文件（full）

路径：`results/pubmed/{task_id}_summary.md`

格式：Markdown，含完整综述正文 + 参考文献列表

### 追问回复

```
📖 综述追问回复

[LLM 回答内容，含 PMID 和文献标题]
```

## 检索式扩展规则

### OR 扩展（同义词组）

| 主题词 | 扩展 |
|--------|------|
| `scar` | `(scar OR keloid OR hypertrophic scar)` |
| `laser` | `(laser OR fractional laser OR pulsed dye laser OR PDL OR CO2 laser)` |
| `infantile hemangioma` | `(infantile hemangioma OR hemangioma)` |

### 限定词叠加优先级

- 时间：最近5年 > 最近10年（互斥，取最高优先级）
- 文献类型：系统评价 > meta分析 > 综述（互斥）
- 人群：儿童 + 成人同时出现时跳过（不添加过滤）
- 研究类型：随机对照 > 临床研究（仅在无其他过滤时使用）

## 追问上下文绑定

优先级（4层 fallback）：
1. 消息中显式包含 `task_id: pubmed_xxx` → 精确绑定
2. 当前有活跃追踪的综述任务 → 复用
3. 从关键词匹配最近完成的任务 → 模糊匹配
4. 无任何匹配时追加提示，要求用户提供 task_id

## 错误处理

| 错误类型 | 处理方式 |
|---------|---------|
| MiniMax API 失败 | 降级为结构化摘要（来自 articles.json 摘要字段） |
| PubMed 检索失败 | 任务标记为 failed，飞书通知 |
| Cookie 失效 | 暂停监控，飞书告警 |
| LLM JSON 解析失败 | 自动规范化换行符后重试 |

## 发布信息

- 版本：v2.2.7-beta
- 依赖：Python 3.8+, PubMed E-utilities（免费）, MiniMax API
- 许可证：MIT
