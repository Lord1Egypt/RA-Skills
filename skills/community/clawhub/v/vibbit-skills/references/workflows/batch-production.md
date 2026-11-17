# Batch production

Establish each input, total count, variation dimensions, and output specifications. Execute the authorized N items; ask when the count is missing. Do not generate indefinitely or keep sampling alternatives. See [credits and limits](../runtime/limits-and-credits.md).

Client batching organizes supported public operations, normally submitting one item at a time. Keep item ID, input/request path, journal path, real task ID, state, and actual results. A local batch manifest is not a server batch ID.

Validate required fields and downstream dependencies for all items before execution. Preserve failures and uncertain submissions; independent items may continue within existing authorization. On recovery, query existing IDs and retain successes. Resubmit only when nonacceptance is established or regeneration is authorized.

Work in bounded rounds and report actual completed/failed/running counts. Return item-to-result mappings with diagnostic IDs. Do not infer precise costs from offline checks.

For saved scripts/talent applied to a new product, use the [creative library](creative-library.md) and [batch records](../contracts/creative-library.md#batch-records). Pin template/talent/scene revisions and product evidence per selected pairing, without an implicit Cartesian product. Check applicability and prepare actual speech, prompts, and requests per item. Keep the base template; save production copy/tasks under the batch. Missing inputs remain needs_input instead of using example values or the old product. Resume submitted, uncertain, and successful items from their original journals.

For platform variants, share confirmed facts/media but retain separate platform briefs and revisions. [Meta](../platforms/index.md) exploration recipes are not instructions to generate every candidate. Link selected creative IDs to actual media through [handoff](../contracts/creative-handoff.md).

For local templates, use a real [template project](../resources/render-templates.md), retain its version, per-item parameters/media/output/logs, and choose concurrency according to actual host/engine resources. Only actual cloud tasks get task IDs. Retain successful items and rerender only affected items; offline validation does not establish exact render time.

Variants sharing adopted audio can share one [transcript record](../runtime/transcript-tools.md), with verified timeline mappings for each export. Different speech, languages, or audio versions each retain their own ASR tasks/results. Equal duration or filenames do not justify timing reuse; resume original queries instead of resubmitting completed recognition.
