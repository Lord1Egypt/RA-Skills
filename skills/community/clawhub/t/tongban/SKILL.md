---
name: shanghai-service-guide
description: Help users with Shanghai government service questions using public Shanghai "一网通办" service-guide data. Use when the user asks about 上海办事, 一网通办, 办事指南, 去哪办, 哪个部门, 线上办理, 线下窗口, 个人事项, 法人事项, or wants to identify the right Shanghai department, service item, online/offline path, or next step for a described need.
---

# 上海办事指南

## Overview

Use this skill to map a user's Shanghai service need to likely municipal departments and public service items. Prefer the bundled reference data first; browse the official site only when the local data is insufficient or the user needs current policy confirmation.

## Workflow

1. Identify the user's role:
   - `个人` for residents, household registration, certificates, social security, medical insurance, housing, travel, public services, or personal permits.
   - `法人` for companies, organizations, licenses, filings, annual inspection, tax, investment, trade, construction, intellectual property, or employer services.
   - If unclear, search both and say which role each result belongs to.
2. Extract keywords from the request:
   - Business object, action, certificate/license/material, life event, industry, department clue, and online/offline preference.
   - Normalize synonyms, for example 公司/企业 -> 法人, 户口/落户 -> 户籍, 医保 -> 医疗保障, 市场监管/营业执照 -> 市市场监管局.
3. Search local references:
   - Start with `references/index.md` for department and common keyword orientation.
   - Use `references/service_items.jsonl` for exact item records. Search with `rg` over Chinese keywords and department names.
   - Always also search `references/required_items.json` and `references/required-items.md`; these are user-specified must-include item names that may not appear in the public municipal item-list API.
   - Use `references/departments.json` to expand department abbreviations to official names and codes.
4. Return 1-5 candidates ranked by fit. For each candidate include:
   - Department
   - Role (`个人` or `法人`)
   - Main item and subitem
   - Item type
   - Whether online handling appears available (`st_net`)
   - Official guide candidate URL
   - Plain next step
5. Handle uncertainty explicitly:
   - If fewer than two strong keyword matches exist, ask one clarifying question or present low-confidence candidates.
   - If multiple departments plausibly apply, group by department and explain the distinguishing clue.
   - For time-sensitive policy, materials, windows, fees, or eligibility, tell the user to verify on the official "一网通办" page or call Shanghai government service hotline 021-12345.

## Data Files

- `references/index.md`: compact human-readable index and examples.
- `references/service_items.jsonl`: one normalized service item per line. Key fields include `department_name`, `department_short_name`, `department_code`, `role`, `item_name`, `subitem_name`, `item_type`, `st_net`, `item_id`, `item_code`, `source_url`, `guide_url`, and `detail_status`.
- `references/departments.json`: municipal department names, short names, and codes.
- `references/required_items.json` and `references/required-items.md`: user-specified required item names. Use these as coverage guarantees, but distinguish `official_status=matched` from `official_status=needs_verification`.

## Response Rules

- Do not claim a service can definitely be completed online; say "公开事项数据标记为可网上办理" when `st_net` is `是`.
- Do not invent required materials, deadlines, fees, or window addresses if the local record lacks detail.
- Always include at least one official source URL for actionable recommendations.
- For required items with `official_status=needs_verification`, say the item is included as a required alias/name but was not found in the current public municipal item-list dataset; ask the user to verify on "一网通办", "随申办", or 021-12345 before acting.
- Keep answers practical: department first, then matching matters, then next steps.
- Remind users that current official pages and 021-12345 are authoritative for final eligibility and processing details.

## Refreshing Data

Use the scripts only when the user asks to refresh or rebuild the data:

```bash
python3 scripts/fetch_zwdt.py --output references/raw_items.json
python3 scripts/normalize_data.py --input references/raw_items.json --output references/service_items.jsonl
python3 scripts/build_reference.py --input references/service_items.jsonl --output-dir references
python3 scripts/validate_data.py --items references/service_items.jsonl --departments references/departments.json
```

The fetcher uses public pages and APIs only, does not log in, and does not submit government service forms.
