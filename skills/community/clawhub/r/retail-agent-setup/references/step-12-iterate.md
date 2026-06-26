# Step 12 — Continuous Improvement

## Goal
Set up automated feedback loops so the agent gets smarter over time without requiring
manual intervention. The system should surface what to fix; the user decides when to act.

---

## The 3 Feedback Loops

### Loop 1: Weekly Unknown-Query Digest
**What:** Collects all questions the agent couldn't answer (score = 0) over the past 7 days
**When:** Every Monday 09:00 (or configured time)
**Delivered to:** Manager via WeCom or configured channel
**Action required:** User reviews digest, uploads or pastes missing knowledge

**Digest format:**
```
📋 本周知识库缺口报告（[日期区间]）

共 [N] 个问题未能回答。最常见的：

1. "你们有没有XX款式？" (问了 8 次) — 需要更新产品目录
2. "可以分期付款吗？" (问了 5 次) — 需要添加支付政策
3. "这个商品有质检报告吗？" (问了 3 次) — 需要上传资质文件

👉 回复这条消息发送文件或文字即可更新知识库。
```

**Cron config:**
```json
{
  "job": "weekly_unknown_digest",
  "schedule": { "kind": "cron", "expr": "0 9 * * MON", "tz": "Asia/Shanghai" },
  "payload": { "kind": "systemEvent", "text": "Run weekly unknown-query digest for retail agent" }
}
```

---

### Loop 2: Monthly Performance Report
**What:** Aggregates usage metrics over the past 30 days
**When:** 1st of each month at 09:00
**Delivered to:** Manager via WeCom
**Action required:** Review trends; decide whether to tune skills or adjust persona

**Report format:**
```
📊 [门店名] 数字员工月报（[月份]）

📈 核心指标：
  总对话数：1,248
  成功回答率：87%（目标 80%）✅
  升级率：3.2%（目标 < 5%）✅
  平均响应时间：< 1秒

🔥 最常被问的 Top 10：
  1. 库存查询（328次）
  2. 退货政策（201次）
  3. 促销活动（187次）
  ...

⚠️ 需要关注：
  - "分期付款"被问了47次，知识库仍无答案
  - 周六 14:00-16:00 升级率偏高（建议：检查当班人员配置）

📅 下月建议优先完善：
  1. 添加支付/分期政策
  2. 新季商品导入知识库
```

**Cron config:**
```json
{
  "job": "monthly_performance_report",
  "schedule": { "kind": "cron", "expr": "0 9 1 * *", "tz": "Asia/Shanghai" },
  "payload": { "kind": "systemEvent", "text": "Generate monthly retail agent performance report" }
}
```

---

### Loop 3: Real-Time Knowledge Gap Alerts
**What:** Fires immediately when the same question goes unanswered 3+ times in a rolling 24-hour window
**When:** Real-time, triggered by threshold breach
**Delivered to:** Manager via WeCom
**Action required:** Immediate: add the missing knowledge

**Alert format:**
```
🚨 知识库警报

过去24小时内，有顾客问了 [N] 次以下问题，但我没有答案：
"[question text]"

请尽快补充相关信息，回复这条消息即可更新。
```

**Config:**
```json
{
  "gap_alert": {
    "enabled": true,
    "threshold": 3,
    "window_hours": 24,
    "delivery_channel": "wecom",
    "recipient": "manager_wecom_id"
  }
}
```

---

## Scheduled Knowledge Base Review

Every 90 days, trigger a full knowledge base review:

**Checklist:**
- [ ] Are all promotions still current? (remove expired ones)
- [ ] Are all product prices still accurate?
- [ ] Are there new products to add?
- [ ] Has the return/exchange policy changed?
- [ ] Are store hours still correct?
- [ ] Do staff escalation contacts still apply?

**Trigger message to manager:**
> "📅 季度知识库检查提醒：距上次全面更新已过90天，建议花15分钟检查一下产品和政策信息是否需要更新。回复"开始检查"我来引导你。"

---

## Self-Improvement from Corrections

When a staff member corrects the agent:
> "小慧，这个不对，正确答案是XX"

The agent should:
1. Acknowledge the correction
2. Update the relevant knowledge base entry
3. Log the correction with timestamp and source
4. Confirm: "已记录！下次遇到这个问题我会用正确的答案了。"

---

## Cron Job Summary

| Job | Frequency | Purpose |
|-----|-----------|---------|
| `weekly_unknown_digest` | Weekly Monday | Surface unanswered questions |
| `monthly_report` | Monthly 1st | Usage metrics + trends |
| `quarterly_kb_review` | Every 90 days | Staleness check |
| `gap_alert` | Real-time | Urgent knowledge gaps |

All jobs are created as OpenClaw cron jobs during Step 12 setup.
Show the user the list of created jobs and confirm they're active before completing onboarding.

---

## Onboarding Complete 🎉

When all 12 steps are done, show the completion summary:

```
╔══════════════════════════════════════════════╗
║  🎉 [名字] 正式上线！                          ║
╠══════════════════════════════════════════════╣
║  角色：[role]                                 ║
║  知识库：[score]/100                          ║
║  上线测试：[score]/100                         ║
║  活跃渠道：[N] 个                             ║
║  监控任务：[N] 个已启动                        ║
╠══════════════════════════════════════════════╣
║  下次检查：[date+7]                           ║
║  需要调整？直接告诉我：                        ║
║  "更新知识库" / "修改人设" / "添加渠道"        ║
╚══════════════════════════════════════════════╝
```

Set `retail_setup_state.completed` = true in agent memory.
