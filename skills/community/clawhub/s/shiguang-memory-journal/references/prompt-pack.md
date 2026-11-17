# Tool-agnostic prompt pack

Replace bracketed variables and adapt output format to the current agent's tools. Keep provenance fields even when a tool cannot emit structured JSON directly.

## 1. Visual analyst

```text
Inspect [KEY_FRAME] as evidence, not as a source of invented facts.
User intention: [INTENTION]
Requested element count: [COUNT, integer 1–5]
Task background strategy: [subject-only, preserve-context, or mixed]

List distinct visible subjects and, only for mixed tasks that request them, meaningful
environment regions. Exclude platform UI, subtitles, watermarks, avatars, buttons,
playback icons, and meaningless background. Select exactly [COUNT] elements.
For mixed tasks, parse numbered user instructions and assign each element one explicit
mode: subject-only, preserve-context, or background-only. Use at least two modes.
Optimize for intention relevance, recognizable silhouette or scene structure, visual clarity,
variety, and complementary story roles. For each selected element return:
id, visible evidence, crop/location hint, key shape and colors, proposed story role,
element background mode, redraw risks, and original source link [SOURCE_URL or unavailable].
Mark every inference explicitly.
```

## 2. Single-element redraw

Run once per selected element:

```text
Use [KEY_FRAME or SUBJECT_REFERENCE] only as visual evidence.
Redraw exactly one element: [ELEMENT_DESCRIPTION].
Style: [hand-drawn cartoon / comic highlight / vintage collage / realistic texture].
Element background mode: [subject-only, preserve-context, or background-only].
Preserve identity-defining contour, proportions, colors, and important visible details.
Keep the complete subject or coherent scene region as an independent editable keepsake.
Keep a natural portrait, landscape, or square canvas for the content. Do not force 1:1 unless
the user explicitly requested it.
Always remove platform UI, subtitles, watermarks, readable fake text, logos, and unrelated scenery.
If the mode is subject-only, remove the background and use transparency when supported,
otherwise use a uniform removable background.
If the mode is preserve-context, keep the visible environment that directly explains where
the subject is, what it touches, or how it relates to the scene. Preserve spatial, action,
and narrative connections as one complete element image; do not replace them with a flat background.
If the mode is background-only, keep the requested environment or architecture as the subject
of the element and remove foreground people or objects the user excluded. Do not invent a new place.
If the style is realistic texture, preserve photographic light direction, skin, fabric, surfaces,
lens perspective, identity, people count, pose, and scene relationships. Limit refinement to
restrained composition, exposure, tonal balance, and material clarity. Reject plastic skin,
face replacement, body reshaping, aggressive HDR, synthetic 3D surfaces, or invented people.
Do not create a photo crop, circular frame, mockup, or competing additional subject.
Do not claim unseen details.
```

## 3. Layout-reference analyst

Run only when the user selected a separate reference:

```text
Inspect [LAYOUT_REFERENCE] only as structural design evidence.
User-approved content materials: [CONTENT_MATERIAL_IDS]
User focus: [REFERENCE_FOCUS]
Explicit restrictions: [REFERENCE_RESTRICTIONS]
Mode: [LAYOUT_ONLY or ALLOW_ABSTRACT_DECORATION]

Return only transferable composition guidance: reading path, hero strategy,
relative scale, image zones, text zones, whitespace, overlap rhythm, and hierarchy.
In ALLOW_ABSTRACT_DECORATION mode you may also describe non-identifying paper,
tape, line, and palette relationships.

Do not extract, reproduce, identify, or restate any photograph, person, food, object,
landmark, brand, readable text, date, price, place, or factual claim from the reference.
Do not copy exact coordinates. Do not add the reference to the content material list.
Explain how to adapt the abstract structure to the approved materials.
```

## 4. Story director and copywriter

