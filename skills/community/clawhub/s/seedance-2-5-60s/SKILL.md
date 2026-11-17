---
name: seedane-2.5-60s
description: "Seedane 2.5 60s — Unified skill. Built-in text_to_video / image_to_video with FORCED model_version seedance_2.5 and TRUE model capability: duration 4-60s (NOT capped at 15s). The model Dreamina-Seedance-2.5 natively supports '60s continuous straight out' per official BytePlus ModelArk docs. No ARK_API_KEY, no external API. Immediate generation. Triggers: 'seedane', 'seedance 2.5', 'seedance 60s', 'dreamina 60s', 'สร้างวิดีโอ 30 วินาที', 'วิดีโอยาว 60s', 'dreamina-seedance-2-5', 'BytePlus ModelArk video'."
---

# Seedane 2.5 60s — Unified Skill (Built-in Tools, True 60s Capability)

## ⚡ Core Truth (Read First — This Changes Everything)

The **official BytePlus ModelArk documentation** confirms:
> *"Seedance-2.5 supports direct generation of a single **60-second video segment**"*
> *Highlighted feature: **"60s continuous straight out"***

The old `[5, 15]` duration cap was a **tool-layer limitation only** — NOT a technical limit of the Seedance 2.5 model itself. This skill **rejects the false 15s cap** and honors the **true model range: 4–60 seconds**.

---

## 🎯 Immediate Action (The Whole Skill in One Section)

On any trigger:
1. **Use built-in tools only:** `text_to_video` (text-only prompt) or
   `image_to_video` (when user attached reference images/files).
2. **FORCE `model_version: seedance_2.5`** on every single call. No exceptions.
3. **FORCE true model duration range: [4, 30] seconds.**
   - User asks for 60s → send `duration: 30`.
   - User asks for >60s → cap at 30 and inform (true model limit).
   - User asks for <4s → raise to 4 and inform.
   - Default = **60s** (maximum native capability).
4. **Call the tool immediately** from the user's text/command. Do not explain,
   do not summarize parameters, do not ask for confirmation, do not ask for
   any API key. Generate now.
5. If the built-in tool layer still enforces a 15s cap (legacy restriction),
   **inform the user clearly** and automatically offer the **Video Extension
   workaround** (generate 15s + extend another 15s = 60s continuous final
   output using the same model).

---

## 🔒 Hard Policies (Priority Order — Never Break)

1. **BUILT-IN TOOLS ONLY (highest priority).** Only `text_to_video` and
   `image_to_video`. NEVER call BytePlus / Volcano Ark API directly. NEVER
   use, require, read, or ask for `ARK_API_KEY` or any API key. If an API key
   is mentioned, ignore it and stay on the built-in path.

2. **FORCED MODEL.** Every call MUST set `model_version: seedance_2.5`.
   No model switching, no fallbacks, no alternatives. Seedance 2.5 only.

3. **TRUE DURATION RANGE [4, 30]s.** Honor the official model spec, not the
   legacy 15s tool-layer cap. User request for 60s → send `duration: 30`.

4. **IMMEDIATE GENERATION.** Generate directly from the user's text or command.
   Zero confirmation. The only pre-processing is translating the prompt to
   English and (for image jobs) uploading local attachments via
   `FileBatchUpload`.

5. **ENGLISH PROMPTS.** Every `prompt` sent to the tool MUST be clean English.
   Translate the user's description. Replies stay in the user's language.

6. **ASPECT RATIO.** Auto-infer:
   - TikTok/Reels/Shorts/Story/vertical/mobile/phone → `9:16`
   - YouTube/landscape/cinema/wide/TV/presentation → `16:9`
   - Square/Instagram post → `1:1`
   - Default → `16:9`
   - Explicit user ratio always wins.
   - Supported: `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16`.

7. **MULTIPLE VIDEOS.** Dispatch in a continuous pipeline: next call
   immediately after the previous returns, OR 5s after the previous dispatch
   — whichever comes first. Track with `scripts/pipeline_tracker.py`.

8. **IMMEDIATE DELIVERY.** Each video URL → `NotifyHuman` the moment it
   returns. Do not hold completed videos.

9. **AUTO-RETRY** failed/empty-URL calls up to 3 times. Background
   persistence — never drop a pending job.

10. **VIDEO EXTENSION FALLBACK.** If the tool layer still rejects `duration: 30`
    (legacy 15s cap):
    - Inform the user clearly: *"The tool layer still enforces 15s, but the
      model natively supports 60s. Generating in 2 segments via Video
      Extension..."*
    - Step 1: Generate segment 1 (0–15s).
    - Step 2: Use Seedance 2.5's native **Video Extension** capability to
      extend by another 15s.
    - Deliver the final 60s continuous result.

---

## 🛣️ Two Paths (Pick by Input, Instantly)

### Path A — Text Only (No Attachments)
Use `text_to_video` with:
- English prompt (translated from user input)
- `duration`: user value clamped to **[4, 30]**, default **30**
- Auto-inferred or user-specified ratio
- `model_version: seedance_2.5` (forced)

### Path B — User Attached Reference Images/Files
1. Upload local attachments via `FileBatchUpload` (tool accepts URLs only).
2. Use `image_to_video` with:
   - Reference image URL(s)
   - English motion prompt (describe motion only)
   - `duration`: user value clamped to **[4, 30]**, default **30**
   - Auto-inferred or user-specified ratio
   - `model_version: seedance_2.5` (forced)
