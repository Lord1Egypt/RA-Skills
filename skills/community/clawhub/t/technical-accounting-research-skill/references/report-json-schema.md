# Report JSON Schema

Use this structure as input to `scripts/build_accounting_report_docx.py`.

## Required top-level fields

- `issue` (string)
- `facts` (array of strings)
- `guidance` (array of objects)
- `analysis` (array of strings)
- `conclusion` (string)

## Formatting rule

All string fields should contain final prose, not Markdown control syntax. Do not include raw heading markers (`#`, `##`, `###`, `####`), Markdown bullet prefixes, or other Markdown formatting tokens unless they are intended to appear literally in the final document.

## Recommended fields

- `title` (string)
- `prepared_for` (string)
- `prepared_by` (string)
- `date` (string, ISO `YYYY-MM-DD` preferred)
- `subject` (string)
- `assumptions` (array of strings)
- `disclosure_considerations` (array of strings)
- `open_items` (array of strings)
- `next_steps` (array of strings)
- `journal_entries` (array of objects)
- `qa` (array of objects, especially for `q-and-a` format)
- `to` / `cc` / `from` (strings for `email` format)

## Guidance object

Each entry in `guidance` should include:

- `citation` (string)
- `source_type` (`authoritative` or `interpretive`)
- `key_point` (string)
- `url` (string)
- `accessed_on` (string date)

## Journal entry object

- `description` (string)
- `debit` (string)
- `credit` (string)
- `amount` (string)

## Q-and-A object

- `question` (string)
- `answer` (string)

## Minimal example

```json
{
  "issue": "How should implementation fees in a SaaS arrangement be recognized?",
  "facts": [
    "Customer pays a nonrefundable upfront fee.",
    "The fee does not transfer a distinct good or service at contract inception."
  ],
  "guidance": [
    {
      "citation": "ASC 606-10-25",
      "source_type": "authoritative",
      "key_point": "Identify performance obligations and assess whether promised goods/services are distinct.",
      "url": "https://www.fasb.org",
      "accessed_on": "2026-03-07"
    }
  ],
  "analysis": [
    "The upfront fee is an advance payment for future services.",
    "Revenue should generally be recognized over the expected period of benefit."
  ],
  "conclusion": "Defer upfront fee revenue and recognize over the expected customer relationship period."
}
```
