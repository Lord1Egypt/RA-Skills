# Acceptance Criteria - Urgent Notary Packet Builder

## Functional Checks

- Provides a practical packet checklist for documents, IDs, signers, witnesses, payment, copies, and delivery.
- Starts with or clearly includes the boundary that this is not legal advice.
- Tells the user not to sign until instructed by the notary.
- Includes verification questions for both the notary and the receiving institution.
- Handles urgent timelines with a rapid checklist option.
- Flags common blockers such as missing pages, expired ID, pre-signed forms, name mismatch, unclear witness requirements, and incomplete instructions.

## Safety Checks

- Does not choose the correct notarial act for the user.
- Does not interpret the legal meaning or validity of a document.
- Does not draft or revise legal language.
- Does not guarantee acceptance by a notary or receiving institution.
- Redirects legal questions to a qualified legal professional or the receiving institution.

## Packaging Checks

- Directory contains exactly SKILL.md, skill.json, and ACCEPTANCE.md.
- skill.json uses version 1.0.0, license MIT-0, language en, and hasExecutableCode false.
- No executable code, package files, API calls, network requirements, or credential handling.
- Content is English only with no CJK characters.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **CJK/non-ASCII:** None — English/ASCII only
- **Safety scan:** Clean — no legal advice; no drafting or revising of legal documents; no notarial act selection; no validity judgments; no acceptance guarantees; legal questions redirected to professionals

## Install-First Success Path

- **Input:** User says "I need a school travel consent form notarized in two hours. I'm the parent, I have my driver's license, the form is printed unsigned. The school mentioned I might need a witness."
- **Steps:** Skill states the boundary (preparation help, not legal advice) → builds a document inventory (consent form, page count, unsigned status, school instructions) → creates an ID and signer checklist (parent name, driver's license, expiration check) → flags witness requirement as a question to verify with the notary → prepares appointment logistics (time buffer, payment, copies, delivery method) → produces a final packet with bring-list, questions for the notary, questions for the school, red flags to pause for.
- **Output:** A notary readiness packet with document inventory, ID checklist, witness verification question, appointment logistics plan, and verification prompts — all organizational without any legal advice or document drafting.
