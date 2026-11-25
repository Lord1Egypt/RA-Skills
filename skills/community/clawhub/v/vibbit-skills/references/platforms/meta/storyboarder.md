---
skill_code: VB-04
version: "1.0.0"
---

# Storyboard strategy, frameworks, and categories

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Storyboarder](#storyboarder)
- [5V storyboard frameworks](#storyboard-frameworks)
- [Storyboard category starting points](#storyboard-categories)

<a id="storyboarder"></a>

## Storyboarder

Read [shared boundaries](guidelines.md). Use `generate` for new scripts and `refine` for existing ones. Preserve supplied shots, exact dialogue, ratio, chosen hooks/roles, and user count/duration.

Read [5V frameworks](#storyboard-frameworks) when choosing types or an exploration set. Full 5V gives Hero, Feature, Social, Solution, and Moment with distinct jobs/hooks. A single ad needs only its best-fitting type.

Choose the intended psychological change and audience stage. Differentiate along hook mechanism, visual approach, character voice, format/pacing, and message angle. Use the [category library](#storyboard-categories) only when it affects demonstration/context; unmatched products need their real use case, not a forced category.

Arrange hook, context, reveal/proof, benefit, and action as needed. Longer ads may use opening at 0–2 seconds, change at 5–6, benefit preview at 12–15, and action transition at 20–25; scale or omit beats to fit the real duration. Plan audible and sound-off understanding. Trending audio is a direction, not an available licensed track.

Hero/Feature product exposure, Social's authentic single shot, and Moment's montage need not all become delayed-product fast-cut ads. Every shot should explain what it demonstrates.

<a id="storyboarder-layered-production-cards"></a>

### Layered production cards

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

<a id="storyboard-frameworks"></a>

## 5V storyboard frameworks

Use for [Storyboarder](#storyboarder). Cold/Warm/Hot describe planning stages of familiarity and intent, not verified account audience data. User goals determine the number and adaptation of types.

<a id="storyboard-frameworks-jobs-and-emotional-arcs"></a>

### Jobs and emotional arcs

| Type | Purpose | Audience | Arc |
| --- | --- | --- | --- |
| Hero | Clear product showcase, immediate desire | Cold + Warm | Ordinary → extraordinary |
| Feature | One feature, purchase intent | Warm | Curiosity → satisfaction |
| Social | UGC trust, reduce hesitation | Warm + Hot | Doubt → confidence |
| Solution | Problem/solution, justify a purchase | Cold + Warm | Tension → release |
| Moment | Aspirational life, brand affinity | Cold | Calm → desire |

<a id="storyboard-frameworks-five-axis-differentiation"></a>

### Five-axis differentiation

| Type | Hook | Visual | Voice | Format/pacing | Message |
| --- | --- | --- | --- | --- | --- |
| Hero | Curiosity | Wide/cinematic | Observer/narrator | Gradual reveal | Desire |
| Feature | Rational | Intimate/close-up | Expert | Structured sequence | Education |
| Social | Social | POV/first person | Peer/friend | Authentic single shot | Social identification |
| Solution | Confrontational | Split-screen/contrast | Skeptic to believer | Narrative arc | Solve a problem |
| Moment | Emotional | Multiple angles/montage | Enthusiast | Quick cuts | Emotion/identity |

Different variants should differ substantively, not merely in wording. One ad need not embody every type. Preserve a chosen hook and explain necessary matrix adjustments.

<a id="storyboard-frameworks-sound"></a>

### Sound

| Type | Primary sound | Voice delivery | Music | Sound-off design |
| --- | --- | --- | --- | --- |
| Hero | Cinematic music, sparse voice | Calm authority | Emotional punctuation | Partially understandable |
| Feature | Explanatory voice | Warm conversation | Background mood | Captions needed |
| Social | Authentic original voice | Energetic | No added music | Plan readable visuals/text |
| Solution | Optional trending sound/text | Deadpan | Rhythm | Plan readable visuals/text |
| Moment | Texture/ASMR/ambience | Intimate | Background mood | Partially understandable |

Trending sound is an optional direction, not permission or an asset. “No added music” does not remove original speech. Verify sound-off understanding on the actual result.

<a id="storyboard-frameworks-eight-hook-archetypes"></a>

### Eight hook archetypes

| Hook | Mechanism | Constraint |
| --- | --- | --- |
| Problem–agitate–solve | Real difficulty, consequence, solution | Ground relevance; no invented fear |
| Curiosity/suspense | Hold one specific fact for a reveal | Resolve the opening |
| Social proof/authority | Credible experience or evidence | Real sales, endorsements, credentials |
| Personal story | Concrete experience and change | Fiction is not a customer testimonial |
| Relatability | Familiar target-audience moment | Avoid unsupported universality |
| Bold claim | Specific, provable unexpected benefit | Stay within evidence |
| Transformation | Compare states/results | Valid conditions; no fabricated efficacy |
| Question | Relevant real-life question | Give a clear answer |

A full five-ad exploration uses different hooks unless the user explicitly wants controlled variants of one hook.

<a id="storyboard-categories"></a>

## Storyboard category starting points

Read the relevant row for [Storyboarder](#storyboarder). Numbers are exploratory creative presets, not conversion guarantees. Product evidence, 5V choice, market, user needs, and model limits take priority. “Watch for” describes potential mismatch in that route, not a ban on studios, specs, or app UI.

| Category | Hook/person | Setting and product reveal | Pace/duration starting point | Sound | Watch for |
| --- | --- | --- | --- | --- | --- |
| Fashion | Personal story/transformation; peer or moving model | Street/cafe/getting ready/mirror; product 0–2s | 15–20 cuts per 30s; 15–20s ad | Optional trending track/text; fabric, zipper, footsteps | Static catalog feel, no opening action, too many outfits |
| Beauty | Proof/transformation/curiosity; hands/skin/application/expert | Bathroom/vanity/routine; product 3–6s | 10–15 cuts per 30s; 20–30s ad | ASMR/soft voice; clicks, liquid, tapping | Extreme macro without context, stock feel, absent human use |
| Food/drink | Question/relatability/curiosity; hands or person enjoying | Kitchen/table/picnic/snack; product 0–3s | 20–25 cuts per 30s; 15–20s ad | Food sounds/optional music; pouring, sizzling, fizz, unwrap | No early food, flat packshot, no sensory moment |
| Technology | Question/provable claim/PAS; hands/problem-solution | Desk/commute/cafe/home office; Hero early, Solution later | 15–18 cuts per 30s; 25–30s ad | Explanatory voice/product clicks, notifications, typing | Context-free specs, static product, feature overload |
| Home | Transformation/curiosity/relatability; arranging/using | Room/daylit living space/shelf; product 3–6s | 10–15 cuts per 30s; 20–25s ad | Ambience/soft voice/text; ceramic, fabric, water, wood | No scale, context, or human interaction |
| Automotive/luxury | Supported bold claim/story/curiosity; driver/silhouette | Architecture/road/night/garage; gradual 5–10s reveal | 8–12 cuts per 30s; 25–30s ad | Engine/cinematic music, sparse voice; door, road, leather | Catalog-only profile or misplaced spec/price emphasis |
| Finance/apps | Relatable story/PAS; person/over-shoulder phone | Real everyday context; product 6–12s | 15–18 cuts per 30s; 25–30s ad | Conversational voice/uplifting bed; app cue | Corporate stock feel, UI without meaning or emotion |
| Gaming | Claim/question/proof; player reaction/gameplay | Gaming area/sofa/split screen; gameplay 0–2s | 22–30 cuts per 30s; 15–20s ad | Game audio/reactions; controller/achievement cues | No early gameplay, trailer-only footage, absent reactions |

Adapt unsuitable environments and audio to the brand. Financial outcomes, beauty transformations, and product claims need real evidence. Do not force an unmatched product into a category.
