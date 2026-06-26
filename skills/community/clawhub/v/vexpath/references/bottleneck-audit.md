# Bottleneck Audit Reference

## Overview

The bottleneck audit identifies where a business is losing time, money, or clients due to broken or missing systems. Run at onboarding or whenever a client says "things feel chaotic."

---

## Diagnostic Questionnaire

Ask all 15 questions. Score each answer. Total score maps to priority recommendations.

---

### Section A: Lead & Intake (Questions 1–4)

**Q1. How do new leads contact you?**
- Multiple channels with no single intake point → +3
- One form or method, but you check it inconsistently → +2
- One method, checked daily → +1
- Automated intake with instant routing → 0

**Q2. How long does it typically take you to respond to a new inquiry?**
- More than 24 hours → +3
- Same day, but inconsistent → +2
- Within 4 hours reliably → +1
- Automated acknowledgment + human reply within 2 hours → 0

**Q3. Do you have a standard process for qualifying leads before spending time on them?**
- No — I respond to everyone the same way → +3
- I do it mentally but it's not written down → +2
- Yes, informal checklist → +1
- Yes, documented and automated → 0

**Q4. How do you track leads who don't convert immediately?**
- I don't — if they don't reply, I forget them → +3
- I try to follow up but it's inconsistent → +2
- I have a list or sheet I check sometimes → +1
- Follow-up is automated with reminders → 0

---

### Section B: Communication & Follow-Up (Questions 5–7)

**Q5. How do you follow up with clients during a project?**
- Client has to ask me for updates → +3
- I send updates when I remember → +2
- I have a schedule but it's manual → +1
- Automated milestone updates → 0

**Q6. Do clients ever go silent mid-project and you're not sure why?**
- Yes, regularly → +3
- Occasionally → +2
- Rarely → +1
- Never — I have a re-engagement trigger → 0

**Q7. How do you handle requests that come in outside business hours?**
- Nothing happens until I see it → +3
- Auto-reply but no routing → +2
- Auto-reply with triage → +1
- Automated routing and priority flagging → 0

---

### Section C: Operations & Delivery (Questions 8–11)

**Q8. How do you onboard a new client?**
- Informally — I figure it out each time → +3
- I have a checklist in my head → +2
- I have a checklist but it's not templated → +1
- Documented, automated onboarding workflow → 0

**Q9. How much time do you spend each week on tasks you could describe as "admin"?**
- More than 10 hours → +3
- 5–10 hours → +2
- 2–5 hours → +1
- Under 2 hours → 0

**Q10. Do you ever miss deadlines, appointments, or deliverables?**
- Yes, more than once a month → +3
- Occasionally (1–2 times a quarter) → +2
- Rarely, and usually external factors → +1
- Never — reminders and scheduling are automated → 0

**Q11. How do you handle recurring tasks (monthly reports, invoice sends, check-ins)?**
- Manually, from memory → +3
- Calendar reminders, but still manual → +2
- Template-based, partially automated → +1
- Fully automated with tracking → 0

---

### Section D: Revenue & Billing (Questions 12–13)

**Q12. How are invoices sent and tracked?**
- Manually, as I remember → +3
- Scheduled but not tracked → +2
- Sent on time, tracked in a sheet → +1
- Automated invoice + payment tracking + overdue reminders → 0

**Q13. Do you have a process to request reviews or referrals after project completion?**
- No → +3
- I ask sometimes but not consistently → +2
- I have a template, send manually → +1
- Automated post-project review sequence → 0

---

### Section E: Tools & Systems (Questions 14–15)

**Q14. How many different tools do you use that don't talk to each other?**
- 5+ disconnected tools → +3
- 3–4 with some manual bridge → +2
- 2–3, mostly connected → +1
- Integrated stack with minimal manual overlap → 0

**Q15. How do you currently use AI or automation in your business?**
- Not at all → +3
- Tried it but nothing stuck → +2
- Using 1–2 tools casually → +1
- Systematic AI and automation integrated into operations → 0

---

## Scoring

| Total Score | Assessment |
|-------------|------------|
| 0–10 | **Optimized** — Fine-tune and document; focus on growth systems |
| 11–20 | **Moderate Friction** — 2–4 systems need repair; prioritize lead + comms |
| 21–30 | **High Friction** — Significant manual overhead; start with intake + follow-up |
| 31–45 | **Operational Chaos** — Immediate intervention needed; start with triage + scheduling |

---

## Bottleneck Score Map

After scoring, identify the top-scoring sections:

| Section | Score > 8 | Recommended First Fix |
|---------|-----------|----------------------|
| A (Lead & Intake) | Leads leaking | Build: Lead intake form + auto-response + CRM entry |
| B (Communication) | Client churn risk | Build: Follow-up system + project update sequence |
| C (Operations) | Time drain | Build: Onboarding workflow + recurring task automation |
| D (Revenue) | Revenue leakage | Build: Invoice automation + review request sequence |
| E (Tools) | System debt | Build: Tool integration audit + consolidation plan |

---

## Audit Report Format

```
VEXPATH BOTTLENECK AUDIT
─────────────────────────────
Business: [name]
Date: [date]
Auditor: VEX

TOTAL SCORE: [X] / 45
ASSESSMENT: [Optimized / Moderate Friction / High Friction / Operational Chaos]

TOP BOTTLENECKS:
  1. [Section]: Score [X/12] — [one-sentence description of the problem]
  2. [Section]: Score [X/12] — [description]
  3. [Section]: Score [X/12] — [description]

IMMEDIATE PRIORITIES:
  Priority 1: [System to build] — [expected impact]
  Priority 2: [System to build] — [expected impact]
  Priority 3: [System to build] — [expected impact]

QUICK WINS (can implement this week):
  - [action]
  - [action]
  - [action]

RECOMMENDED WORKFLOW TEMPLATES:
  See references/workflow-templates.md — [profile] templates

ESTIMATED TIME SAVINGS:
  [X] hours/week once Priority 1 and 2 are implemented

NEXT STEPS:
  1. [action]
  2. [action]
  3. [action]
```

---

## Recommendation Engine

### Lead intake score ≥ 8
→ Build: Lead intake workflow
→ Template: See `workflow-templates.md` → [business type] → Lead Capture

### Communication score ≥ 8
→ Build: Follow-up system
→ Template: `follow-up.md` + `workflow-templates.md` → Follow-Up

### Operations score ≥ 8
→ Build: Onboarding workflow + recurring task automation
→ Template: `workflow-templates.md` → [business type] → Onboarding

### Revenue score ≥ 6
→ Build: Invoice automation + review request
→ Template: `workflow-templates.md` → Invoice + Review Request

### Tools score ≥ 6
→ Run: Tool audit — list all tools, map overlaps, identify consolidation or integration opportunities
→ Recommend: Zapier/Make/n8n for bridging disconnected tools