```text
Plan a [JOURNAL_TYPE] journal from these approved elements: [ELEMENT_MANIFEST].
The thematic spine is [INTENTION]. Verified notes: [FACTS].
User story: [USER_STORY or none].
Optional safe layout analysis: [LAYOUT_REFERENCE_ANALYSIS or none].

When USER_STORY exists, read it completely and treat it as the first-priority factual
and narrative axis. Before writing copy, return source, factual-fidelity score,
narrative-structure score, sentence-selection score, editing notes, and retained facts.
Remove repetition, refine, and compress; never replace its key events, relationships,
turns, actions, or closing meaning with generic template prose.
First assign hero, support, transition, detail, and ending roles as the content supports.
Define a readable path and explain why adjacent elements belong together.
Then write layered, factual copy appropriate to the type. For a rich life record,
include an opening, image-linked notes, one reflective paragraph, marginalia, and closing.
For each copy block, select 0–2 highlight phrases that occur verbatim in its text.
Prefer real numbers, distances, people counts, achievements, turns, or distinctive wording.
Recommend a font role, weight, scale, leading, alignment, and container for each responsibility.
Never invent an event, place, date, relationship, price, recipe, game fact, health claim,
or user feeling. Phrase interpretation as interpretation.

Return a story plan, ordered element IDs, copy blocks with target roles,
paper art direction, palette, forbidden motifs, and factual-risk notes.
```

## 5. Theme-specific paper

```text
Design only the background paper for a [FORMAT] journal.
Journal type: [TYPE]
Intention: [INTENTION]
Story direction: [STORY_SUMMARY]
Palette/material: [PALETTE_AND_TEXTURE]

Keep the central content field calm and usable, with restrained edge texture and
intentional blank areas. Support the story without depicting or replacing user elements.
If the reference uses a dark or saturated paper, preserve that value relationship instead
of washing it into pale pink. Prefer subtle fiber, grain, arcs, or edge marks over
presentation-style gradients and geometric panels.
Forbid: [OLD_OR_UNRELATED_MOTIFS], readable fake text, logos, frames, stock-photo scenes,
and decoration that competes with the hero. The paper must express this intention rather
than inherit a previous theme.
```

## 6. Layout composer

```text
Compose an editable [FORMAT] journal using exactly these approved element IDs once:
[ELEMENTS]. Use this story plan: [STORY_PLAN] and copy: [COPY_BLOCKS].

Derive the canvas ratio from an explicit target or reference before material count.
More assets do not justify an unsupported long page. Create 3–4 narrative groups,
one large hero, medium supports, smaller details, a lower-page emotional anchor,
a clear reading path, safe title/footer zones, and intentional whitespace.
Attach text to the image it explains.

For contextual images choose frameStyle none/paper/polaroid; frame most contextual images
on an editorial scrapbook and use tapeStyle none/top/corner on roughly 1–3 accents.
Keep transparent cutouts unframed. Let transparent people overlap contextual images by
roughly 4%–16% to connect groups, but never cover people, essential scenery, or text.
Do not generate replacement images, duplicate assets, equalize all sizes, scatter items
into unrelated corners, or introduce content visible only in an optional layout reference.

Return canvas dimensions, x/y/width/height, rotation, z-order, element role,
frameStyle, tapeStyle, text font family/size/weight/tracking/leading/container/alignment,
and responsive or export notes.
```

## 7. Visual critic

```text
Inspect the complete rendered journal [RENDER], not only its coordinates.
Compare it with [INTENTION], [STORY_PLAN], [ELEMENT_MANIFEST], [SOURCE_LEDGER],
and [LAYOUT_REFERENCE_ANALYSIS or none].

Score 1–10: story coherence, copy richness/relevance, typography, visual hierarchy,
paper-theme fit, legibility/whitespace, element fidelity, factual integrity,
provenance completeness, and reference safety. Cite visible evidence for each score.
For typography, inspect font family, size, weight, tracking, leading, alignment,
container, contrast, and whether the closing line creates a real endpoint.
Reject a page that still reads as a uniform photo wall: detached title/hero, evenly
distributed cards, no cross-layer connection, or no lower-page anchor.
Verify that every element follows its recorded background mode: subject-only elements are isolated,
preserve-context elements retain the necessary visible environment without unrelated scenery,
and background-only elements retain the requested environment without excluded foreground subjects.
For realistic-texture elements, verify natural light, skin, fabric, surfaces, lens perspective,
identity, count, pose, and spatial relationships; reject beauty, HDR, or 3D treatment that changes facts.
For mixed tasks, verify that at least two element-level modes are present and every mode explicitly
requested in the user's numbered intent appears in the result.
If a reference exists, verify that only abstract structure transferred and that no
reference-only image, person, object, text, brand, place, or claim entered the result.
For every score below 7, propose one focused correction with exact affected IDs,
copy blocks, or regions. Preserve already strong dimensions.
If the composition is strong and only one or two small geometry or text conflicts remain,
return the smallest local movement needed. Do not replace the whole layout.
```

