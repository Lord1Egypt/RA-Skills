---
name: va-claims-assistant
description: "Research and guide VA disability claims for U.S. military veterans. Use when a veteran asks about: VA disability ratings, filing or increasing a claim, nexus letters, buddy statements, DBQs (Disability Benefits Questionnaires), PACT Act eligibility, toxic exposure benefits, VA buddy statements, C&P exam preparation, supplemental claims, appeals (HLR/BVA), combined rating calculations, or any VA benefits question. Covers the full claims lifecycle from initial filing through Board of Veterans Appeals."
---

# VA Claims Assistant

Guide veterans through the VA disability claims process from initial filing through appeals.

## Quick Reference

**Rating calculator:** See `references/rating-math.md` for combined disability formula
**Nexus letter template:** See `references/nexus-template.md`
**Common conditions:** See `references/conditions.md` for service connection guidance

## Core Workflow

### 1. Assess the Veteran's Situation
Ask (or infer from context):
- Branch of service, dates of service, discharge status
- Current claimed conditions and their severity
- Existing rating (if any) and target rating
- Key events: PACT Act exposure, MST, TBI, hazardous duty

### 2. Calculate / Estimate Combined Rating
Use `scripts/va_rating_calc.py` — NOT simple addition. VA uses "whole person" method:
```bash
python3 scripts/va_rating_calc.py 70 30 20 10
```
Always round to nearest 10 for final rating display.

### 3. Research Service Connection
Each condition needs:
- **In-service event** (exposure, incident, MOS)
- **Current diagnosis** (medical records)
- **Nexus** (medical opinion linking service to condition)

PACT Act (2022): expands presumptive conditions for burn pit, Agent Orange, radiation exposure — no nexus letter required for presumptives. See `references/conditions.md`.

### 4. Documents Checklist
- DD-214 (discharge document)
- STRs (Service Treatment Records) — request via MyHealtheVet or NPRC
- Private medical records + buddy statements
- DBQ completed by private doctor (stronger than VA examiner)
- Nexus letter (if not presumptive)

### 5. Filing Strategy
- **New claim:** VA.gov > File a VA disability claim (21-526EZ)
- **Increase:** Same form, select "increase in disability"
- **Supplemental:** New evidence required
- **HLR (Higher Level Review):** Same evidence, fresh review
- **BVA Appeal:** Board of Veterans Appeals — use if HLR denied

### 6. C&P Exam Prep
Tell veteran: Show up. Describe worst day, not best day. Don't minimize symptoms.
Checklist: See `references/cp-exam-prep.md` for condition-specific prep.

## Key Rules
- Always calculate combined rating with the script — never add percentages
- PACT Act presumptives skip nexus requirement (just need diagnosis + exposure)
- 100% P&T (Permanent and Total) = CHAMPVA for dependents + property tax exemptions
- TDIU: Can get 100% pay at 60%+ single / 70%+ combined with one at 40%+
- SMC (Special Monthly Compensation): additional pay for loss of use, Aid & Attendance
