# Selection and layout policy

## Source and assembly

- Read the current request, director brief, project, and `list_editor_assets`. A current/saved explicit canvas choice wins; absent one, call `set_canvas_properties` with `vertical`.
- For `.subclip-video-context` created from YouTube, inspect `transcript.srt` when the manifest lists it and import only from `originalPath`. Never download the URL again. If the context lacks a trustworthy timestamped transcript, transcribe the imported item.
- Transcribe one exact source item at a time. Persist completed/pending IDs before each background job, store its job ID, and end the turn until Subclip resumes.
- Default duration is 30–90 seconds, with 45–90 preferred. A 20–30 second interval is acceptable only when unusually complete and compelling. Never exceed 90 seconds unless the creator explicitly changes that editorial requirement.
- Align in/out to real caption sentence/word boundaries. Do not cut off setup, clause, answer, payoff, or punchline.
- Set the first candidate output start to exactly `1.0s`. A candidate may use adjacent source items when one complete thought crosses their boundary. Its pieces stay contiguous; exactly `2.0s` of empty timeline separates candidates.
- “Make clips,” “AI clipping,” “make shorts,” and equivalent requests mean a clips-only reel unless the creator explicitly asks to retain the full source for comparison. Assemble and verify candidates first, then delete the original full-length timeline item IDs. Never delete their Project Media files merely to make the reel.
- For every piece, resolve the owner `fileId`; compute source time as `sourceStartTime + (candidateTime - item.startTime) * playbackRate`; call `place_editor_asset`, then `trim_media_item` with exact source in/out, output start, and original playback rate.
- Keep primary non-overlapping pieces on lane 0. Every Aura background, alternate face crop, or duplicate visual is muted and uses explicit overlap lane/z-order.
- Prefer existing timing over paid retranscription. When the source item owns editor captions, call `reuse_caption_timing_for_media_items` once after every target copy is trimmed. Keep `removeSourceCaptions=false` until the copied words and pages are verified; then delete the full source item through the normal timeline tool. When the source has no owned editor captions but `transcript.srt` supplies timestamped host cues, pass the exact overlapping source-relative cues to `import_caption_cues_for_media_item` for each audible target. Only when neither exact route exists should you transcribe the new audible candidate items sequentially.
- Record candidate number, title, exact duration, score, hook, evidence-based reason, source range, output range, interval checks, caption ownership, and layout in the director brief.
- Write a source-language, non-clickbait hook under 12 words and normally under 90 characters. Its rendering depends on the layout; a hook does not imply a separate TextPanel.
- For `fill_face` and `fill_faces_split`, do not add a separate hook overlay by default. Use the opening Dynamic Caption page as the visible hook, preserving normal caption styling and semantic emphasis. A separate headline that covers the face is a verification failure.
- For `fit_canvas`, add a static TextPanel only when verified negative space exists above the contained foreground. Match Subclip-web unless the creator has a saved brand style: Inter (or SF Pro Display for an Apple-clean layout), about 65px on a 1080-wide canvas, weight 700 (or 500 for Apple-clean), white, transparent background, 1px black stroke at about 60% opacity, black shadow around 32% opacity with `y=2` and blur `3`, line height `1.08`, no animation, at most two compact lines. Shorten or omit it if it collides with the subject, foreground, or captions.
- For `tutorial`, the separate hook card may last four seconds, sit around `y=26%`, use at most 90% canvas width and about 80px type on a 1080-wide canvas, and use a compact black background around 54% opacity with the same restrained stroke/shadow treatment. Keep the screen content and presenter unobscured.

## Candidate contract

Each candidate has:

- `group_index`
- a concise source-language `title`
- `start_time` and `end_time` in seconds on the source timeline
- `duration_seconds`, calculated from the accepted source interval
- `viral_score` from 0–100
- a source-language `hook`, `conclusion`, and `reason`

Rank candidates by likely human retention, then assemble the accepted set in source chronological order. Penalize weak openings, repeated points, low novelty, missing context, and unresolved endings. Keep candidates non-overlapping and meaningfully distinct.

### Selection signals

Prefer a segment that has all of these:

1. An immediate specific hook: question, surprising fact, mistake, contrast, concrete result, tension, or realization.
2. A complete thought or compact story arc.
3. Curiosity, humor, surprise, inspiration, useful insight, or another real emotional payoff.
4. A satisfying answer, conclusion, punchline, or practical takeaway.
5. Standalone meaning without requiring unseen setup.
6. A reason someone would retain, share, save, or discuss it.

Calibrate scores:

