# Finding Specific Content Workflow (Multi-Stage Refinement)

Use this workflow when a user wants to find the "most [adjective]" clip (e.g., "the most funny clip," "the most exciting part") from a video. This process optimizes for speed and accuracy by escalating through multiple API tasks.

## Phase 1: Rapid Automated Discovery (`clip` with `--no-export`)
The `clip` task is designed to identify high-quality, engaging moments automatically.
- **Action**: Submit a `clip` task with the `--no-export` flag.
- **Why?**: Skipping video rendering makes results available much faster (within minutes).
- **Evaluation**: Review the `desc` (description), `title`, and `tags` of each clip in the result.
    - **Found?**: If a clip's description clearly matches the user's intent, proceed to Phase 4 for rendering.
    - **Not found?**: If none of the automated clips match, move to Phase 2.

## Phase 2: Natural Language Targeted Search (`search` with `--no-export`)
If the automated `clip` task didn't catch the specific vibe, use the `search` task with the user's criteria as the query.
- **Action**: Submit a `search` task with the `--query "the most [user adjective] moment"` and the `--no-export` flag.
- **Why?**: Like Phase 1, disabling rendering ensures near-instant search results.
- **Tip**: If Phase 1 results were close but not perfect, incorporate keywords from their `desc` or `tags` into your Phase 2 query to bridge the gap.
- **Evaluation**:
    - **Found?**: If a result has a high score (>= 50) and a matching description, title, or tags, proceed to Phase 4.
    - **Low Confidence?**: If the highest score is `< 50` or the descriptions are irrelevant, move to Phase 3.

## Phase 3: Context-Aware Query Refinement (`summarize` + `search` with `--no-export`)
A low score often means the query doesn't match how the model "sees" the video. Use a summary to bridge the gap.
- **Action 1**: Submit a `summarize` task.
- **Action 2**: Review the `summary` and `highlights` to understand the actual vocabulary and themes used in the video.
- **Action 3**: Refine the search query based on the summary (e.g., if the user wants "funny" and the summary mentions "a clumsy blooper with a cat," change the query to "clumsy blooper cat").
- **Action 4**: Re-run the `search` task with the refined query and `--no-export`.
- **Final Result**: If still not found, report to the user that the specific content could not be located.

## Phase 4: Precision Rendering & Delivery (using `export`)
Since rendering was disabled during the discovery phases, you must now render the specific clips identified as successful.
- **Action**: Submit an `export` task using the `--id` from the successful discovery task (Phase 1 or 2).
- **Optimization**: Use `--clip-indices` to render only the specific clip(s) that match the user's criteria. This is faster and more cost-efficient than re-running the entire discovery task.
- **Why?**: The standalone `export` API allows you to take existing non-exported results and render them with specific style preferences such as `--ratio`, `--target`, or `--caption-display both` with a valid `--cc-style-tpl`.
- **Deliver**: Provide the clickable `export_link` from the `export` task results to the user.
