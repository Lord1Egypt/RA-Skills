# SAR Narrative Drafter

**Platforms:** Claude · Openclaw · Codex
**Domain:** AML / BSA — Suspicious Activity Reports

## Purpose

A SAR-narrative drafting partner for BSA officers, AML investigators, transaction-monitoring analysts, and financial-intelligence-unit (FIU) staff at U.S. financial institutions filing under 31 C.F.R. Chapter X. Turns the case file (alerts, investigation notes, account history, transaction summary, subject information, red-flag triggers) into a DRAFT FinCEN SAR Part V narrative structured as **Introduction → Body → Conclusion**, covering **Who / What / When / Where / Why / How**, with FinCEN-keyword tagging, FFIEC SAR-quality self-check, and a BSA-officer review block.

## When to Use

- Drafting the Part V narrative for a SAR before submission via FinCEN BSA E-Filing
- Rewriting a weak existing narrative flagged in QA, internal audit, or examiner review
- Tagging FinCEN advisories (FIN-2026-… keywords) in the narrative as required by current FinCEN guidance
- Drafting a 90-day continuing-activity SAR narrative that references the prior SAR by BSA ID and incremental new facts
- Standardizing narrative structure across investigators to satisfy the FFIEC BSA/AML Examination Manual SAR-quality expectations

## What It Does

**Phase 1: Case intake**
1. Captures filer institution type (bank, MSB, broker-dealer, casino, MSB-virtual-currency, fintech with FinCEN-registered partner, other), filer ID / RSSD, point of contact
2. Captures subject(s) — individual / entity / both — with internal identifiers (not full SSN / EIN in working notes)
3. Captures account(s) — number (last 4 in narrative, full in structured Part III), product, opening date, signers
4. Captures the activity window (start / end), aggregate dollar amount, transaction count, and instrument mix
5. Captures the red-flag triggers (alert ID, scenario, monitoring rule), investigation steps taken, and dispositioning rationale
6. Captures whether this is **initial**, **continuing-activity** (linked to prior BSA ID), **joint**, or **corrected** filing

**Phase 2: 5 W's + H mapping**
7. Maps each fact to **Who / What / When / Where / Why / How**, flagging any missing dimension as **Unknown — required for narrative**
8. Identifies applicable FinCEN advisories / keywords (e.g., FIN-2026-…, elder-financial-exploitation, human-trafficking, healthcare-fraud, cyber-event, virtual-currency)

**Phase 3: Drafting**
9. Drafts the Introduction (filer, subject, activity, total dollars, period)
10. Drafts the Body (chronological method of operation with specific dates, amounts, counterparties, instruments, jurisdictions)
11. Drafts the Conclusion (institution's response — account closure / restriction / continuing monitoring; law-enforcement contact; document retention)
12. Tags FinCEN keywords and cross-references prior BSA IDs for continuing activity
13. Runs the FFIEC SAR-quality self-check and the weak-language audit

## Output

A DRAFT narrative packet with:

- Part V narrative (Introduction → Body → Conclusion)
- FinCEN keyword tag list (for Field 2 and inline narrative reference)
- 5 W's + H coverage matrix
- FFIEC quality self-check
- Weak-language audit (flags "may indicate", "could be consistent with", etc.)
- Prior-SAR cross-reference list (for continuing-activity filings)
- Document-retention block (where supporting docs live; 5-year retention noted)
- BSA-officer review and sign-off block
- Unresolved-information list

## Safety

This skill drafts a narrative, **not** a filing. Every output is labeled **DRAFT — BSA OFFICER MUST REVIEW BEFORE FINCEN BSA E-FILING SUBMISSION**. The skill never submits a SAR, never accesses FinCEN BSA E-Filing, never communicates with law enforcement, and never discloses the SAR's existence to the subject (31 U.S.C. § 5318(g)(2)). The skill enforces the **30-day** SAR filing deadline from initial detection (60 days where no suspect is identified) and flags any case past or near the deadline. PII is minimized in drafts (last-4 of account, no full SSN / EIN inline); the structured FinCEN SAR fields hold the full identifiers, not the narrative. SAR confidentiality is absolute — the narrative, the existence of the SAR, and the underlying investigation may not be shared outside the institution's authorized personnel and law-enforcement-with-jurisdiction. Continuing-activity SARs reference prior BSA IDs and incremental new activity only.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
