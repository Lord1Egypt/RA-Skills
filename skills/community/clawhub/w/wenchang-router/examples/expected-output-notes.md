# Expected Output Notes

- Identify the platform branch and current artifact stage.
- Recognize topic, research, draft, review, preflight, illustration, card authoring, card rendering, visual QA, human confirmation, image URL, apply, and final-check stages.
- Route a `publish_ready` card package with no real images to `cards-to-images`.
- Route to `md-img-r2` only when checked local assets need public URLs.
- Return accepted inputs, ignored or stale context, a compact `content_state`, and the next action.
- Stop before unresolved human or external-write gates.
