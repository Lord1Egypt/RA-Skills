# Summary output contract (v0.3 — decision-ready brief)

> Close session 时 `_build_summary.py` 产两份文件到 session folder：
> - **`summary.md`** — LLM-synthesized **决策-ready 6 节预读**，这是 Responder 要读的
> - **`summary_audit.md`** — 4 柱分组的 audit trail，给想 dig 细节的人

---

## `summary.md`（主产物）六节结构

Responder 读完 ≤ 5 分钟可进入会议。挑刺者视角——不软化 dissent，不隐藏 open items。

```
# 会前简报 — <subject>

_Requester: <name> (<open_id>) · Rounds: N · 产出时间: <ts>_

## 1. 议题摘要
  一句话（20-40 字）+ 三行背景（why now / what's at stake / where it stands）

## 2. 核心数据
  材料里的关键数字，带来源+日期；无来源的明确标「未给出来源」作为风险信号

## 3. 团队自检结果
  - Findings 被挑战了几条
  - Requester 响应的分布：接受并修改 / 保留异议 / 无解
  - Agent 对响应质量的判断：强 / 中 / 弱 / 对抗性，带具体理由

## 4. 待决策事项
  - 主 ask（一句话，Responder 被要求做什么决定）
  - 需要讨论的开放项 ≤ 3 条，带 A/B 判断框架

## 5. 建议时间分配
  每议题建议时长 + 原因。若材料未达 decision-ready，可建议「不开」或「改短会对齐」

## 6. 风险提示（Agent 认为团队可能遗漏或低估的点）
  从六维度 + Responder 模拟综合，≤3 条
  每条标出维度（逻辑自洽性 / 数据完整性 / 方案可行性 / 利益相关方 / 风险评估 / ROI 清晰度）
  + Agent 建议 Responder 开会时具体追问什么（Socratic）
```

## `summary_audit.md`（审计产物）

4 柱分组的 raw 数据视图，deterministic 从 annotations.jsonl 聚合，不经 LLM：

- 四柱状态表（pass / fail / unresolvable）
- 最终材料清单
- 已接受 findings（按柱分组）
- Requester 修改版本
- 保留异议（按柱分组，含 reviewer 建议 + requester 理由）
- 未闭合进入讨论
- Responder 模拟追问（按 priority 排序）
- 关闭时仍未解决的（若 force-close）

## Delivery targets 推荐

在 `delivery_targets.json` 里：

```json
{
  "on_close": [
    {
      "name": "responder-lark-dm",
      "backend": "lark_dm",
      "open_id": "{{RESPONDER_OPEN_ID}}",
      "payload": ["summary", "final"],     // 主脑：决策 brief + 定稿材料
      "role": "responder"
    },
    {
      "name": "requester-lark-dm",
      "backend": "lark_dm",
      "open_id": "{{REQUESTER_OPEN_ID}}",
      "payload": ["summary"],               // 只给他 brief（他已知细节）
      "role": "requester"
    },
    {
      "name": "archive-local",
      "backend": "local_path",
      "path": "...",
      "payload": ["summary", "summary_audit", "final", "conversation", "annotations", "dissent"]
    }
  ]
}
```

`summary` 给决策人读；`summary_audit` 只进本地归档，不默认投给 Lark。
