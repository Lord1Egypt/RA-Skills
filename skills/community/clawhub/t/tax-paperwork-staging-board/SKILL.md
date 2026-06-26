---
name: Tax Paperwork Staging Board
description: Gather scattered tax-time paperwork quickly into a clear staging board with a missing-items checklist, folder map, and handoff cover sheet, without giving tax or legal advice.
version: 1.1.0
type: prompt-flow
author: Bell (design)
tags: [tax-preparation, document-staging, deadline-tracking, kanban]
---

# Tax Paperwork Staging Board

## Overview

Tax Paperwork Staging Board helps a user organize tax-season paperwork when documents are scattered across email, portals, paper mail, folders, and receipts. It creates a practical staging system: what to gather, where to put it, what is missing, and how to hand it off to a tax professional or reviewer.

This skill is document staging only. It does not decide tax treatment, estimate taxes, interpret law, optimize deductions, or say whether an item is deductible. The user should verify all tax questions with official instructions or a qualified tax professional.

## When to Use

Use this skill when the user says things like:

- "I need to gather my tax papers fast."
- "Help me organize documents for my accountant."
- "My tax forms are scattered everywhere."
- "What should I put in my tax folder?"
- "I need a checklist before handing documents over."

## Required Inputs

Collect only the details needed to stage paperwork:

- Filing context: country or region, tax year, individual or household, self-employed or employee, rental or investment activity if relevant
- Deadline or handoff date
- Where documents currently live: paper mail, email, downloads, employer portal, bank portal, brokerage portal, phone photos, receipts box
- Handoff recipient: self-prep, tax professional, family member, bookkeeper, or other reviewer
- Known life changes: job change, move, school, new child, home purchase, business activity, major medical expenses, charitable giving, sale of investments, rental activity

If the user does not know an answer, proceed with an "unknown" marker rather than guessing.

## Workflow

### Step 1 - Identify the Filing Context

Confirm the tax year, region, deadline, and who will use the staged documents. Ask whether the user wants a fast first-pass board or a detailed handoff board.

Keep the context neutral. Do not infer filing status, eligibility, deductions, credits, or legal positions.

### Step 2 - Build the Needed Categories List

Create categories that match the user's context. Common categories include:

- Identity and prior-year reference: previous return, taxpayer IDs kept privately, address changes, dependent information
- Income: employment forms, contract income forms, business income summaries, unemployment, pension or retirement income, interest and dividends
- Investments: brokerage tax forms, sale summaries, crypto or digital asset reports if applicable, capital gains statements
- Property and housing: mortgage interest, property tax statements, rent-related records where relevant, home purchase or sale documents
- Business or side work: income log, expense summaries, mileage log, invoices, platform statements, business bank summaries
- Education: tuition statements, student loan interest, scholarship or grant records
- Health and insurance: health coverage forms, medical expense summaries, health savings account forms
- Giving and payments: charitable donation receipts, estimated tax payments, extension payments
- Other supporting records: major life event documents, notices from tax agencies, correspondence, unusual one-time items

Label each category as "likely needed," "only if applicable," or "ask professional."

### Step 3 - Sort the Documents

Guide the user to sort documents into a small folder map:

- 00 Intake and cover sheet
- 01 Identity and prior-year reference
- 02 Income
- 03 Investments
- 04 Property and housing
- 05 Business or side work
- 06 Education
- 07 Health and insurance
- 08 Giving and tax payments
- 09 Notices and questions
- 10 Receipts and support

For digital folders, recommend consistent file names such as year, category, source, and short description. For paper folders, recommend sticky notes or divider labels with the same categories.

### Step 4 - Flag Gaps and Conflicts

Create a missing-items checklist with:

- Missing item
- Why it may matter
- Where to look next
- Owner
- Due date
- Status
- Question for reviewer

Flag duplicates, blurry scans, mismatched names, partial-year forms, missing pages, and unclear dates. Use "verify" language rather than making conclusions.

### Step 5 - Package the Handoff

Prepare a cover sheet for the reviewer. Include:

- Tax year and filing context
- Folder map
- Summary of included documents
- Missing-items checklist
- Open questions
- Known deadlines
- Contact preferences
- Notes about unusual events or documents

Remind the user to keep originals or backups and send sensitive documents only through secure channels chosen by the professional or official service.

## Output Template

### Tax Paperwork Staging Board

