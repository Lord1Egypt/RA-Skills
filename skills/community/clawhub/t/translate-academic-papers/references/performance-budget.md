# Efficient, complete processing

There is no delivery-time limit. Complete the translation and all quality checks before delivery; do not convert a task into a timed-out draft because an arbitrary duration has elapsed.

## Efficient execution

- Parse the PDF or authoritative HTML once and retain one canonical source map for both outputs.
- Batch stable-ID translation blocks and process independent figure jobs concurrently where tool limits permit.
- Key text caches by SHA-256 of source text plus translation-policy and terminology-ledger versions.
- Key figure caches by SHA-256 of the source image plus label map plus Image 2 prompt version.
- Reuse a cache entry only after its prior acceptance record passes the current validation rule.
- Build both document variants from the same in-memory records in one process.
- Patch a failed unit and rerun its relevant validator; do not restart successful extraction, translation, figure edits, or document construction.

## Figure requirement

For every raster figure containing English semantic text that must be replaced, call Image 2 with the original figure as the edit target. Do not use deterministic in-image text replacement as a substitute. Preserve the visual data and accept the output only after visual inspection confirms in-place Chinese replacement.

## Service failure

If a translator, renderer, or image service fails, retain valid completed units and retry only the affected unit. If it remains unavailable after reasonable bounded retries, report the concrete external blocker rather than delivering a falsely complete document.

