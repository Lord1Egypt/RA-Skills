---
name: workers-comp-claim-intake
description: >
  Use this skill when an HR manager, safety officer, employer representative, or workers'
  compensation coordinator needs to document a workplace injury or illness claim. Covers
  OSHA recordability determination (29 CFR 1904), state-specific First Report of Injury
  (FROI) data requirements, filing deadline flags, and incident investigation documentation.
  Produces a DRAFT FROI and incident investigation report for HR and safety officer review
  before any submission.
---

# Workers' Comp Claim Intake

Document workplace injury and illness claims accurately and completely — from initial incident facts through OSHA recordability determination, state FROI data collection, and incident investigation — to meet carrier, regulatory, and employer reporting obligations.

## Flow

### Phase 1 — Incident Identification

Ask one question at a time:
1. Employer name and Federal Employer Identification Number (FEIN) — or indicate "drafting only" to proceed without sensitive identifiers
2. Worksite state (determines WC jurisdiction, FROI form, and filing deadline)
3. Date and time of the injury or illness
4. Date the employer first learned of the injury or illness
5. Injured worker's job title and department (use a pseudonym or "Worker A" if privacy requires)
6. Employment type: full-time employee / part-time employee / temporary employee / contractor

Flag: if the injured worker is a contractor, add a note that WC compensability depends on employment classification, which varies by state, and recommend legal review before filing.

### Phase 2 — Incident Description

Collect the following as a narrative, prompting for each element:
- What task or activity was the worker performing immediately before the incident?
- What event or exposure caused the injury or illness?
- Nature of the injury or illness (e.g., sprain, laceration, fracture, burn, repetitive-motion condition)
- Body part affected
- Single traumatic event or repeated / cumulative exposure?
- Names and contact information for any witnesses (note: mark witness data as sensitive; exclude from any public-facing document)

### Phase 3 — OSHA Recordability Determination

Walk the 29 CFR 1904 recordability analysis step by step:

**Step 1 — Work-relatedness (§ 1904.5)**
Is the case work-related? Apply the work-environment presumption: an injury or illness is work-related if an event or exposure in the work environment caused or contributed to it, or significantly aggravated a pre-existing condition.
Ask for any facts relevant to the seven § 1904.5(b)(2) exceptions (e.g., personal task, off-premises commute, entirely personal cause).

**Step 2 — New case (§ 1904.6)**
Is this a new case, or a recurrence of a previously recorded case?
A new case requires a new record. A recurrence of a previously recorded case updates the existing record.

**Step 3 — General recording criteria (§ 1904.7)**
Did the case involve any of the following?
- Medical treatment beyond first aid
- Days away from work
- Restricted work or job transfer
- Loss of consciousness
- Diagnosis of a significant injury or illness by a licensed healthcare professional
- Cancer, chronic irreversible disease, fractured or cracked bone, or punctured eardrum

Output: **OSHA Recordable — Yes / No / Indeterminate (information needed)**

If Recordable: Flag for OSHA 300 Log entry, OSHA 301 Incident Report, and OSHA 300A Annual Summary.
If Indeterminate: List the specific missing facts required to complete the determination. Flag for safety officer review.

### Phase 4 — Medical Treatment and Work Status

Ask for:
1. Level of medical treatment: first aid only / urgent care / emergency room / primary care physician / hospital admission
2. Name and address of treating facility or physician
3. Diagnosis (if available at intake)
4. Work restrictions imposed: none / light duty / restricted work / days away from work
5. Estimated return-to-work date (if provided by the treating provider)
6. Has the worker been directed to an Authorized Treating Physician (ATP) under the employer's WC managed care plan?

### Phase 5 — State FROI Requirements

Based on the worksite state from Phase 1, surface state-specific requirements:

For the identified state, note:
- FROI form name and number (e.g., California DWC-1, New York C-2F, Texas DWC Form-1, Florida DWC-1, Illinois 45-Day Report)
- Filing deadline from date of employer knowledge of the claim (most states: 5–10 calendar days)
- Carrier notification deadline (often shorter than the state FROI deadline)
- Any electronic filing mandate
- State-specific data fields beyond the standard FROI

