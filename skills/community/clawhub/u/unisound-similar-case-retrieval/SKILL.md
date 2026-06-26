---
name: med-doctor-similar-case-retrieval
description: 医生端临床科研 — 相似病例语义检索与可解释排序，锚点病例对候选池做类比推理辅助。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔬"
      }
  }
---

# 相似病例检索（科研辅助）

## 概述

面向**临床科研与教学**的「锚点病例 → 候选病例池」语义对齐能力：在用户提供的一组已脱敏摘要或结构化要点上，由内部医疗大模型完成**类比排序、相似维度拆解与科研启发式提示**。

> 本实现**不接真实院内病历库**，候选病例须由调用方预先准备（导出队列、公开数据集子集、或文献病例摘要）。价值在于统一走公司内部医疗大模型，便于与后续真实检索管线对接时替换为向量召回 + 重排。

## 业界脉络（写法参考，非功能承诺）

近年医疗 AI 文献中常见的组合范式包括：**病例基推理（Case-based Reasoning）**与 **RAG / GraphRAG** 并用，在 EHR 长程结构数据上保留时间轴与合并症模式再做相似患者检索；也有工作将「指南证据检索」与「相似患者 exemplar」双通道融合以提升可解释性。本 skill 在接口层预留 `anchor_case` / `candidate_cases` 字段，语义上对齐上述「患者级类比」叙事，当前阶段以 **LLM 重排与解释** 为主。

## OpenClaw 中的角色

- **输入**：锚点病例自然语言摘要 + 多条候选病例（每条含 `id` 与 `summary`）。
- **输出**：统一 JSON（`data` 为结构化回显与轻量统计，`text` 为 Markdown 级排序解读与科研注意点）。

## 快速开始

```bash
python3 scripts/run.py --input input.json --output output.json --appkey YOUR_KEY
```

## 输入字段（JSON）

| 字段 | 必填 | 说明 |
| --- | --- | --- |
| `anchor_case` | 是 | 锚点病例摘要（主诉、关键体征、诊断线索、时间轴等） |
| `candidate_cases` | 是 | 数组，元素含 `id`、`summary` |
| `top_k` | 否 | 期望在解读中重点讨论的靠前条数，默认 `5` |
| `task_hint` | 否 | 科研关注点，如「预后分层」「用药方案对照」 |

## 输出约定

与仓库内其他 LLM skill 一致：

```json
{
  "skill": "相似病例检索",
  "status": "ok",
  "data": { },
  "text": "Markdown 解读"
}
```

## 参数

- `--input PATH`：**必填**。UTF-8 JSON 文件路径。
- `--output PATH`：可选。落盘路径；省略则打印到 stdout。
- `--appkey STRING`：**必填**。调用内部医疗大模型的鉴权 key，由平台分配。

## 模型配置

- endpoint：`https://maas-api.hivoice.cn/v1/chat/completions`
- model：`u1-insuremed`
- 鉴权：`Bearer {appkey}`

## 医疗与合规边界

输出仅供科研、教学或方法学讨论参考，**不构成诊疗建议**；使用真实患者数据前须完成脱敏与伦理审批。
