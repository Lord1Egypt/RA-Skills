# Step 11 — Launch & Handoff

## Goal
Activate the agent on all configured channels, generate a staff onboarding card,
and schedule the first improvement review.

---

## Launch Checklist

Before activating, confirm all are green:

- [ ] Knowledge base score ≥ 80 (Step 06)
- [ ] Pre-launch test score ≥ 80 (Step 10)
- [ ] At least one channel connected (Step 08)
- [ ] Escalation contacts configured (Step 09)
- [ ] Persona saved and previewed (Step 07)

If any item is red, return to the relevant step. Do not activate with critical gaps.

---

## Activation Steps

1. **Flip the agent live** — set `agent_status: "active"` in config
2. **Send welcome message** to each connected channel:

   *WeCom (staff channel):*
   > 👋 大家好！我是[名字]，你们的新数字同事，今天正式上岗了！
   > 有任何产品、库存、政策问题，直接问我就好。我24小时在线，秒回。
   > 有问题找不到我，也可以直接 @[名字] 。一起加油！🚀

   *WeChat MP / Kiosk (customer-facing):*
   > 您好！我是[门店名]的[名字]，有什么可以帮到您？😊

3. **Set first check-in cron job** — 7 days from today:
   > "7天使用回顾：查看未回答问题清单，检查知识库是否有新缺口"

4. **Record go-live timestamp** in agent memory

---

## Staff Onboarding Card (One-Pager)

Generate a compact guide for human employees. Format as a printable card or WeCom message.

```
╔══════════════════════════════════════════════╗
║  认识你的新同事：[名字] 🏪                      ║
╠══════════════════════════════════════════════╣
║                                              ║
║  TA 能做什么？                                ║
║  ✅ 回答顾客产品问题      ✅ 查库存             ║
║  ✅ 解释活动优惠          ✅ 处理常见投诉        ║
║                                              ║
║  TA 不能做什么？                              ║
║  ❌ 代表你承诺退款        ❌ 修改订单           ║
║  ❌ 开具发票              ❌ 拍板价格例外        ║
║                                              ║
║  当 TA 找你时：                               ║
║  📲 收到升级通知 → 5分钟内响应               ║
║  ✅ 点确认 = 同意TA的建议                    ║
║  ✏️ 回复内容 = 告诉TA怎么处理               ║
║                                              ║
║  发现 TA 答错了？                             ║
║  直接回复："[名字]，这个不对，正确答案是..."  ║
║  TA 会学习并记住。                            ║
║                                              ║
║  紧急情况：                                   ║
║  联系 [店长名] [联系方式]                     ║
╚══════════════════════════════════════════════╝
```

---

## Manager Configuration Summary

Generate a one-page config summary for the store owner / area manager:

```
数字员工配置摘要 — [门店名]
上线日期：[date]

角色：[role_name]
技能：[list of active skills]
渠道：[list of channels]
知识库：[X] 个商品 | [Y] 条政策 | [Z] 条FAQ
测试评分：[score]/100

升级路由：
  L1/L2 → [contact name]（[wecom/phone]）
  L3    → [contact name]（[phone]，5分钟SLA）
  非工作时间 → [contact name]（[phone]，短信通知）

下次检查：[date + 7 days]
更新知识库：直接对话发送文件或文字即可
```

---

## Post-Launch Schedule

| Time | Action | Trigger |
|------|--------|---------|
| Day 7 | First check-in | Cron job |
| Day 30 | Monthly usage report | Cron job |
| Day 90 | Persona + skills review | Cron job |
| Ongoing | Unknown-query digest | Weekly cron |
| Ongoing | Knowledge gap alerts | Real-time threshold |

All cron jobs are configured in Step 12.

---

## Rollback Plan

If something goes wrong after launch:

1. Set `agent_status: "maintenance"` — agent auto-replies "系统维护中，请联系人工客服"
2. All channels still receive the fallback message
3. Escalation contacts are notified of maintenance mode
4. Fix the issue, re-run affected tests, then re-activate

Keep the rollback command visible:
> "暂停数字员工" → enters maintenance mode immediately
