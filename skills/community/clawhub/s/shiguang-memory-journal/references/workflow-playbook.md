# Workflow playbook

## Contents

1. Intake and capability mapping
2. Source ledger
3. Element planning and redraw
4. Content materials and optional layout reference
5. Story, copy, paper, and layout
6. Multi-pass review
7. Journal and collection management
8. Archive, recall, and return
9. Degraded modes

## 1. Intake and capability mapping

Collect only what changes the result:

| Input | Rule |
| --- | --- |
| Key frame or images | Required for visual execution; otherwise produce an implementation template |
| Source link | Optional; preserve supplied HTTP(S) links, otherwise mark unavailable and continue |
| Extraction style | `handdrawn`, `comic`, `collage`, or `realistic`; the style changes rendering, never identity, count, pose, provenance, or the chosen background mode |
| Element count | User-controlled integer 1–5; default 1 when omitted |
| Background strategy | `subject-only` isolates every subject; `preserve-context` keeps every subject with meaningful environment; `mixed` assigns an explicit range to each element from the user's intent |
| Journal type | `portrait`, `pet`, `travel`, `game`, `life`, `fashion`, or `food` |
| Intention | A short thematic spine such as “诗与远方” |
| Factual notes | Optional verified places, dates, prices, steps, names, or feelings |
| User story | Optional first-priority factual and narrative source; always score, refine, and select before layout |
| Composition materials | 1–12 user-approved images or reusable elements |
| Layout reference | Optional; structural inspiration only, never an implicit content asset |
| Review mode | `one-shot` or `interactive`; interactive pauses after reference, story, layout, and rendered review |
| Collection action | Optional search, filter, quick edit, reopen, single delete, or bulk delete |
| Output | Editable canvas, image, document, web page, JSON plan, or agent handoff |

Map the current environment to seven capability roles: inspect, redraw, compose, persist, retrieve, manage collections, and present source links. Prefer tools already available to the agent. Do not require a particular vendor or API.

Choose an execution mode:

- **Full execution:** all six roles are available.
- **Creative execution:** inspect, redraw, and compose are available; also output a portable archive manifest.
- **Planning mode:** visual or layout tools are missing; output exact prompts, element plan, story plan, and layout specification.
- **Recall-only mode:** archive data already exists; rank it and surface source links.
- **Management-only mode:** saved records already exist; search or mutate them by stable ID without invoking visual generation.

## 2. Source ledger

Create the source record first. Assign stable IDs before generating derived items.

For each transformation, keep:

- parent source ID;
- original source URL when supplied, otherwise an explicit unavailable value;
- operation (`inspect`, `redraw`, `crop`, `reference-analyze`, `compose`, `edit`, `delete`, `archive`, or `recall`);
- prompt or decision summary;
- tool/model when known;
- warnings and missing facts.

Never replace the source link with the generated image URL. The first supports “return to original”; the second only locates a derivative. A missing source link is valid input and must not block element planning, redraw, composition, or archive creation.

## 3. Element planning and redraw

### Select subjects

Rank visible candidates by:

1. relevance to intention;
2. recognizable silhouette;
3. visual clarity;
4. difference from already selected subjects;
5. contribution to hero, support, transition, detail, or ending.

Select exactly the requested count. In fixed subject modes, do not pad the set with platform UI, subtitles, watermarks, generic background, or duplicate views of the same subject. In `mixed`, a background region is valid only when it is visually meaningful and intentionally assigned `background-only`.

### Choose the background mode

Choose one task-level strategy:

- `subject-only`: keep the complete subject and remove unrelated scenery. Prefer transparency when supported, otherwise a removable flat background.
- `preserve-context`: keep one clear primary subject together with the visible background needed to understand where it is, what it touches, or how it relates to the scene. Preserve spatial, action, and narrative connections such as a person with the counter they are serving across, a vehicle with the road it is traveling on, or a building with the surrounding riverbank. Remove platform UI and unrelated scenery, but do not flatten the result into an isolated sticker.
- `mixed`: requires at least two elements. Give every element its own mode: `subject-only`, `preserve-context`, or `background-only`. Parse numbered or itemized user intent first; when the user names a mode, the matching output must use it. If no per-element intent exists, distribute at least two useful modes based on the visible story.