**Compute the filing deadline date** based on the employer-knowledge date from Phase 1.

**URGENT flag**: If the filing deadline is within 3 calendar days of today, display a prominent URGENT notice before drafting.

State coverage note: Workers' compensation is state-regulated. Confirm state-specific requirements with your WC carrier, TPA, or state workers' compensation board before filing. This skill provides general FROI data structure and deadline guidance, not legal advice.

### Phase 6 — Incident Investigation Documentation

Draft the incident investigation section:

**Immediate cause**: The direct unsafe act or unsafe condition that caused the injury.
**Root cause**: Why the unsafe act or condition existed. Use the 5-Why technique: ask "Why?" up to five times to reach the systemic cause.
**Contributing factors**: Training gap / equipment failure / supervision deficiency / process design / environmental condition / time pressure.
**Corrective actions**: For each contributing factor, define:
  - Corrective action description
  - Type: Immediate containment / Short-term fix / Long-term prevention
  - Responsible party (title or department placeholder)
  - Target completion date

### Phase 7 — DRAFT Assembly

Produce two DRAFT documents:

---

**DOCUMENT 1 — DRAFT First Report of Injury**

Structured to the worksite state's FROI data fields identified in Phase 5.

Mark all sensitive fields at the top: "[SENSITIVE — SSN, DOB, and detailed medical diagnosis must be entered by the authorized HR representative. Do not include in email or unsecured documents.]"

Include: employer information, incident date and description, body part and nature of injury, medical treatment level, work status, insurer/carrier information (placeholder if unknown), and filing deadline reminder.

---

**DOCUMENT 2 — DRAFT Incident Investigation Report**

Sections:
1. Incident Summary
2. OSHA Recordability Determination with rationale
3. Medical Treatment and Work Status Summary
4. Immediate and Root Cause Analysis (with 5-Why chain)
5. Contributing Factors
6. Corrective Action Plan (with owners and due dates)
7. Safety Officer and HR Review Block

Add this block to both documents:

```
DRAFT — AUTHORIZED EMPLOYER USE ONLY
Safety Officer Review: _____________________ Date: ________
HR Review: ________________________________ Date: ________

These documents contain confidential employee health information.
Handle in accordance with applicable privacy law, HIPAA where applicable,
and company document retention policy. Do not transmit via unsecured channels.
```

## Key Rules

- **No legal or medical decisions**: OSHA recordability and WC compensability are employer and carrier determinations. This skill produces documentation to support those decisions — it does not make them.
- **State law variation**: Workers' compensation is state-regulated. Always surface state-specific deadline and form requirements and direct the user to confirm with their WC carrier or state board before filing.
- **Sensitive data**: Workers' comp claims contain protected health information. Never include SSNs, full dates of birth, or detailed medical records in illustrative examples. Remind the user to store all documents securely and transmit only via authorized channels.
- **Contractor flag**: If the injured worker is a contractor, immediately flag the classification question and recommend legal review.
- **One question at a time**: Do not present multi-part intake forms; ask for each data item individually.
- **Deadline urgency**: If the carrier or state FROI deadline is within 3 calendar days, surface an URGENT flag before beginning Phase 5 drafting.
- **No filing**: This skill drafts documents. The authorized employer representative must review, complete sensitive fields, and file with the carrier and state board.

## Output Format

Two DRAFT documents:
1. **DRAFT FROI** — state-structured first report of injury with all required data fields, sensitive-field flags, and the filing deadline date
2. **DRAFT Incident Investigation Report** — OSHA recordability determination with rationale, 5-Why root cause chain, contributing factors, corrective action plan with owners and due dates, and safety officer / HR review block

## Feedback

If you encounter a state-specific FROI form, self-insured employer workflow, or WC system requirement this skill doesn't handle, share it at https://github.com/archlab-space/Open-Skill-Hub/issues.
