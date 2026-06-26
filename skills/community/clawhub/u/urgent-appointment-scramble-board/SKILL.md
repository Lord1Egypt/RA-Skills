---
name: Urgent Appointment Scramble Board
description: Track urgent appointment calls across multiple providers with a live availability board, call log, openings, callbacks, and confirmation details.
version: 1.1.0
type: prompt-flow
author: Bell (design)
tags: [appointment-scheduling, urgency-management, waitlist-optimization, healthcare]
---

# Urgent Appointment Scramble Board

## Overview

Urgent Appointment Scramble Board helps a user who needs the soonest available appointment and is calling multiple places under time pressure. It creates a live availability board with target list, call script, call log, openings, callback status, rank order, and confirmation checklist.

This skill is logistics-only. It does not provide medical, legal, financial, immigration, or professional advice. It does not decide whether a situation is safe to wait for an appointment. If the user describes immediate danger, severe symptoms, threats, deadlines with legal consequences, or any emergency, direct them to emergency services or the appropriate licensed professional channel first.

## When to Use

Use this skill when the user says things like:

- "I need the soonest appointment and keep calling places."
- "Help me track who has openings today or tomorrow."
- "I am waiting on callbacks and losing track."
- "I need a script for asking about cancellations."
- "Which appointment slot should I take based on availability and logistics?"

This can apply to many scheduling contexts, such as clinics, repair visits, government offices, school meetings, passport offices, salons, consultations, or service appointments. Keep advice limited to scheduling logistics.

## Workflow

### Step 1 - List Targets

Build a target list before calling.

Capture:

- Provider or office name
- Phone number or contact method
- Location or service area
- Hours
- Reason for appointment in user-approved wording
- Required person, specialist, service, or department
- Distance or travel time
- Priority level
- Backup notes

If the user has no target list, help them create categories to search manually, but do not claim live availability unless the user provides it.

### Step 2 - Prepare a Short Call Script

Create a concise script the user can read or adapt:

```text
Hi, I am trying to schedule the soonest available appointment for [reason/service].
Do you have any openings today, tomorrow, or this week?
Can you check cancellations or a waitlist?
If nothing is available, when is the earliest slot and what is the best time to call back?
What details do I need to confirm before booking?
```

Add optional questions:

- Is there a cancellation list?
- Can I be notified by phone, text, email, or portal?
- Are there multiple locations with earlier openings?
- Are virtual, standby, same-day, or after-hours slots available?
- What documents, forms, payment, referral, ID, insurance, or account details are required?
- What is the cancellation or late-arrival policy?

### Step 3 - Call and Log Slots

For each call, log:

- Call time
- Person or department reached
- Earliest available slot
- Other openings
- Waitlist or cancellation option
- Callback promised and expected time
- Required documents or prerequisites
- Fees, deposits, or policies to confirm
- Hold time or best call-back time
- Outcome: booked, callback, no answer, closed, not eligible, not available
- Notes

If the user leaves voicemail, record the exact time and callback instructions.

### Step 4 - Rank Openings

Rank available slots using logistics criteria, not professional judgment about the underlying issue.

Suggested ranking factors:

- Earliest time
- Required travel time
- Ability to attend without conflict
- Required documents can be ready in time
- Cancellation or reschedule flexibility
- Cost or deposit clarity
- Provider/location preference stated by the user
- Callback reliability
- Risk of losing the slot while waiting

Ask the user to define the tie-breaker if needed: earliest time, preferred provider, shortest travel, lowest cost, or easiest paperwork.

### Step 5 - Confirm Details

Before the user treats a slot as secured, provide a confirmation checklist:

- Date and time
- Time zone, if relevant
- Location, room, phone, or meeting link
- Provider, department, or service type
- Arrival time and late policy
- Required documents, ID, forms, referral, payment, insurance, or account information
- Fees, deposits, cancellation terms, and refund policy
- How confirmation will arrive
- Callback or waitlist status
- What to do if a better slot opens

### Step 6 - Maintain the Live Board

Update the board after every call:

- Move booked or strongest options to the top
- Keep callbacks visible
- Mark dead ends clearly
- Preserve phone numbers and names for follow-up
- Add next call time for offices that suggested calling back

Do not overload the user. Under pressure, one visible board is better than perfect data.

## Output Format

Produce a live scramble board:

