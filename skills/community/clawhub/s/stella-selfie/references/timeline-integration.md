# Timeline Integration for Stella

Load this document only when `timeline_resolve` is available in the current environment and either:

- the current selfie request is `Sparse`, or
- the current selfie request clearly refers back to a single recently resolved timeline scene in the current conversation.

If `timeline_resolve` is unavailable, fails, times out, returns `fact.status === "empty"`, or does not contain usable `result.consumption`, skip this document and continue with Stella's default prompt behavior from `SKILL.md`.

## Compatibility Boundary

- `timeline_resolve` is optional. Stella must work normally without it.
- Timeline enhancement is best-effort only.
- Never refuse, delay, or noticeably degrade image generation because timeline context is missing.
- Never introduce a hard dependency on timeline-specific env vars, install steps, or internal field paths.

## Eligibility

Use this document in exactly two cases:

- `Sparse current-state requests`: the user asked for a photo without a clear scene, outfit, location, activity, or camera requirement.
- `Recent-scene callbacks`: the user is clearly asking for a photo of a scene that was just resolved through Timeline in the current conversation.

Typical Sparse current-state requests:

- “发张自拍”
- “发张照片”
- “想看看你”
- “send a selfie”
- “send a photo”
- “show me what you look like”

Typical recent-scene callbacks:

- “发一张你打球时的照片”
- “刚才那个场景来一张”
- “昨天上午那个状态发张照片”
- “show me a photo from that scene”

Standalone non-Sparse requests do **not** use timeline enhancement, even if timeline is available.

Typical standalone non-Sparse requests:

- “发张海边的自拍”
- “发张穿红裙子的自拍”
- “发张窗边的自拍”
- “send a mirror selfie in a black dress”
- “show me a third-person photo at the beach”

## Stable Input Contract

Use only `result.consumption` from timeline output.

Primary visual anchor:

- `consumption.selfie_ready`

Optional enhancement fields:

- `consumption.scene.city`
- `consumption.scene.calendar_date`
- `consumption.scene.local_timestamp`
- `consumption.scene.timezone`
- `consumption.scene.location_props`
- `consumption.scene.lighting_hint`
- `consumption.scene.framing_hint`
- `consumption.scene.activity_mode`
- `consumption.scene.continuity_relation`
- `consumption.scene.environment_mood`
- `consumption.scene.social_context`
- `consumption.scene.appearance_change_expected`
- `consumption.scene.appearance_change_reason`
- `consumption.fact.continuity`

Do not rely on:

- `episodes[0]`
- `state_snapshot`
- `trace`
- `notes`

## Timeline Role

Timeline is a fact-grounding layer for current-state Sparse requests and explicit callbacks to recently resolved scenes.

Use it to:

- recover a believable current scene from `result.consumption`
- supply concrete place / date / time anchors
- support realistic weather / lighting / indoor-outdoor coherence
- enrich mood, social context, and continuity details
- unlock Nano Banana real-world grounding when city plus exact local date/time anchors are available

Timeline does not own selfie semantics in general. Stella still owns the capture strategy and final prompt assembly.

Structured fields and natural-language fields may both influence the decision. When a natural-language field is decisive, rely on LLM semantic understanding rather than hardcoded script logic.

## Merge Strategy

Treat timeline as a reality anchor layer, not the source of truth for everything.

Priority order for eligible requests:

1. User's explicit wording, if any
2. the most recent relevant Timeline `result.consumption`, when the current request clearly refers back to it
3. `consumption.selfie_ready`
4. `consumption.scene`
5. Stella's default fallback heuristics

Merge rules:

- Use `selfie_ready` as the base prompt skeleton when present.
- Use `scene` to enrich missing reality details such as city, time, props, lighting, mood, and continuity-friendly appearance details.
- Do not invent exact real-world synchronization unless city plus exact local date/time anchors are present.

## Recent Scene Reuse

If the current conversation already contains a single recent successful Timeline result, and the user is clearly asking for a photo of that same scene, do not call `timeline_resolve` again.

Reuse the most recent relevant `result.consumption` directly when all of the following are true:

- the prior Timeline result succeeded and contains usable `consumption.selfie_ready` or `consumption.scene`
- the current request clearly refers back to that scene
- there is only one plausible recent scene candidate
- the conversation has not drifted to a different event

If any of those checks fail, do not guess. Either fall back to Stella's normal explicit-scene behavior, or call `timeline_resolve` using the query strategy below.

## Timeline Query Strategy

If you need a fresh Timeline call, use one of these paths:

1. Current-state Sparse request:
   Use the fixed query `现在`.

2. User-provided time or scene wording:
   Pass the user's exact wording through when it already contains the needed time or event anchor.

3. Elliptical callback without enough wording:
   Build a minimal natural-language anchor query that preserves only `你` plus the time anchor or event anchor.

Allowed minimal-anchor examples:

- `昨天上午你打球时的场景`
- `刚才那个场景`
- `你昨天上午那个状态`

Forbidden query rewrites:

