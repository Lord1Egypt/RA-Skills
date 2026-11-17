# Output Schema

The parser writes `fields.json` with the following top-level groups.

| Group | Meaning |
|---|---|
| `source_file` | Reviewed source filename |
| `document_type` | Heuristic document category, not an authoritative classification |
| `basic` | Project name, document title, units, date, code, and location |
| `contacts` | Phone numbers plus only those name/role links supported by nearby text |
| `scope` | Recognized equipment, pipeline, and main work scope |
| `process_parameters` | Domain-specific values recognized by deterministic patterns |
| `schedule` | Total duration, civil duration, stages, daily nodes, and schedule tables |
| `safety` | Keyword counts and source snippets for safety and emergency review |
| `type_specific` | Optional fire-control, steel-structure, or cryogenic fields |
| `review_checks` | Missing items, possible conflicts, and limitations |
| `pending_questions` | Short questions for the customer or project owner |
| `document_stats` | Extracted character, line, and table counts |
| `outline` | Detected headings |

## Interpretation Notes

- An empty string means “not reliably extracted,” not “does not exist.”
- Keyword counts indicate presence only; they do not prove adequacy.
- A `document_type` value is used to select additional extraction patterns.
- `review_checks.conflicts` identifies rule-detectable conflicts. Absence of a conflict does not prove consistency.
- `extracted_text.md` is an intermediate local artifact and may contain personal or commercial information.

## Multi-File Comparison

The script processes one file at a time. Compare multiple `fields.json` files using:

- Exact value match for codes, dates, phones, and explicit quantities
- Scope-aware comparison for total, stage, civil, or installation durations
- Presence/absence comparison for safety and emergency topics
- Manual source review for all ambiguous or OCR-derived fields