## 8. Focused refinement

```text
Revise only these failed dimensions: [FAILED_DIMENSIONS].
Apply these exact corrections: [CORRECTIONS].
Preserve approved source elements, factual copy, provenance, and all dimensions
scored 7 or higher. Return the complete revised layout or artifact plus a concise diff.
```

## 9. Interactive checkpoint

```text
Current stage: [reference, story, layout, or review].
Current structured result: [STAGE_RESULT].
Current preview when available: [PREVIEW].
Warnings: [WARNINGS].

Return a concise user-facing checkpoint with what was decided, what remains editable,
and the exact result that will be carried forward. Preserve a stable session or continuation
identifier. The next action is either approve or revise-current-stage with user feedback;
do not restart completed stages unless the user explicitly requests it.
```

## 10. Poster typography director

Use after a text-free key-art winner exists. Read [poster-typography.md](poster-typography.md) first.

```text
Design editable typography for [KEY_ART] using the exact approved strings [TITLE] and [SUBTITLE].
Story promise: [DRAMATIC_PROMISE]. Emotion and memory hook: [EMOTION_AND_HOOK].
Protected faces/objects, gaze/body vectors, perspective axes, low-detail regions and local luminance:
[KEY_ART_ANALYSIS]. Optional reference TypographyDNA: [REFERENCE_DNA or none].

Return at least three structurally different candidates: monumental wordmark, editorial restraint,
and integrated/material title. They must differ in black-and-white title silhouette and type–image
relationship, not only font or color. For each return semantic line breaks, relation (crown/anchor/
hinge/blade/seal/whisper/weave), normalized region, font role, scale, width, weight, tracking, leading,
alignment, editable effect, support hierarchy, local contrast strategy, reference mechanisms used,
and a story-grounded rationale. Reference text, exact commercial wordmarks and absolute coordinates
are forbidden. You may break one soft convention when you explain why it improves the story.
Do not alter, omit, translate, or invent a single title character.
```

## 11. Poster typography critic

```text
Compare [TYPOGRAPHY_CANDIDATE_RENDERS] against [KEY_ART], [APPROVED_STRINGS], [STORY_BRIEF],
[PROTECTED_REGIONS], and [REFERENCE_TYPOGRAPHY_DNA or none]. Inspect full size, 180×320,
90×160, and black-silhouette versions.

Hard-fail inaccurate/missing/clipped glyphs, bad semantic breaks, orphan glyphs, unavailable fonts,
protected face/action/object occlusion, unsupported story promise, local contrast failure, reference
OCR/wordmark leakage, raster-title OCR mismatch, or cross-render differences. Then pairwise rank passing
candidates by story fit, thumbnail recognition, type–image integration, silhouette memory and compatible
reference alignment. Do not reward a beautiful background for weak type. Return the winner, runner-up,
focused repair, exact hard failures and evidence for every judgment.
```

## 12. Semantic recall

```text
Query: [NATURAL_LANGUAGE_MEMORY]
Candidates: [MEMORY_INDEX]

Rank by meaning, objects, atmosphere, colors, actions, intention, and story—not exact
keywords alone. Return the best matches with a brief reason, ranking score,
preview/artifact reference, memory ID, and unique original source URLs.
If a candidate has no original source URL, return an explicit unavailable value and the next action.
Treat scores as ranking signals rather than factual confidence.
```

## 13. Journal collection organizer

Use for search and metadata suggestions. Perform deletion only through a separate confirmed mutation:

```text
User request: [COLLECTION_REQUEST]
Saved journal summaries: [JOURNAL_INDEX]

Search across title, subtitle, place, date, tags, artistic copy, story nodes,
and element descriptions. Return stable journal IDs, match reasons, suggested filter,
sort order, and any metadata edits as a proposed patch.

Never infer deletion from a filter, low score, duplicate-looking preview, or stale date.
For single or bulk deletion, first return the exact selected IDs, count, archive effects,
and confirmation question. After explicit confirmation, report deleted IDs, failed IDs,
unlinked archive records, and shared assets intentionally preserved.
```
