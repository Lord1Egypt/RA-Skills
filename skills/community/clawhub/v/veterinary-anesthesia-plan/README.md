# Veterinary Anesthesia Plan

**Platforms:** Claude · Openclaw · Codex
**Domain:** Veterinary — Anesthesia

## Purpose

An anesthesia-planning partner for licensed veterinary teams. Turns patient signalment, today's measured weight, ASA Physical Status, the planned procedure, current medications, and comorbidities into a structured DRAFT anesthesia plan organized around premedication, induction, maintenance, analgesia, fluids, monitoring, recovery, and emergency drugs, with weight-based dose ranges, contraindication flags, and a required-equipment checklist.

## When to Use

- Building an anesthesia plan for a scheduled or emergency procedure (dental, soft-tissue surgery, orthopedic, imaging under sedation, endoscopy, emergency stabilization)
- Standardizing protocol modifications for sighthounds, brachycephalics, MDR1 breeds, pediatric / geriatric, pregnant, cardiac, renal, hepatic, diabetic, or seizure-disordered patients
- Pre-calculating emergency drugs to the patient's weight before induction
- Producing a monitoring and recovery plan aligned to AAHA Anesthesia & Monitoring Guidelines and ACVAA Monitoring Guidelines
- Teaching veterinary students and interns the structure of a complete anesthesia plan

## What It Does

**Phase 1: Intake**
1. Captures practice context, formulary basis, and available monitoring level
2. Captures signalment, today's measured body weight, BCS / MCS, hydration, mentation
3. Captures procedure, duration, expected pain level, positioning, fasting status
4. Captures history, current medications, allergies, prior anesthetic events, pre-anesthetic diagnostics, and proposed ASA Physical Status
5. Restates every fact with Confirmed / Assumed / Unknown tags and lists the modification flag each comorbidity triggers

**Phase 2: Drafting**
6. Builds Protocol Modifications table tied to breed, conformation, life stage, and comorbidity
7. Drafts premedication, induction, and maintenance with range (mg/kg), proposed value, route, total mg, volume at named concentration, indication, contraindication flags, and source
8. Drafts a multimodal analgesia plan including intra-op opioids, regional / local blocks, NSAID candidacy, and post-op rescue
9. Drafts a fluid plan, monitoring plan with cadence and intervention triggers, and a recovery plan

**Phase 3: Safety scaffolding**
10. Builds a patient-specific Emergency Drug Worksheet with pre-calculated doses
11. Builds an Equipment Checklist for the induction room
12. Produces an Evidence Matrix, Unresolved-Questions list, and a sign-off block for the attending veterinarian

## Output

A DRAFT anesthesia plan with:

- Patient summary, ASA rationale, and protocol-modification table
- Premedication, induction, maintenance, and analgesia tables with weight-based doses
- Fluid plan
- Monitoring plan with cadence and intervention triggers
- Recovery plan with extubation, PACU, and discharge criteria
- Patient-specific Emergency Drug Worksheet
- Equipment checklist
- Evidence matrix and unresolved-questions list
- Sign-off block for the attending veterinarian

## Safety

This skill drafts a recommendation, **not** an order. Every output is labeled **DRAFT — LICENSED VETERINARIAN MUST REVIEW AND SIGN BEFORE ADMINISTRATION**. The skill never selects a final drug or dose, never administers anesthesia, never overrides veterinarian judgment, and never extrapolates doses across species without disclosure. Cats are not small dogs. Day-of measured weight is required before any dose is finalized; otherwise every dose is flagged **PENDING DAY-OF WEIGHT — RECALCULATE**. Sighthound, brachycephalic, MDR1-breed, pediatric, geriatric, pregnant, cardiac, renal, hepatic, diabetic, seizure, obesity, cachexia, anemia, and GI-obstruction risks each trigger a dedicated flag and modification note. All patient data is treated as confidential and is never pasted to external services.

## Feedback & Contributions

Found a gap or have a suggestion? [Open an issue or PR](https://github.com/archlab-space/Open-Skill-Hub/issues) — improvements are welcome.
