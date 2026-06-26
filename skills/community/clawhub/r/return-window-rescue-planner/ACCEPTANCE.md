# Acceptance Tests - Return Window Rescue Planner

## Overview
- **Skill:** Return Window Rescue Planner
- **Slug:** return-window-rescue-planner
- **Priority:** P1
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 10

## AT-1: Return inventory is captured.
- **Check:** Each item has store or seller, deadline, method, proof, and packing needs when provided.
- **Expected:** Missing information is marked clearly.
- **Pass:** The user can see every return in one action sheet.

## AT-2: Deadlines are triaged.
- **Check:** Items are sorted or labeled by urgency.
- **Expected:** Today, next few days, this week, later, and unknown categories are used when helpful.
- **Pass:** The user knows what must be handled first.

## AT-3: Policies are not invented.
- **Check:** The skill reminds the user to verify current store policies and deadlines.
- **Expected:** No fabricated return windows, fees, addresses, or eligibility rules.
- **Pass:** Unverified policy details are not presented as fact.

## AT-4: Proof requirements are listed.
- **Check:** Receipts, order numbers, QR codes, labels, packing slips, and other proof are identified.
- **Expected:** Missing proof is marked as a blocker.
- **Pass:** The user knows what to gather before leaving or shipping.

## AT-5: Packing needs are specific.
- **Check:** The plan lists item parts, accessories, tags, boxes, padding, labels, and authorization details when relevant.
- **Expected:** The user can set up a packing station.
- **Pass:** The plan reduces forgotten-item risk.

## AT-6: Personal data warning is included.
- **Check:** The final action sheet reminds the user to remove, cover, or shred personal data on labels and paperwork.
- **Expected:** Privacy caution is visible before packing or drop-off.
- **Pass:** Sensitive data is not accidentally exposed.

## AT-7: Route or batch order is grounded.
- **Check:** The route uses only user-provided locations, deadlines, and constraints.
- **Expected:** If geography is unknown, the skill provides a logical batch order instead of pretending to know travel time.
- **Pass:** The route plan is honest and useful.

## AT-8: Blockers are visible.
- **Check:** Unknown deadlines, missing labels, missing receipts, policy uncertainty, and packaging gaps are called out.
- **Expected:** Blockers are separated from ready-to-go items.
- **Pass:** The user can resolve problems before the return window closes.

## AT-9: Final checklist is actionable.
- **Check:** The output ends with a before-you-go or before-you-mail checklist.
- **Expected:** It includes verification, packing, privacy, labels or QR codes, and tracking or receipt retention.
- **Pass:** The user can execute without rereading the whole plan.

## AT-10: No-code compliance.
- **Check:** The skill remains prompt-only.
- **Expected:** `requires_api` is false, `no_code_execution` is true, and no executable steps are required.
- **Pass:** Skill has no scripts, tools, API calls, credentials, or network dependency.

## Clean Scan Evidence

- [x] No executable code, scripts, binaries, or package files.
- [x] No secrets, credentials, API keys, tokens, or environment variables.
- [x] No network calls, API endpoints, or internet dependencies.
- [x] No CJK characters. Documentation is English/ASCII only.
- [x] `skill.json` is valid JSON with `version=1.0.0`, `license=MIT-0`, `language=en`, `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, `ACCEPTANCE.md`.
- [x] No temp files, log files, or build artifacts.

## Install-First Success Path

**Input:** "I have three items to return this week and the deadlines are tight. Help me plan my returns."

**Steps:**
1. Skill asks for each item: name, store, deadline, return method, condition, proof available, packing needs.
2. Skill triages items by deadline urgency, identifies missing proof and blockers, and builds a batch/route order.
3. Skill produces a return action sheet with inventory, deadline triage, proof checklist, packing station list, and before-you-go checklist.

**Output:** A return window rescue action sheet with deadline triage, return inventory table, route/batch order, packing station checklist, and final before-you-go verification list.
