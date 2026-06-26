# Annotation Schema — pillar-based (v0.2)

> 当前版本（2026-04-21 起）：以 `pillar` 为 first-class 分类。旧 `axis`（7-axis）字段只在 backward-compat 时保留，final-gate 和 summary 会自动映射。

One JSON object per line in `sessions/<id>/annotations.jsonl`.

## 当前 schema (v0.2)

```jsonc
{
  "id": "p1" | "r1" | "m1",   // p=four_pillar_scan, r=responder_simulation, m=manual
  "round": 1,
  "created_at": "2026-04-21T...",

  "source": "four_pillar_scan" | "responder_simulation" | "manual",

  "pillar": "Background" | "Materials" | "Framework" | "Intent",
  "severity": "BLOCKER" | "IMPROVEMENT" | "NICE-TO-HAVE",

  "anchor": {
    "source": "normalized.md" | "conversation.jsonl" | "responder_simulation",
    "section": "optional",
    "line_range": [3, 5],
    "text_hash": "sha256:...",
    "snippet": "原文片段 ≤120 字"
  },

  "issue": "简述问题（一句话）",
  "suggest": "具体建议，动词开头，含替换文本",

  "simulated_question": "(only when source=responder_simulation) 模拟的 Responder 原话",
  "priority": 1,  // responder_simulation 的优先级 (1 最要紧)

  "status": "open" | "accepted" | "rejected" | "modified" | "unresolvable",
  "reply": "Requester 的回应文本（rejected 必填）",
  "replied_at": "...",
  "unresolvable_reason": "(only for unresolvable) 为什么闭合不了",
  "extra": {
    "framing_a": "若 Responder 倾向 A 则...",
    "framing_b": "若 Responder 倾向 B 则..."
  },
  "escalated_to_open_items": false
}
```

## 四柱定义

| Pillar | 含义 | 典型问题 |
|---|---|---|
| **Background** | 背景 / 为什么现在 / 当前状态 / 项目锚点 | "为什么换 Tavily，现在遇到了什么问题" |
| **Materials** | 数据 / 证据 / 来源 / 定价 / 对比 / 实测 | "准确率的 benchmark 来源是什么" |
| **Framework** | 讨论变量 / 决策维度 / 判断类型 | "你想让 Responder 按 cost 还是 speed 选" |
| **Intent** | 单一 ask / 具体决策 / Responder 下一步动作 | "你希望 Responder 做的决定是批准 Exa 吗" |

## 生成来源（source）

| source | 谁写的 | 特点 |
|---|---|---|
| `four_pillar_scan` | scan.py Layer A | LLM 按四柱系统扫描，确定性高，覆盖基线 |
| `responder_simulation` | scan.py Layer B | LLM 扮演 Responder 本人提问，风格/priority 来自 profile |
| `manual` | Admin 人工 | 需要特殊标注时使用 |

## Status lifecycle

```
open ─┬─> accepted       (Requester 同意，会改)
      ├─> rejected       (Requester 不同意 → dissent.md)
      ├─> modified       (Requester 提出自己的改法)
      └─> unresolvable   (无信息可补，进 open_items)
```

闭合后重开需要新 id（不 reuse）。

## Dissent log rule

任何 `status: "rejected"` 的条目，在 status 变化的瞬间自动 append 到 `sessions/<id>/dissent.md`（附 reviewer 建议 + Requester 的拒绝理由）。summary 从 `dissent.md` 取，不直接 scan annotations。

## Cursor

Agent emit finding 时按 cursor 顺序：

```jsonc
{
  "current_id": "p1",                  // 当前正在对话的 finding
  "pending": ["p3", "r1", "p5", ...],  // 排队（BLOCKER 优先，IMPROVEMENT 次之）
  "done": ["p2"]                        // 已处理完（任何 terminal status）
}
```

Requester 可以跳条："skip to r2" / "先谈 p5" → agent 更新 cursor。

## 对话形式发出

annotations.jsonl 是批量产出，但 emit 给 Requester 时**一条一条发**。每条 IM 只发一个 finding + 等回复。

## Backward compat（legacy v0.1）

旧 annotations（有 `axis` 字段、无 `pillar`）会被 final-gate.py / _build_summary.py 按以下 map 自动转换：

| Legacy axis | Mapped pillar |
|---|---|
| BLUF | Intent |
| Decision Readiness | Intent |
| Completeness | Framework |
| Assumptions | Materials |
| Evidence | Materials |
| Red Team | Materials |
| Stakeholder | Materials |

Legacy 7-axis 详细定义见 `axes_decision_brief_reference.md`（已归档）。

## Alternate annotation backends (v1)

若 boss 在 profile 里 set `annotation_mode: lark-doc`：
- JSONL 保留（audit 用）
- 用户可见层变成 Lark Doc inline comments（Lark Open API `/open-apis/docx/v1/documents/:doc_id/comments`）
- Status mapping:
  - `accepted`/`modified` → comment resolved
  - `rejected` → comment marked resolved+dissent tag 保留可见
  - `open` → comment active

v0 不实现。
