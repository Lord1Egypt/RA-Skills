# Acceptance Tests - Tax Paperwork Staging Board

## Overview
- **Skill:** Tax Paperwork Staging Board
- **Slug:** tax-paperwork-staging-board
- **Priority:** P2
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 10

## AT-1: Filing context is identified first.
- **Check:** Response asks or states tax year, region, deadline, and handoff recipient before building the board.
- **Expected:** Unknown details are marked as unknown rather than assumed.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-2: Needed categories are context-aware.
- **Check:** Response lists document categories such as income, investments, property, business, education, health, giving, payments, and notices.
- **Expected:** Categories are labeled as likely needed, only if applicable, or ask professional.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-3: Folder map is provided.
- **Check:** Output includes a practical folder map for paper or digital sorting.
- **Expected:** Folder labels are clear enough for immediate use.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-4: Missing-items checklist is provided.
- **Check:** Output includes missing item, where to look, owner, due date, status, and reviewer question.
- **Expected:** Gaps are tracked without making tax conclusions.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-5: Handoff cover sheet is included.
- **Check:** Output contains a cover sheet with filing context, included documents, missing items, open questions, deadlines, and notes.
- **Expected:** The cover sheet is suitable for a tax professional or reviewer.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-6: No tax or legal advice is given.
- **Check:** Response does not decide deductions, credits, filing status, taxable treatment, liability, penalties, or eligibility.
- **Expected:** Tax-treatment questions are redirected to official guidance or a qualified professional.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-7: Sensitive information is handled safely.
- **Check:** Response does not ask for full taxpayer IDs, passwords, account access, or credentials.
- **Expected:** User is reminded to use secure channels and keep originals or backups.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-8: Urgent notices are escalated appropriately.
- **Check:** If the user mentions an agency notice, audit, levy, garnishment, or urgent deadline, response recommends official channels or professional help promptly.
- **Expected:** No attempt is made to provide legal representation or final interpretation.
- **Pass:** Output demonstrates compliance with this criterion.

## AT-9: Document Language
- **Input:** Any valid trigger.
- **Expected:** Output is English-first with no CJK-dominant paragraphs.
- **Pass:** No CJK-dominant content in main output.

## AT-10: No-Code Compliance
- **Check:** No executable code, scripts, API calls, external handlers, or network dependency.
- **Expected:** skill.json has `hasExecutableCode: false`, `requires_api: false`, and `no_network: true`.
- **Pass:** Skill is purely document/prompt-flow with no executable components.

## Install-First Success Path

- **Input:** User says "My accountant needs everything tomorrow and my tax forms are everywhere. I have W-2s in email, 1099s in a drawer, mortgage interest in a portal, and donation receipts in a shoebox. Tax year 2025. Build me a staging board with a folder map and cover sheet."
- **Steps:** Skill confirms filing context (tax year, region, deadline, handoff recipient) → builds needed categories list labeled as likely needed/only if applicable/ask professional → guides user to sort documents into a folder map (00 Intake, 01 Identity, 02 Income, 03 Investments, etc.) → creates a missing-items checklist with where to look, owner, due date, status → produces a handoff cover sheet with included documents, missing items, open questions, deadlines, and notes → reminds user to verify tax treatment with official guidance or a qualified professional.
- **Output:** A tax paperwork staging board with filing context summary, categorized folder map, missing-items checklist, handoff cover sheet, and open-questions tracker — all document staging without tax or legal advice.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **Safety scan:** Clean — does not give tax/legal/accounting/investment advice; does not decide deductibility, calculate liability/refunds, or interpret tax law; does not request full taxpayer IDs, passwords, or account access; recommends secure handling of personal documents and professional review.