- 90–100: exceptional hook, clarity, payoff, and share impulse.
- 70–89: strong, complete, high-potential segment.
- 50–69: usable but missing one important strength.
- Below 50: normally omit.

The hook is creator-facing copy, not invented clickbait. Preserve the transcript's language, register, vocabulary, and vibe. Keep it under 12 words and normally under 90 characters, avoid em dashes/double hyphens, and reject generic openers such as “In this video” or “Let me show you.” The title is the editorial label reported to the creator, not a second mandatory on-screen headline.

## Completion report

After assembly and verification, report every accepted clip individually with:

- title
- exact duration formatted as `M:SS`
- viral score formatted as `N/100`
- one concrete reason tied to its actual hook, insight, tension, payoff, novelty, or share/save value
- optionally, the hook and selected layout when that helps review

Do not describe all candidates with one generic sentence. Titles, durations, scores, and reasons must match the saved director brief so a later turn can audit or revise the selection.

## Layout modes

Follow an explicit creator choice. Otherwise inspect representative source frames and choose the least destructive mode that keeps the subject or information readable.

### `fill_face`

Use for a single talking head or a podcast shot dominated by one speaker.

- Make the primary item a full-canvas `cover` container.
- Use `set_media_source_focus` to keep eyes around the upper third and the face away from crop-prone edges.
- Choose one stable focus per shot. If the subject genuinely changes position, split on a natural shot/sentence boundary and reframe the new segment; do not animate a restless crop.
- Inspect at least the first frame, last frame, each transcript sentence or visible shot boundary, and every 3–5 seconds in between. A materially different speaker, person position, object of interest, or camera composition is a new stable layout segment.

### `fill_faces_split`

Use when two speakers must remain readable and a single vertical crop cannot preserve both.

- With synchronized separate sources, isolate the interval first and use the native split-scene tool when its side-by-side result fits the requested composition.
- With two faces baked into one source, duplicate the exact source range, crop/focus one copy per speaker, place them in two stable panels, and mute one copy. Use explicit z-order and separate overlap lanes.
- Do not duplicate one face merely to fill space. Do not switch crops on every diarized word; change only at a stable speaker or shot boundary.

### `tutorial`

Use for a screen recording that contains or accompanies a presenter.

- Give the screen roughly the upper 62–72% of a 9:16 canvas. Fit/contain it to the available width so menus, code, cursor targets, and text remain readable; blank space is acceptable.
- Give the presenter roughly the lower 28–38%, centered, with a stable `cover` crop on the face. The content copy is audible; the presenter duplicate is muted when both came from the same source.
- If separate screen and presenter items exist, synchronize exact in/out points before arranging them. If the presenter is baked into the screen recording, duplicate the same source range and use source crops to isolate the two regions.
- Use normalized editable containers rather than scale-only transforms. A useful starting geometry on a 9:16 canvas is screen `x=0.04`, `y=0.04`, `width=0.92`, `height=1.12`; presenter `x=0.10`, `y=1.18`, `width=0.80`, `height=0.55`. Treat these as starting points and correct them from rendered pixels.

### `fit_canvas`

Use when showing the full source matters more than filling every pixel.

- Place a contained foreground centered within safe margins.
- If empty space is visually distracting, create an Aura background from a second exact source copy: full-canvas `cover`, centered, `blurPx` around 24–40, `brightness` around 0.45–0.7, `saturate` around 0.7–0.95, behind the foreground, and muted.
- Keep the foreground unblurred and audible. Never let both copies play audio.
- Prefer this mode for software demos, slides, code, dashboards, or landscape UI that a vertical cover crop would destroy.

## Continuity checks

- The first candidate starts at `1.0s`; candidate groups are separated by exactly `2.0s`; constituent pieces inside one candidate have no artificial gap.
- A stable shot keeps identical position, size, focus, crop, and fit across adjacent pieces.
- Split on real shot or speaker changes, not arbitrary face-detection fluctuations.
- Default to hard source cuts with no transition. Do not use motion or J-cuts to conceal mismatched geometry.
- Inspect the first spoken frame, last spoken frame, one frame on each side of every internal boundary, and enough 3–5 second interval samples to prove that a long clip never silently drifts off its speaker or current object of interest.
- Set duration to the final candidate end when it is the last intentional content or for clips-only output. Preserve a later intentional endpoint.
- Re-list items to prove candidate count, the `1.0s` lead-in, `2.0s` gaps, source windows, source-placement removal, caption ownership, hook items, mute policy, lane/z-order, and duration.