- do not introduce names such as `小刘`, `Leon`, or other third-person substitutions
- do not expand into output-slot questions such as `你在哪`, `穿什么`, `看起来怎么样`
- do not inject a new time anchor such as `今晚九点左右` unless the user explicitly asked for that time
- do not rewrite a callback into a different subject

## Capture Strategy

When an eligible request enters timeline enhancement, let the recovered scene guide the most natural capture strategy:

- prefer `mirror` when the recovered scene naturally supports self-presentation or reflective capture
- prefer `direct` when the recovered scene feels naturally handheld and immediate
- for requests explicitly asking for a selfie, do not switch to `third_person`; keep the image selfie-coded even when the recovered scene is weakly staged

Do not encode brittle hard mappings such as “fresh moment means mirror.”

## Outdoor and Real-World Awareness

This is the main place to use Nano Banana's real-world perception for eligible requests.

Classify the scene into one of these buckets:

- `outdoor`: the subject is actually outside
- `indoor_with_outdoor_view`: the subject is inside but outdoors is visibly present through a window, balcony, terrace opening, train window, cafe window, etc.
- `indoor_closed`: the subject is in a normal enclosed interior without meaningful outdoor visibility

Signals can come from:

- `selfie_ready.location`
- `scene.location_props`
- `scene.framing_hint`
- natural-language semantic interpretation of the recovered scene

### Outdoor

When the scene is truly outdoor, and `scene.city` plus either `scene.calendar_date` or `scene.local_timestamp` are available:

- explicitly inject the city and an exact local date/time anchor into the prompt
- append the real-world grounding clause using this exact strong form:
  `The outdoor environment must display the real-time weather conditions and natural lighting and shadow effects of the specified [city] at the specified [YYYY-MM-DD], at [HH:mm].`
- let outdoor light, sky condition, pavement dryness, seasonal vegetation, and air feel match the real world naturally through that clause instead of soft atmosphere wording
- adjust outfit details to fit likely weather and activity while preserving the character's style
- do not pre-bake conflicting environment outcomes such as `spring evening`, `sunny afternoon`, `rainy street`, `golden-hour light`, or similar weather/lighting conclusions into the main descriptive sentence

If exact city/date anchors are missing, fall back to general atmosphere cues instead of claiming real-world synchronization.

### Indoor With Outdoor View

When the scene is indoors but the outside is visible:

- still inject city and exact local date/time anchors when available, so the visible outdoors can benefit from real-world perception
- use the same strong grounding pattern for the visible outdoors:
  `The outdoor environment must display the real-time weather conditions and natural lighting and shadow effects of the specified [city] at the specified [YYYY-MM-DD], at [HH:mm].`
- make the visible outdoors match the city, local date/time, and weather
- keep clothing primarily appropriate for the indoor environment

### Indoor Closed

Do not invoke weather-based outfit changes.

You may still use:

- `time_of_day`
- `lighting_hint`
- `environment_mood`
- continuity-friendly appearance details

## Prompt Construction

If `consumption.selfie_ready` is present, use it as the base:

- The photographed subject is always Stella/the assistant, never the human user.
- If a timeline description appears to describe the user instead of the assistant, ignore the timeline enhancement and fall back to Stella's default selfie behavior for that request.


```text
A [mode] photo of this person, [activity] at [location], wearing [appearance], with a [emotion] expression, [time_of_day] atmosphere.
```

Then enrich only when supported by timeline facts:

- add `city` and exact local date/time anchors when they help real-world grounding
- add `location_props` as concrete scene details
- add `lighting_hint` for believable light behavior
- add `framing_hint` as a descriptive cue when it strengthens realism
- add `environment_mood` and `social_context` as subtle atmosphere cues
- keep atmosphere cues subordinate to grounding; they must not override objective outdoor weather or lighting
- when real-world grounding is active, avoid descriptive phrases in the main sentence that already decide the outdoor weather, season, sky state, or time-specific light result

For outdoor or outdoor-visible scenes, append this explicit grounding clause with concrete values:

```text
The outdoor environment must display the real-time weather conditions and natural lighting and shadow effects of the specified [city] at the specified [YYYY-MM-DD], at [HH:mm].
```

## Examples

### Sparse request, timeline resolves a home study

```text
A mirror selfie of this person, organizing work files at her home study, wearing a casual home outfit, soft warm indoor light, slightly tired but calm, with a focused expression.
```

### Sparse request, cafe by the window, outdoor visible

```text
A direct selfie of this person, reading at a cozy cafe window seat, wearing a light casual outfit, relaxed and content, seated by the window with the city visible outside. The outdoor environment must display the real-time weather conditions and natural lighting and shadow effects of the specified Shanghai at the specified 2026-03-28, at 17:40.
```

### Sparse request, outdoor city walk that reads better as non-selfie

```text
A direct selfie of this person, walking along a riverside street in Hangzhou, wearing a stylish weather-appropriate outfit, relaxed and cheerful, handheld framing, clearly a selfie. The outdoor environment must display the real-time weather conditions and natural lighting and shadow effects of the specified Hangzhou at the specified 2026-03-28, at 16:20.
```
