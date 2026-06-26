---
name: same-day-document-drop-plan
description: "Create a same-day document drop plan with timing, routing, recipient confirmation, proof-of-delivery checklist, copy handling, and fallback steps. Use for urgent paperwork delivery while protecting originals, identity documents, and sensitive records."
---
# Same-Day Document Drop Plan

## Purpose

Help the user plan an urgent same-day document drop-off with clear logistics, recipient confirmation, proof of delivery, and careful handling of originals or identity documents. The goal is to reduce missed deadlines, wrong-door deliveries, and lost paperwork.

This is a prompt-only logistics and proof checklist. It is not legal, immigration, court, tax, medical, employment, banking, courier, or identity-verification advice, and it does not guarantee acceptance by the recipient.

## Use This Skill When

Use this skill when the user needs to deliver documents today or very soon, such as:

- Forms, applications, signed paperwork, school documents, employer documents, lease packets, claim packets, permit materials, or administrative records.
- Court, agency, consulate, clinic, school, bank, office, landlord, insurance, or service-provider drop-offs.
- Originals, notarized copies, ID documents, passports, birth certificates, titles, certificates, checks, or records that need careful handling.
- A route plan, checklist, proof-of-delivery plan, or fallback plan before closing time.

Do not use this skill to advise on legal sufficiency, court filing rules, immigration strategy, tax filings, medical decisions, or identity verification requirements beyond checking with the official recipient.

## Best Inputs

Ask for only what is needed. If details are missing, proceed with placeholders and a concise follow-up list.

- Recipient organization, department, person, address, suite, entrance, drop box location, phone number, email, and hours.
- Deadline, closing time, last accepted drop time, appointment or queue requirements, and security check details.
- Document list, whether each item is original, copy, notarized, signed, sealed, confidential, or replaceable.
- Required envelopes, labels, cover sheet, case number, account number, application number, return address, or attention line.
- Transportation mode, route constraints, parking, building access, elevator or front desk rules, and backup options.
- Proof needed: date-stamped copy, receipt, signature, photo of sealed envelope, tracking number, email confirmation, or staff name.

## Workflow

1. **Confirm the real recipient.** Capture the exact office, department, address, suite, entrance, drop box, attention line, and contact channel. Flag anything that must be verified by phone, official site, or the recipient.
2. **Check the time window.** Record deadline, business hours, last accepted drop time, appointment rules, security line risk, travel time, parking, and buffer.
3. **Inventory documents.** List each document and mark original, copy, signed, notarized, sealed, confidential, replaceable, or irreplaceable.
4. **Protect originals and identity documents.** Recommend carrying only what is required, using a folder or envelope, keeping copies when allowed, not leaving originals unless required, and asking for a receipt when originals are surrendered.
5. **Prepare the packet.** Build the cover sheet, label, order of documents, copy set, envelope notes, and redaction notes if a full number is not required.
6. **Plan proof of delivery.** Decide what proof the user should request or capture: stamped copy, receipt, staff name, confirmation email, drop-box photo where allowed, or courier tracking.
7. **Build the route.** Create a time-blocked route from departure to arrival, security, drop-off, proof capture, and exit, with a latest-leave time.
8. **Add fallback steps.** Include what to do if the office is closed, the address is wrong, the drop box is unavailable, staff refuse intake, an original is requested unexpectedly, or the user misses the cutoff.
9. **Create a post-drop log.** Record who accepted it, when, proof kept, documents surrendered, and follow-up timing.

## Output Format

Return the drop plan in this order:

1. **Drop Mission Snapshot**

| Field | Detail |
|---|---|
| Recipient | |
| Address and suite | |
| Department or attention line | |
| Deadline or cutoff | |
| Latest leave time | |
| Documents included | |
| Proof needed | |

2. **Recipient and Hours Verification**

| Item to verify | Current answer | How to verify | Risk if wrong |
|---|---|---|---|

3. **Document Inventory**

| Document | Original or copy | Status | Handling note | Copy kept? |
|---|---|---|---|---|

4. **Packet Prep Checklist**

| Step | Done? | Notes |
|---|---|---|

5. **Time-Blocked Route Plan**

| Time | Action | Buffer or risk note |
|---|---|---|

6. **Proof-of-Delivery Checklist**

| Proof type | How to get it | Backup proof | Privacy note |
|---|---|---|---|

7. **Fallback Plan**

| Problem | Immediate action | Who to contact | Evidence to keep |
|---|---|---|---|

8. **Post-Drop Log**

| Date/time | Person or location | Documents delivered | Proof kept | Follow-up needed |
|---|---|---|---|---|

9. **Open Questions**

A short list of missing facts that could affect timing, acceptance, or proof.

## Message Style

- Be calm, practical, and deadline-aware.
- Highlight verification items and last-safe departure time.
- Treat originals and identity documents as high-risk items.
- Avoid overexplaining; give the user an executable checklist.
- Separate logistics from legal or official acceptance questions.

## Safety Boundary

- This skill creates a logistics and proof checklist only; it does not determine legal sufficiency, filing validity, immigration status, tax compliance, medical requirements, or official acceptance.
- Verify recipient address, hours, intake method, deadline, and required originals with the official recipient before relying on the plan.
- Handle originals, passports, IDs, birth certificates, titles, notarized documents, sealed records, checks, and identity documents carefully. Carry only what is required, keep copies when allowed, and request a receipt if surrendering originals.
- Do not include full payment numbers, full account numbers, full tax IDs, passwords, one-time codes, or unnecessary personal data in packet summaries.
- Do not recommend leaving sensitive originals unattended, photographing restricted areas, bypassing security, forging signatures, altering dates, or misrepresenting delivery time.
- If the drop involves court, immigration, regulated filing, legal deadline, medical records, or high-value originals, advise confirming requirements with the recipient or a qualified professional.

## Example Prompts

Copy and paste one of these to get started:

- "I need to drop a signed lease renewal at the management office before 5pm today. Build my same-day document drop plan with routing, proof, and fallback steps."
- "Court filing deadline is at 4pm. I have originals and notarized copies. Make a drop plan with time-blocked route, proof of delivery, and a backup if the clerk's office closes early."
- "Help me deliver a claim packet to insurance today — I need a document inventory, route plan, proof checklist, and fallback if the drop box is unavailable."
