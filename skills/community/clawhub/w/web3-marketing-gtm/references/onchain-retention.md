# On-Chain Retention Strategy & User Segmentation

## Purpose
Design a retention system rooted in on-chain behavior — not social follows or Discord roles. The goal is to bring users back to the product through actions that happen on-chain, triggered by real usage signals.

---

## Core Principle

Web3 retention is different from Web2 retention.

- Web2: email open rates, push notifications, login streaks
- Web3: wallet activity, transaction recency, on-chain streaks, asset holding behavior

This skill produces retention strategies that use **on-chain data as the signal** and **on-chain or community rewards as the response**.

---

## Step 1: User Segmentation

Segment all users into 4 tiers based on on-chain behavior. Adapt criteria to product type.

### Tier Definitions

| Tier        | Label          | Criteria                                                                     | Size (typical) |
|-------------|----------------|------------------------------------------------------------------------------|----------------|
| Tier 1      | Core Users     | ≥3 transactions OR ≥2 return visits in last 30 days                         | 5–15% of wallets |
| Tier 2      | Active Users   | 1–2 transactions in last 30 days                                             | 20–30%         |
| Tier 3      | Dormant Users  | Connected wallet but 0 transactions in last 14 days                         | 30–40%         |
| Tier 4      | One-And-Done   | Exactly 1 transaction, no return in 7+ days                                 | 20–35%         |

### Segment Triggers by Product Type

**DeFi:**
- Core: Wallet has open positions or recurring deposits
- Dormant: Withdrew all liquidity in last 14 days
- One-and-done: Swapped once, no further activity

**GameFi:**
- Core: Played ≥3 sessions or ≥5 matches in last 7 days
- Dormant: No game activity in 10+ days
- One-and-done: Completed tutorial, never played a real match

**Payments/Infra:**
- Core: ≥2 API calls or on-chain payment requests per week
- Dormant: Integrated but 0 requests in 14 days
- One-and-done: Sent one test transaction, no follow-up

**Oracle/Data:**
- Core: Active subscription or ≥5 queries in last 7 days
- Dormant: Subscription lapsed or no queries in 14 days
- One-and-done: Made 1–2 queries during free trial, did not convert

---

## Step 2: Retention Loop Design

Design a loop for each tier. Each loop has: **Trigger → Response → Outcome**.

### Tier 1 (Core Users) — Deepen Engagement

Goal: Make power users feel recognized and give them more to do.

| Trigger                         | Response                                         | Outcome                          |
|---------------------------------|--------------------------------------------------|----------------------------------|
| Reaches [N] transactions        | Unlock exclusive Discord role or badge           | Identity + social proof          |
| Uses [feature X] 3+ times       | Surface advanced feature or beta access          | Increases product surface explored |
| Refers another wallet           | On-chain acknowledgment or points credit         | Viral loop activation            |
| Holds asset/subscription ≥30d   | Loyalty reward or reduced fee                    | Reduces churn for paying users   |

### Tier 2 (Active Users) — Increase Frequency

Goal: Move from occasional to habitual.

| Trigger                         | Response                                         | Outcome                          |
|---------------------------------|--------------------------------------------------|----------------------------------|
| 7 days since last transaction   | Discord DM / Telegram message: "Here's what's new" | Re-engagement without pressure  |
| Used 1 feature only             | Tutorial or in-app prompt for second feature     | Feature discovery                |
| Completed onboarding            | Weekly digest of relevant on-chain data for them | Personalized value delivery      |

### Tier 3 (Dormant Users) — Re-Activate

Goal: One specific reason to return.

| Trigger                         | Response                                         | Outcome                          |
|---------------------------------|--------------------------------------------------|----------------------------------|
| 14 days no activity             | "Here's what changed since you left" post (X or Discord) | Low-friction return path       |
| New feature shipped             | Targeted Telegram message to dormant segment     | Feature as re-entry point        |
| Ecosystem event on their chain  | Contextual callout: "This affects your wallet"   | Urgency without spam             |

### Tier 4 (One-And-Done) — Convert or Accept Churn

Goal: One clear CTA to return. If no response after 2 attempts, stop messaging.

| Trigger                         | Response                                         | Outcome                          |
|---------------------------------|--------------------------------------------------|----------------------------------|
| 7 days post-first-tx, no return | Single re-engagement post: "Did something go wrong?" | Honest, non-pushy recovery     |
| 14 days post-first-tx           | "Here's a 2-minute walkthrough" (tutorial link) | Reduce friction as churn cause   |
| 21+ days, no response           | No further outreach. Tag as churned.             | Preserve community quality       |

---

## Step 3: Retention Content Calendar

Produce a repeating weekly retention content schedule. This runs in parallel with the main campaign calendar.

| Cadence     | Content                                                    | Channel          |
|-------------|------------------------------------------------------------|------------------|
| Every Monday | "Week in review" — on-chain stats from last 7 days        | Discord + X      |
| Every Wednesday | Feature spotlight or tutorial for Tier 2 users        | Discord          |
| Every Friday | Core user highlight or milestone recognition             | Discord + X      |
| Bi-weekly   | Re-engagement message to Tier 3 (Dormant) segment         | Telegram         |
| Monthly     | Retention health report (internal — not published)        | Internal doc     |

---

## Step 4: Retention KPIs

Track these metrics weekly. Do not rely on social metrics (likes, follows) as retention signals.

| KPI                        | Definition                                              | Target (30-day)            |
|----------------------------|---------------------------------------------------------|----------------------------|
| D7 Retention               | % of Day-0 wallets that transact again by Day 7         | >25%                       |
| D30 Retention              | % of Day-0 wallets that transact again by Day 30        | >15%                       |
| Avg transactions/wallet    | Mean txns per connected wallet over 30 days             | >2 (adjust by product)     |
| Churn rate                 | % of Tier 2 users moving to Tier 3 each week            | <20%                       |
| Re-activation rate         | % of Tier 3 users who return after retention message    | >10%                       |

---

## Step 5: Retention Message Copy Templates

Use these for re-engagement outreach. Keep all messages factual and non-pushy.

### Template R1 — 7-Day Dormant (Discord/Telegram)
```
Hey — it's been a week since you connected to [Project Name].

Here's what's new: [1–2 specific updates or improvements]

If something didn't work, reply here. We'd rather fix it than lose you.

→ [Link]
```

### Template R2 — 14-Day Dormant (Telegram)
```
[Project Name] update — [specific feature or data point].

Worth a second look: [link]
```

### Template R3 — Milestone Unlock (Discord)
```
You just hit [milestone — e.g. "10 transactions on NodusAI"].

You're now one of [X] wallets that's reached that mark.

[Specific reward or recognition — role, shoutout, or early access].
```

### Template R4 — Re-engagement Post (X — targets lapsed users passively)
```
If you tried [Project Name] a few weeks ago and stepped away:

[Specific thing that changed or improved].

Still free to [action]. Still on [chain].

→ [Link]
```

---

## Chain-Specific Notes

| Chain      | Retention Consideration                                                     |
|------------|-----------------------------------------------------------------------------|
| Avalanche  | Subnets can create isolated user bases — track by subnet if applicable      |
| Base       | High new-user volume; D7 retention especially important to track            |
| Solana     | Fast finality = higher tx frequency expected; raise "active" threshold      |
| Ethereum   | Gas costs reduce casual usage; 1 tx/month may = "active" for some products |
| Polygon    | Low fees = easy one-and-done; require 3+ txns for "active" classification  |
