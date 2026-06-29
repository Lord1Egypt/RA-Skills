---
name: wapc-submission
description: Automate WAPC award submissions on mulandxc.com when you need to collect real LoTW-confirmed evidence, fill the WAPC table, upload screenshots, save applicant info, and complete the final browser-based submission flow.
---

# WAPC Submission

## Overview

Use this skill for the Mulan DX Club WAPC application flow. Work from real LoTW-confirmed QSOs only and keep the submission backed by the site's own saved state, not by what the page merely renders.

## Workflow

1. Inspect the current WAPC page and the task brief before acting.
2. Use LoTW as the source of truth:
   - search `QSO Query` with exact-length `?` wildcards when a prefix is unknown
   - only accept records with visible `QSL` text
   - prefer the LoTW `Details` page when the row needs confirmation
3. Prepare real screenshots only:
   - capture from LoTW, not from generated HTML
   - keep the browser view wide enough for the QSO detail and QSL text
   - add a large, high-contrast signal-report label on the right side only when the source mode supports it
4. Save evidence in the ordered project folder using numbered filenames.
5. Fill the WAPC table by hitting the site's own save endpoints, not by editing only the visible DOM.
6. Recheck the backend list and `check_detail` before submitting.
7. Submit only after the applicant-info modal is complete with user-approved personal data.

## Practical Rules

- One province needs one valid LoTW screenshot.
- Treat the backend JSON as authoritative when the page looks filled but validation still fails.
- `donation_app_list?wapc_app_id=806` is the best source for row IDs and saved values.
- `account/update_app_detail` saves a single text field for one row.
- `account/upload_app_img?id=<row id>` uploads the evidence image for that row.
- `account/check_detail` must return `{"state":"ok"}` before final submission.
- `account/app_save` stores the applicant info modal fields.
- Keep tab count low and reuse one working WAPC tab whenever possible.

## Reference

Read [WAPC workflow reference](references/workflow.md) for the exact row structure, validation sequence, and submission modal fields.
