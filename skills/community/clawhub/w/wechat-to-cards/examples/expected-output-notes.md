Expected output:

- Starts with source diagnosis and treats the skill as a WeChat-specific adapter.
- Routes generic card authoring through `long-to-cards` with `platform_profile=wechat-inline`.
- Routes `publish_ready` card packages through `cards-to-images` until real checked files and a manifest exist.
- Adds Moments copy, community share copy, card-specific CTA, source caveats, and follow-up ideas.
- Reuses approved title, summary, cover, tags, and CTA from the publish package instead of silently overwriting them.
- Preserves the article thesis and marks claims needing verification.
- Stops before external upload or publishing and leaves human confirmation visible.
