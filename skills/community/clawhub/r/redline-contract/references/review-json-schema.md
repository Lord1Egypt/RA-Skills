# Contract Review JSON Schema

`init-review` creates one review entry per non-empty paragraph, with heading context included in `clause_title`. Review each entry independently.

Use `scripts/contract_review_pipeline.py init-review` to create a starter JSON file.

Fill these fields before running `materialize`:

- `supported_party`: Party you represent (for example, `Buyer` or `Licensor`).
- `priority_focus_areas`: List of terms that need extreme attention (for example, `indemnity`, `limitation of liability`, `IP ownership`).
- `opponent_comment_authors`: Word comment authors to classify as opponent side.
- `reviewer`: Name or role of reviewer.
- `overall_notes`: Cross-clause summary notes.
- `clauses[*].favorability`: `favorable`, `neutral`, or `unfavorable` for your party.
- `clauses[*].risk_level`: `low`, `medium`, `high`, or `critical`.
- `clauses[*].risk_summary`: Specific risk in this clause.
- `clauses[*].why_it_matters`: Business or legal impact for your party.
- `clauses[*].proposed_replacement`: Replacement sentence/paragraph to insert as tracked change for that specific paragraph-level review unit.

Opponent comments section:

- `opponent_comments[*].is_opponent_comment`: Boolean set by author matching.
- `opponent_comments[*].response_stance`: `agree`, `partial`, or `disagree`.
- `opponent_comments[*].draft_response`: Draft response to the opponent comment.
- `opponent_comments[*].additional_proposal`: Optional fallback language or compromise proposal.

Do not change:

- `clauses[*].target_paragraph_index`
- `clauses[*].paragraph_indexes`
- `clauses[*].source_text`
- `opponent_comments[*].comment_id`
- `opponent_comments[*].anchor_text`

These fields map review entries to DOCX paragraph positions and Word comment threads.