`background-only` is an element-level mode inside `mixed`, not a standalone task option. It keeps a meaningful environment or architecture region and removes foreground people or objects that the user excluded. Do not infer `preserve-context` merely because a source contains a rich background. Use the user's choice; default to `subject-only` when no choice is supplied.

### Redraw

Use one visual generation/editing call per planned element when possible. This preserves independent assets and makes later layout editing reliable.

Keep in every mode:

- identity-defining contour and colors for subject-bearing elements;
- a complete subject or coherent environment region rather than arbitrary circular crops;
- coherent style across the set;
- the selected background mode on every derived element and archive record.

For `realistic`, preserve photographic light direction, skin, fabric, surface texture, lens perspective, identity, people count, pose, and spatial relationships. Limit beautification to restrained composition, exposure, tonal balance, and material clarity. Reject plastic skin, face substitution, body reshaping, aggressive HDR, synthetic 3D surfaces, invented people, or any output whose aesthetic improvement changes visible facts.

For `subject-only`, use a transparent background when supported, otherwise a removable flat background. For `preserve-context`, keep the necessary environment as a complete element image and reject results that isolate the subject or lose its visible relationship to the scene. For `background-only`, reject results that keep the excluded foreground subject or replace the requested place with generic scenery.

Keep the natural canvas orientation of a valid redraw. Portrait, landscape, and square are all acceptable; only crop, pad, or force an aspect ratio when the user explicitly asked for one or the chosen output medium has a declared hard requirement.

Reject outputs that introduce competing subjects, readable fake text, platform logos, frames, mockups, or unrelated scenery. Contextual people or objects may remain only when they visibly participate in the selected subject's relationship. If only cropping is possible, record `generationMode: crop`.

## 4. Content materials and optional layout reference

### Approve content materials

For automatic composition, let the user choose 1–12 content materials from the current task, canvas, or reusable library. Record stable IDs and provenance before layout. Use only approved materials and do not silently import visually similar items.

### Isolate the reference

Store an optional reference journal under `layoutReference`, never inside `elements` or `contentMaterials`. Analyze:

- composition model and reading path;
- hero placement and relative scale;
- image and text zones;
- whitespace strategy;
- overlap, tape, line, or rhythm relationships;
- abstract paper and palette relationships only when explicitly allowed.

Do not extract or copy the reference's photographs, people, food, objects, landmarks, brands, readable text, captions, dates, prices, or factual claims. Do not recreate exact coordinates. Convert the analysis into constraints for the user's approved materials.

Record both:

- `focus`: what the user wants to learn from the reference;
- `restrictions`: what must not transfer.

If the reference is unavailable to the visual tool, continue with the chosen style profile and disclose that no reference analysis was executed.

## 5. Story, copy, paper, and layout

### Story pass

Before coordinates, assign:

- `hero`: the page's first visual answer;
- `support`: evidence or context;
- `transition`: movement between moments;
- `detail`: texture and intimacy;
- `ending`: a quiet return, decision, or next step.

With fewer elements, combine roles. With five elements, use all roles only when the content supports them. Define a top-to-bottom, diagonal, S-shaped, timeline, or grid reading path according to the journal type. When a layout reference exists, adapt its abstract reading logic to the current story rather than cloning positions.

If the user supplied a story, read it completely before using filenames, inferred scene labels, generic type templates, custom visual instructions, or reference analysis as narrative input. Return:

- a source marker (`user-story` or `visual-inference`);
- factual-fidelity, narrative-structure, and sentence-selection scores;
- editing notes that explain removal, reordering, and compression;
- retained facts that the final copy may not lose.

Low scores require editing, not replacement. Preserve key events, people relationships, turns, concrete actions, and the user's closing meaning. Let visual imagination affect rhythm and phrasing without changing facts.

### Copy pass

For rich life records, aim for 6–10 blocks:

- 30–70 Chinese characters for the opening;
- 18–55 near each important image;
- 55–130 for one reflective paragraph;
- 20–60 for the closing;
- one or two short marginal notes.

