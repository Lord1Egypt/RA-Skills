# Expected Output Notes

- Identify the earliest stage supported by the supplied artifacts.
- Route WeChat and Zhihu long-form images through `article-to-illustrations`.
- Route Xiaohongshu, WeChat inline-card, Zhihu Idea, and generic card delivery through `long-to-cards -> cards-to-images` by default.
- Route generative or mixed image jobs through `resilient-imagegen -> chatgpt-image-handoff` only when the selected runtime backend requires it.
- Continue `publish_ready` packages until real local images, per-image visual QA, and a `cards-manifest` exist.
- Produce compact card, generation-runtime, handoff, illustration, R2, publish-gate, next-skill, and stop-condition state.
- Stop before unresolved fact decisions, paid or sensitive generation, human image approval, external uploads, URL rewrites, and platform publishing.
