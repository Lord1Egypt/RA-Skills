> Subclip sandbox: use only pinned, validated imports and native Subclip tools. Package/skill installation, external CLI execution, provider API keys, and standalone project setup are unavailable. Verify managed resources before use; use a supported alternative when unavailable.

# Workflow catalog (moved)

Each workflow's input/output/trigger contract now lives in its own route file — one
small read per candidate instead of a whole catalog:

`references/routes/<workflow>.md` — e.g. `routes/product-launch-video.md`,
`routes/general-video.md`, `routes/remotion-to-hyperframes.md`.

The same file carries that route's interview entry (must-haves, conditionals, deferred
asks, run-shape), so confirming a route is exactly one read.
