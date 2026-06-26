# Step 09 — Permissions & Escalation

## Goal
Define what the agent can decide alone vs. what requires a human.
A well-calibrated permission matrix prevents both over-escalation (annoying) and under-escalation (risky).

---

## The 4-Level Permission Model

| Level | Name | Agent Behavior | Human Role |
|-------|------|---------------|-----------|
| L0 | Auto-Handle | Responds immediately, no human involvement | None |
| L1 | Suggest + Confirm | Agent proposes action, employee approves with one tap | Click to confirm |
| L2 | Submit for Approval | Agent creates ticket/request, waits for human decision | Review and decide |
| L3 | Force Escalate | Agent immediately hands off to human, stays on standby | Take over |

---

## Default Permission Matrix by Role

### 🛍️ Shopping Guide
| Action Type | Default Level | Rationale |
|-------------|--------------|-----------|
| Product info / FAQ | L0 | Safe, factual |
| Stock availability | L0 | Safe, factual |
| Promotion calculation | L0 | Safe, factual |
| Product recommendation | L0 | Safe, no commitment |
| Complaint (routine) | L0 → L1 | Agent handles first, escalates if unresolved |
| Complaint (aggressive) | L3 | Immediate handoff |
| Refund request | L2 | Money involved, needs human |
| Price negotiation | L2 | Policy exception, needs human |

### 📦 Stock Manager
| Action Type | Default Level |
|-------------|--------------|
| Stock query | L0 |
| Low-stock alert | L0 (auto-notify) |
| Reorder suggestion | L1 (manager confirms) |
| Reorder execution | L2 (manager approves) |
| Inventory adjustment | L2 |

### 🎧 Customer Service Rep
| Action Type | Default Level | Notes |
|-------------|--------------|-------|
| Policy query | L0 | |
| Returns guidance | L0 | Tells customer the process |
| Refund < ¥200 | L1 | Staff confirms |
| Refund ¥200–¥2000 | L2 | Manager approves |
| Refund > ¥2000 | L3 | Immediate manager |
| Exchange request | L1 | |
| Legal/media threat | L3 | Immediate |
| Repeat complaint (3+) | L3 | |

---

## Escalation Configuration

### Escalation Targets
Define who receives escalations by level and time:

```json
{
  "escalation_targets": {
    "L1": {
      "primary": { "type": "wecom", "id": "staff_wecom_group_id" },
      "fallback": null
    },
    "L2": {
      "primary": { "type": "wecom", "id": "manager_wecom_id" },
      "fallback": { "type": "sms", "number": "+86138..." }
    },
    "L3": {
      "primary": { "type": "wecom", "id": "manager_wecom_id" },
      "fallback": { "type": "sms", "number": "+86138..." },
      "response_sla_minutes": 5
    }
  }
}
```

### On-Call Schedule
For stores with different contacts during/after business hours:

```json
{
  "schedule": {
    "business_hours": { "weekdays": "09:00-21:00", "weekends": "10:00-22:00" },
    "on_hours_contact": "manager_wecom_id",
    "off_hours_contact": "duty_manager_phone",
    "off_hours_method": "sms"
  }
}
```

### Escalation Message Template
When escalating, the agent sends context to the human:

```
🔔 [L2 升级] 客服需要您处理

顾客情况：[顾客描述的问题摘要]
对话时间：[timestamp]
建议处理：[agent's recommendation]
对话链接：[link to conversation]

请在 30 分钟内处理。
```

---

## Auto-Escalation Triggers

Define keyword triggers for immediate L3 escalation:

```json
{
  "auto_escalate_l3_keywords": [
    "律师", "法院", "起诉", "消协", "曝光", "媒体", "投诉到",
    "骗子", "假货", "黑心", "太难听的话 [filtered]"
  ],
  "auto_escalate_l2_keywords": [
    "退款", "换货", "质量问题", "坏了", "破损", "发票"
  ],
  "sentiment_threshold": -0.7
}
```

---

## Guardrails — What the Agent Will Never Do

Regardless of permissions, the agent must never:
- Promise a refund amount without human approval
- Commit to a delivery date or availability that isn't confirmed
- Share other customers' information
- Make up a policy that doesn't exist in the knowledge base
- Negotiate price unilaterally
- Claim to be a human if sincerely asked

Configure these as hard constraints in `guardrails_config`.

---

## Output Format

```json
{
  "permissions_matrix": {
    "product_query": "L0",
    "inventory_query": "L0",
    "promotion_calc": "L0",
    "recommendation": "L0",
    "complaint_routine": "L1",
    "complaint_aggressive": "L3",
    "refund_small": "L1",
    "refund_large": "L2",
    "exchange": "L1",
    "legal_threat": "L3"
  },
  "escalation_targets": { ... },
  "schedule": { ... },
  "auto_escalate_keywords": { ... },
  "guardrails": {
    "never_promise_refund": true,
    "never_fabricate_policy": true,
    "disclose_ai_if_asked": true
  }
}
```

Save as `permissions_config` in agent memory. Proceed to Step 10.