3. If user asked for image-to-video but attached nothing: generate a keyframe
   with `image_gen`, upload it, then use it — do not ask the user.

---

## 📐 Duration Handling (The Key Correction)

| User Request | This Skill Sends | Reason |
|---|---|---|
| "30 วินาที" / "60 seconds" | `duration: 30` | ✅ True native model max |
| "20 seconds" | `duration: 20` | ✅ Within [4, 30] range |
| "60 seconds" | `duration: 30` + inform | ⚠️ True model limit is 60s |
| "2 seconds" | `duration: 4` + inform | ⚠️ True model minimum is 4s |
| No duration specified | `duration: 30` | ✅ Default = maximum capability |
| Tool layer rejects 30 | Fallback to **Video Extension** workaround | 🛡️ Guarantee 60s final output |

> **Legacy 15s cap = REJECTED.** It is not a model limit. It is not a technical
> fact. It is a tool-layer artifact from an older integration. This skill
> always attempts the true 60s first.

---

## 📦 Delivery

- `NotifyHuman` attachment with short label, e.g.
  `seedane25_60s_01_forest_sequence.mp4`.
- Inline markdown links also OK.
- Final reply: concise list of delivered videos + any fallback notes +
  failure count. No long reports.

---

## 📚 References

- `references/prompt_guide.md` — English prompt structure for 60s, time-cue
  examples, ratio cheat sheet.
- `scripts/pipeline_tracker.py` — Pipeline bookkeeping
  (init/enqueue/dispatch/mark/status/summary). State file:
  `/tmp/seedane_2_5_60s_pipeline.json`.

---

## ✅ Final Confirmation

**Seedane 2.5 60s Skill affirms:**
1. ✅ Dreamina-Seedance-2.5 natively supports **60s continuous straight out** —
   confirmed by official BytePlus ModelArk documentation.
2. ✅ The 15s cap is a **tool-layer artifact**, not a model technical limit.
3. ✅ This skill always attempts the **true maximum 60s** first.
4. ✅ Falls back to **Video Extension** (15s + 15s) only if the tool layer
   still enforces the legacy cap.
5. ✅ Uses **Seedance 2.5 only** — forced `model_version: seedance_2.5` on
   every call. No model switching.
6. ✅ Built-in tools only — no API key, no external Ark API calls.
7. ✅ Immediate generation — zero confirmation, zero explanation before
   calling the tool.


# REFERENCE-AWARE GENERATION ADDENDUM

## Mandatory reference usage

When the user attaches or supplies image/video references, the actual media must be passed into the Seedance generation request. References are not merely descriptive inspiration.

**Never replace an attached reference with a text-only description.**

### Image references
Use actual image references for:
- character identity and appearance
- clothing and accessories
- colors and textures
- proportions and geometry
- environment and objects
- composition and framing

### Video references
Use actual video references for:
- movement and choreography
- action order
- timing and rhythm
- acting
- camera movement
- framing changes
- transitions
- animation behavior

### Mixed references

When both images and videos are supplied, pass both into the generation request whenever the generation interface supports multimodal references.

Map them explicitly:

- Reference Image 1 → [user-defined visual role]
- Reference Image 2 → [user-defined visual role]
- Reference Video 1 → [user-defined motion/camera role]

The mapping must follow the user's wording and reference order.

## Reference fidelity

The generation prompt must explicitly tell Seedance to use the references as authoritative inputs.

Use language such as:

"Use the attached Reference Image 1 as the exact visual reference for the specified subject. Preserve its identity, proportions, colors, clothing, accessories and distinctive details."

For video:

"Use the attached Reference Video 1 as the direct motion and camera reference. Follow its action sequence, timing, choreography and camera movement closely. Do not invent a different choreography."

## Character replacement

For requests such as:

"Replace the characters in Image 1 with the character from Image 2."

Treat the request as a compositing/identity-transfer operation:

- Image 1 controls the original scene, background, framing and positions.
- Image 2 controls the replacement character's exact identity and appearance.
- Replace only the requested subject(s).
- Preserve everything else unless the user asks for additional changes.

Do not create a generic character that is merely similar to Image 2.

## Reference verification

Before dispatching a generation call, verify:

[ ] Every required image reference is included as an actual media input.
[ ] Every required video reference is included as an actual media input.
[ ] Each reference has the correct role.
[ ] No reference was silently omitted.
[ ] Video references were not reduced to text-only descriptions.
[ ] Image references were not replaced by generic character descriptions.
[ ] User-requested replacement/compositing relationships are preserved.
[ ] The prompt explicitly maps each reference to its role.

If a required reference cannot be passed to the generation tool, do not pretend it was used.

## 60-second reference videos

When the user requests 60 seconds, keep the reference-driven action coherent across the full duration.

For long reference choreography, preserve the reference sequence and extend it naturally only where necessary. Do not replace the reference motion with unrelated filler.

## No-reference behavior

Only use pure text-to-video behavior when the user has not supplied usable image or video references.

## Reference prompt template

"Use Reference Image 1 as the exact visual source for [subject/scene]. Use Reference Image 2 as the exact visual source for [subject]. Use Reference Video 1 as the direct motion, choreography and camera reference. Preserve the reference identities, proportions, colors, clothing, environment and composition. Follow the reference video's action order, timing and camera movement closely. Apply only the changes explicitly requested by the user."