**Filing context:**
- Tax year:
- Region:
- Handoff recipient:
- Deadline:
- Known life changes:

**Folder map:**
1. 00 Intake and cover sheet -
2. 01 Identity and prior-year reference -
3. 02 Income -
4. 03 Investments -
5. 04 Property and housing -
6. 05 Business or side work -
7. 06 Education -
8. 07 Health and insurance -
9. 08 Giving and tax payments -
10. 09 Notices and questions -
11. 10 Receipts and support -

**Needed categories:**
- Likely needed:
- Only if applicable:
- Ask professional:

**Missing-items checklist:**
- Item:
  - Where to look:
  - Owner:
  - Due date:
  - Status:
  - Question for reviewer:

**Handoff cover sheet:**
- Included documents:
- Missing or pending documents:
- Open questions:
- Deadlines:
- Notes for reviewer:

**Verification reminder:** This is a document-staging board, not tax or legal advice. Verify tax treatment, filing requirements, deductions, credits, and deadlines with official guidance or a qualified tax professional.

## Safety Boundaries

- Do not give tax, legal, accounting, or investment advice.
- Do not say whether an expense is deductible, taxable, allowed, or disallowed.
- Do not calculate tax liability, refunds, penalties, credits, or filing status.
- Do not replace official tax instructions, government guidance, or professional review.
- Do not request full taxpayer IDs, passwords, account access, or other sensitive credentials.
- Recommend secure handling for personal documents and keeping originals or backups.
- If the user receives a tax agency notice, audit letter, levy, garnishment, or urgent legal deadline, recommend contacting the agency through official channels or a qualified professional promptly.


## Usage Scenarios

### Scenario 1

**User Input:** "Set up a board for 2025 personal tax filing. I'm a W-2 employee with a side LLC and rental property."

**Expected Output:** Board created with columns: To Collect / In Progress / Ready. Pre-populated card templates for W-2, 1099-MISC, Schedule C docs, Schedule E docs, and deductions receipts.

### Scenario 2

**User Input:** "Move my W-2 and mortgage 1098 to 'Ready'. What's still missing for Schedule C?"

**Expected Output:** Status updated. Returns a gap analysis: missing business-expense receipts, home-office square footage, and vehicle mileage log.

### Scenario 3

**User Input:** "Archive the 2024 board and clone the template for 2025 with adjusted deadlines."

**Expected Output:** 2024 board archived (read-only). 2025 board created with inherited template but blank status; all deadlines shifted +1 year.


### Scenario 4: 每年报税材料凑不齐
**User input:** "每年3-6月个税汇算清缴前我都找不到材料，发票、捐赠凭证、继续教育信息全乱放。怎么做才能每年报税不慌？"
**Expected output:** 个税汇算材料管理系统——第一步：在手机里建一个相册"2026年个税"，每次有相关票据直接拍照放进去（捐赠发票/继续教育证书/购房合同/房租合同/大病医疗单据）；第二步：用一个共享Excel（或飞书文档）每月1号记录：收入来源/专项附加扣除变化/是否有新的可抵扣项；第三步：每年2月底前整理上年度的所有材料，按类别放文件夹（专项附加扣除/其他扣除/捐赠/大病/年终奖）；第四步：3月1日一开系统就填报（避免排队），用个税App的"预填"功能核对单位上报的收入是否准确。关键：平时每产生一笔可能可抵扣的支出就立即归档。

## Example Prompts

Copy and paste one of these into your AI assistant with your details filled in:

1. **Fast accountant handoff:** "My accountant needs everything tomorrow and my tax forms are everywhere. I have W-2s in my email, 1099s in a drawer, mortgage interest in a portal, and donation receipts in a shoebox. Tax year 2025. Build me a staging board with a folder map and cover sheet so I can hand everything off cleanly."

2. **Self-employed receipt chaos:** "I do freelance work on the side and have a box of receipts, payment screenshots, and platform statements. I also drove about 3,000 miles for client meetings. Tax year 2025, I file as an individual. Help me sort these into categories and flag what's missing before I meet my tax preparer."

3. **Missing form from old job:** "I changed jobs in March 2025 and I think I'm missing a W-2 from my previous employer. I checked my email but nothing's there. Tax deadline is two weeks away. Help me build a missing-items checklist and a cover sheet I can give my accountant with open questions flagged."
