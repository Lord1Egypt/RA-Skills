# Proposed-edit contract

All suggestions must point to immutable source `blocks`, with one evidence quote appearing **verbatim** in the source block. Do not treat a quote as support for a factual conclusion. Use the `assets/review.example.json` contract.

- `replace`: `{type, block_id, before, after}`; `before` must exactly match source text. Use for proofreading, clarity and local tightening.
- `insert_after`: `{type, after_block_id, new_id, text, thread}`. Use for explicit bridges or missing prerequisites.
- `move_after`: `{type, block_id, after_block_id}`. Use for coherent paragraph reordering; reevaluate the new neighbors afterward.
- `delete`: `{type, block_id, before}`. Use only when information is genuinely redundant or incorrect and removal preserves intent.

Each suggestion has `id`, `title`, `why`, `priority`, `thread`, `anchor`, `evidence`, and `operations`. Suggested changes are never silently applied; preview and export use the accepted set. Reject or undo must restore the original. Changing the immutable source or any anchor requires a fresh review; do not attach stale suggestions to newly edited text.

After applying a group of suggestions, inspect possible overlaps: two replacements of the same source paragraph conflict unless deliberately authored as one combined suggestion. Perform a second semantic and grammatical reading to catch broken pronouns, claims that lost their qualifications, repetition from bridges, and moved paragraphs lacking setup. Mark that independent check as not done if it did not occur. Any external claim requiring verification remains unresolved until a proper source or runtime probe supports it.