Use fewer blocks for portrait pages and more structured labels for guides. Copy may interpret visible mood and user-provided intention, but must not fabricate personal experience. Use explicit uncertainty such as “画面让人想到” when the meaning is inferred.

For each block, optionally select 0–2 highlight phrases that appear verbatim in its text. Prefer real numbers, distances, people counts, achievements, turns, or distinctive original wording. Do not highlight every paragraph.

Design typography with the copy rather than after it. Specify font family, size, weight, tracking, leading, alignment, container treatment, and contrast. Use at least three sizes and two font voices on a rich editorial page; reserve display or handwritten emphasis for titles, labels, marginalia, and the closing line rather than rendering all copy as one small caption style.

### Paper pass

Describe paper independently from the images:

- material and texture;
- palette;
- edge decoration;
- reserved blank areas;
- forbidden motifs;
- relation to the intention.

The center should support content rather than compete with it. When “诗与远方” involves mountains, sky, roads, or distance, prefer mist blue, mountain green, warm dawn white, fine route lines, and restrained horizon texture—not food-table remnants.

### Layout pass

Use the user's requested ratio or the supplied target/reference render's natural ratio when either is explicit. Otherwise use a mobile-first 3:4 portrait canvas. Never crop a valid target into the default ratio merely for implementation convenience, and never lengthen the page merely because the material count increased. Establish:

- one large hero;
- 3–4 narrative groups rather than an even card stream;
- two medium supports when assets allow;
- smaller details;
- a lower-page emotional anchor that is visibly larger than nearby details;
- at least 20% breathing room for a life record;
- text attached to the images it explains;
- safe title and footer zones;
- paper or Polaroid frames for most contextual images and roughly 1–3 tape accents;
- purposeful overlap without hiding subjects.

When transparent people are available, enlarge them enough to contribute visual impact and let them bridge adjacent contextual images with roughly 4%–16% coverage. A cutout may connect more than one image only when each lower image remains readable. Never cover a person, essential scenery, or text in a lower image. Keep cutouts unframed and prefer moving a contextual image before moving the main people group during local repair.

Never place all items at nearly equal size or distribute them evenly into four corners. Never replace an approved content material with an object seen only in the reference.

### Target reconstruction and layer recovery

When the user asks to open a specific finished effect as an editable journal:

1. treat the finished image as the initial-render target, not as a recoverable source of hidden pixels;
2. inventory the base, photo cards, cutout people, text/decorations, and expected people count;
3. keep the original source images beside the derived layer assets;
4. create a clean base by removing every independently editable region with the same masks used for the layer assets;
5. assign shared or overlapping pixels to the top visible layer so lower layers do not contain a duplicate person or neighboring card;
6. reconstruct the target from the saved layers and compare it with the finished target before import;
7. store explicit canvas width and height and verify the real editor at desktop and mobile widths;
8. export both a flattened preview and a versioned structured project whose embedded or resolvable assets complete a round trip.

If hidden portions cannot be recovered from the finished target, keep the original full source image and mark the placed layer as a visible-region reconstruction. Do not invent hidden faces or people.

## 6. Multi-pass review

Use separate calls or roles when available:

1. **Visual analyst:** candidate subjects and factual observations.
2. **Story director:** roles, sequence, art direction, and copy responsibilities.
3. **Element artist:** independent redraws.
4. **Paper artist:** theme-specific background.
5. **Layout composer:** editable coordinates and render.
6. **Visual critic:** direct inspection of the complete render.
7. **Refiner:** focused correction of failed dimensions.

Score each dimension from 1–10:

- story coherence;
- richness and relevance of copy;
- typography: font family, size, weight, tracking, leading, alignment, containers, and contrast;
- visual hierarchy;
- paper-theme fit;
- legibility and whitespace;
- element fidelity;
- factual integrity;
- provenance completeness.
- reference safety and content/reference separation.
- people-count integrity and overlap ownership when people or reconstructed layers are present.
- realistic-material integrity when any element uses `realistic`: natural light and materials survive without identity, anatomy, count, or relationship drift.

Revise any dimension below 7. Prefer one focused revision and at most two critique cycles unless the user requests deeper exploration. Preserve the latest valid result if a later call fails.

