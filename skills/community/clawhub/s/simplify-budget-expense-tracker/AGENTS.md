# Simplify Budget Agent Notes

This skill only works with the official Simplify Budget template or a direct copy of it:
- [Simplify Budget Template](https://docs.google.com/spreadsheets/d/1fA8lHlDC8bZKVHSWSGEGkXHNmVylqF0Ef2imI_2jkZ8/edit?gid=524897973#gid=524897973)

Do not assume compatibility with arbitrary Google Sheets budget trackers.

## Required assumptions

- Tabs must exist exactly as:
  - `Expenses`
  - `Income`
  - `Recurring`
  - `Dontedit`
- Active categories are read from `Dontedit!L10:O39`
- `Expenses` data block starts at row `5`
- `Income` data block starts at row `5`
- `Recurring` data block starts at row `6`
- Expense and recurring expense categories must use `=zategory<stableId>`
- Recurring income may use literal `Income 💵`

## Runtime requirements

Required environment variables:
- `GOOGLE_SA_FILE`
- `SPREADSHEET_ID`
- `TRACKER_CURRENCY`

Optional:
- `TRACKER_CURRENCY_SYMBOL`

The user must share the copied template sheet with the service account email from `GOOGLE_SA_FILE`.

## Operational rules

- Use this template only. If the user points to a different sheet layout, warn that the skill is template-coupled.
- Keep the Google Sheet as the source of truth.
- Find rows first, then mutate by id.
- Do not invent categories. Resolve against the live category list.
- For Telegram/OpenClaw routing, prefer the bundled command wrappers in the skill directory.
- Recurring schedule questions are read-only. Do not materialize recurring rows into `Expenses` or `Income` when answering due-date questions.
- For receipt images, default to one expense per receipt.
- Use the final charged total or grand total, not individual line items.
- Use the merchant name or a short summary as the description.
- Only split a receipt into multiple expenses if the user explicitly asks.
- For mixed-purpose receipts, choose the dominant category unless the split is important enough to require one short clarification.
- Treat the Clawhub skill package and the Clawhub plugin package as separate published outputs.
- Before committing Simplify Budget changes, update both packages unless the change is intentionally limited to one of them.
