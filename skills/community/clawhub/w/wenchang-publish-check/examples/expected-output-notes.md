# Expected Output Notes

- State whether the run is `preflight` or `final`.
- Keep one formal body per platform and write metadata to a separate publish package.
- Provide WeChat titles, search title, summary, cover copy, sharing copy, keywords, and illustration decision.
- Provide Zhihu title types, lead, summary, topics, illustration decision, and comment prompt.
- Provide Xiaohongshu cover title, first-line hook, body caption, image order, CTA, and grouped tags.
- Record delivery mode, platform profile, image count, ratio, local/public asset policy, and manifest target for every card-based branch.
- In final mode, verify real files, dimensions, order, per-image visual QA, manifest state, and human confirmation.
- Mark hot tags `unverified` unless current source, values, and check time are recorded.
- Keep human-unconfirmed card images at `needs_review`; return `ready_to_publish`, `needs_review`, or `blocked` with concrete blockers.
- Do not generate images, upload files, or perform external publishing.