Reject a rendered page that still behaves like a photo wall: a detached title and hero, evenly distributed cards, no cross-layer connection, or no lower-page anchor. When the critique returns a structurally strong revision but deterministic checks find only a small excess overlap or text collision, apply the smallest local movement, run text avoidance, and validate again. Do not discard the entire AI composition for a one-point threshold miss. Use full safe-layout fallback only for missing assets, identity or people-count errors, collapsed hierarchy, unsafe reference transfer, or unresolved structural failure.

In `interactive` mode, expose a durable checkpoint after:

1. reference analysis;
2. story assessment and selected copy;
3. editable layout draft;
4. rendered visual critique.

Each checkpoint must show the current result, stage summary, warnings, and a stable continuation token or session ID. `approve` advances; `revise` reruns only the current stage with the user's feedback. Preserve completed stages and the latest valid render across timeout or retry.

Set timeout budgets per expensive structured stage rather than for the whole product flow. Keep visible progress or heartbeats, preserve checkpoints, and distinguish a still-running model from a failed process. A longer limit can solve valid slow inference; it cannot repair authentication failure, unreadable assets, schema-invalid output, or a hung process.

## 7. Journal and collection management

Keep the rendered preview and editable journal record together. Support:

1. browse with faithful thumbnails;
2. full-text search across title, subtitle, place, date, tags, artistic copy, story nodes, and element descriptions;
3. type filters plus clear “all” and “unclassified” states;
4. sorting by recent/oldest update, title, or content count;
5. quick edit of title, subtitle, place, date, tags, and journal type;
6. reopen for full image, text, layout, and source-link editing;
7. import a portable structured journal as a new stable record without overwriting the current collection item;
8. export editable structure with embedded or resolvable assets so it can complete a round trip;
9. import a flattened image only as one editable visual or a background, with a visible explanation that its original layers cannot be recovered;
10. explicit single and bulk deletion.

Before accepting a structured import, validate schema version, field bounds, image protocols, source-link protocols, element counts, explicit canvas width/height, canvas bounds, and per-asset size limits. Persist embedded assets before saving the journal record; do not store temporary `blob:` URLs. Generate a new journal ID on user-initiated import, retain original provenance separately, and leave source links empty when they were not supplied.

For deletion:

- resolve stable IDs, not visible indexes;
- preview or state the number of selected records;
- require confirmation immediately before mutation;
- remove journal records and stale archive links;
- remove archived JSON, snapshots, and backgrounds only when no surviving journal references them;
- keep unrelated source frames and derived elements unless explicitly selected;
- record deleted IDs and failures;
- use tombstones or equivalent suppression when automatic backfill could recreate intentionally deleted records.

Apply the same trust model to library and memory collections: text edits should refresh searchable content, and batch deletion should affect only explicit selections.

## 8. Archive, recall, and return

Archive a portable manifest beside the rendered result. Include the source record, elements, prompts, story, layout, warnings, and source links.

Build searchable text from:

- user intention and verified notes;
- visible subjects, colors, atmosphere, and actions;
- story and captions;
- journal type and style;
- source title or domain when known.

For recall, accept natural language such as “雨后骑车去山里的那一页”. Rank by semantic relevance, explain the match, and do not treat similarity as proof.

The final result should show:

1. remembered item and preview;
2. why it matched;
3. related journal or elements;
4. unique original source links when available, otherwise a visible unavailable state;
5. a clear return action or next real-world action.

## 9. Degraded modes

| Missing role | Deliver instead |
| --- | --- |
| Visual inspection | Ask for descriptions or provide an analysis checklist |
| Image generation/editing | Provide one redraw prompt per planned element |
| Layout renderer | Provide coordinates, z-order, typography, and responsive rules |
| Durable storage | Return a portable manifest and recommended folder structure |
| Semantic engine | Use weighted keyword/fuzzy matching and disclose the fallback |
| Collection manager | Return stable-ID edit/delete commands or a dry-run mutation plan; do not claim persistence |
| Link navigation | Print validated source links without opening them; when none were supplied, report unavailable and continue |

Always distinguish a completed artifact from a handoff specification.
