---
skill_code: VB-04
version: "1.0.0"
---

# Storyboarder

Read [shared boundaries](guidelines.md). Use `generate` for new scripts and `refine` for existing ones. Preserve supplied shots, exact dialogue, ratio, chosen hooks/roles, and user count/duration.

Read [5V frameworks](libraries/storyboard-frameworks.md) when choosing types or an exploration set. Full 5V gives Hero, Feature, Social, Solution, and Moment with distinct jobs/hooks. A single ad needs only its best-fitting type.

Choose the intended psychological change and audience stage. Differentiate along hook mechanism, visual approach, character voice, format/pacing, and message angle. Use the [category library](libraries/storyboard-categories.md) only when it affects demonstration/context; unmatched products need their real use case, not a forced category.

Arrange hook, context, reveal/proof, benefit, and action as needed. Longer ads may use opening at 0–2 seconds, change at 5–6, benefit preview at 12–15, and action transition at 20–25; scale or omit beats to fit the real duration. Plan audible and sound-off understanding. Trending audio is a direction, not an available licensed track.

Hero/Feature product exposure, Social's authentic single shot, and Moment's montage need not all become delayed-product fast-cut ads. Every shot should explain what it demonstrates.

## Layered production cards

Four or five cards can start a conventional full script, adjusted to duration/model/assets. Each card is self-contained with complete necessary character, clothing, world, subject motion, and camera motion; “same as above” is insufficient for standalone generation.

Retain:
- Summary: `storyboard_id`, `video_type`, `purpose`, numeric `total_duration_seconds`, hook/reference ID, `emotional_arc`, and five-axis `diversification`.
- `character_lock`: appearance, wardrobe, continuity rules; no invented person for a product-only shot.
- `generation_cards`: stable `shot_id`, order/function, numeric duration, complete generation prompt, motion, do-not constraints, transition, retention note, and actual asset references.
- `audio_layer`: timed exact speech, delivery, music direction, shot effects, and sound-off version.
- `text_overlay_layer`: shot/start/end, exact text, layout; precise safe placement after verification.
- `assembly_notes`: order, transitions, pacing, final duration, dependencies, and missing steps.

These are planning fields, not API schema. Structured output must be valid JSON with actual values, not enum lists or comments as values. Show a readable shot table when that suffices.

For production, use [storyboard workflow](../../workflows/storyboard-video.md). A 1–3-second creative card may need a longer supported generation and real cutting, or a native multi-shot result. Current Seedance minimum is 4 seconds; local animation follows its own timeline. Do not promise precise assembly without a working cutting path or send planning fields directly to APIs.

For refinement, identify concrete hook/pacing/visual/audio/emotional/category problems. Subjective scores are not CTR predictions. Change the requested card and necessary adjacent sound/text/transitions, preserve other cards/assets/task IDs, and record superseded revisions. Do not automatically regenerate the whole ad.