```text
Urgent Appointment Scramble Board

Goal:
- Appointment/service needed:
- Latest acceptable time:
- User tie-breaker:
- Constraints:

Call Script:
- Short script:
- Questions to ask:

Target List:
| Priority | Provider/Office | Phone/Contact | Location | Hours | Notes |

Live Availability Board:
| Rank | Provider | Earliest Slot | Location/Mode | Prerequisites | Fees/Policy | Status | Callback Time | Notes |

Call Log:
| Time | Provider | Person Reached | Outcome | Slots Offered | Waitlist | Next Action |

Best Current Options:
1. Best slot:
2. Backup slot:
3. Callback to watch:

Confirmation Checklist:
- Date/time confirmed
- Location/mode confirmed
- Required documents/forms confirmed
- Fees/deposit/cancellation policy confirmed
- Arrival or login instructions confirmed
- Confirmation message received or requested
```

## Safety Boundaries

- Logistics-only: do not provide medical, legal, financial, immigration, or other professional advice.
- Do not tell the user it is safe to wait for an appointment when immediate professional help may be needed.
- If the user describes emergency symptoms, danger, threats, legal deadlines, or immediate harm, direct them to emergency services or the relevant professional authority.
- Do not book, cancel, pay, submit forms, share personal data, or contact providers for the user unless the user explicitly requests a separate reviewed external action.
- Do not claim live availability unless the user has provided it from calls, websites, or messages.
- Remind the user to confirm fees, eligibility, required documents, and cancellation policies before relying on a slot.

## Acceptance Criteria

1. The response creates a target list and call script before call logging begins.
2. The live board tracks earliest slots, callback status, prerequisites, fees/policies, and next actions.
3. Available openings are ranked by logistics criteria and user tie-breakers.
4. A confirmation checklist is included before treating a slot as secured.
5. The skill remains logistics-only and avoids medical/legal/professional advice.
6. Emergencies or immediate danger are escalated to emergency services or appropriate professional channels.

## Example Prompts

Copy and paste one of these into your AI assistant with your details filled in:

1. **Scrambling for a medical appointment:** "I need the soonest dermatologist appointment this week. I have called four offices. Two have no openings this month, one has a slot next Tuesday but it conflicts with work, and one put me on a callback list and said to call back tomorrow at 8 AM. Help me track all this on a live board so I don't lose any openings."

2. **Tracking service appointment calls:** "My car needs a state inspection and the deadline is Friday. I called three shops. One has Thursday at 2 PM, one said check back tomorrow for cancellations, and one didn't answer. The Thursday slot is 40 minutes away. Build me a scramble board and help me decide whether to book the Thursday slot or keep calling."

3. **Multiple callbacks incoming:** "I left callback requests with a passport office, a visa center, and a photographer for urgent travel documents. Each one said they'll call in 24-48 hours but I'm losing track of who said what. Build a board with expected callback windows and a follow-up script so I don't miss anything."


## Usage Scenarios

### Scenario 1

**User Input:** "I need a dermatologist appointment within 3 days for a suspicious mole. Here are 5 clinics I can go to."

**Expected Output:** Ranked priority list by cancellation-history likelihood, distance, and insurance acceptance. Generates call scripts for each clinic's front desk.

### Scenario 2

**User Input:** "Monitor the patient portals for these 3 clinics and alert me if a slot opens before Friday."

**Expected Output:** Sets monitoring check cadence. When a slot opens, sends an urgency alert with the time, provider, and a one-tap booking link.

### Scenario 3

**User Input:** "I got an 8 AM slot tomorrow. Build my pre-visit packet: insurance card, symptom timeline, previous biopsy report."

**Expected Output:** Assembles a single PDF with: visit summary cover sheet, photo of insurance card, 1-page symptom timeline, and embedded prior medical record references.


### Scenario 4: 挂不上三甲医院的号怎么办
**User input:** "牙疼得不行，但上海三甲医院的号全满了，最早的也要两周后。有没有办法捡漏或加号？"
**Expected output:** 三甲医院挂号攻略——第一步：每天早上7点/下午5点击点刷新（退号集中释放时间），用医院官方App/公众号刷新比第三方平台快；第二步：挂同科室的普通门诊或专病门诊（比专家号好挂，医生是同一批轮转），到现场再请医生转诊同一个专家；第三步：急诊通道（有明显疼痛/发烧/出血的可以直接去急诊，三甲急诊24小时开放但排队2-4小时）；第四步：上海市级医院可互认，查附近二甲/区中心医院（比如同济医院挂不到挂普陀区中心医院）；第五步：黄牛渠道（谨慎使用，费用300-1000不等，有风险但确实管用）。关键：正规渠道优先，急诊兜底。

## Example

**User says:** "I need the soonest appointment this week and have called five offices. Two did not answer, one has next Friday, and one might call me back today."

**Skill output:** Builds a scramble board with each office, logs no-answer and callback status, ranks next Friday against any pending callback, prepares a short follow-up script, and lists confirmation details to verify before accepting a slot.
