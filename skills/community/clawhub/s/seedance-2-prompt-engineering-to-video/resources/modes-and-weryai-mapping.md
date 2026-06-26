# Modes, strengths, and WeryAI field mapping

Companion to [SKILL.md](../SKILL.md). Use with [camera-and-styles.md](camera-and-styles.md) and [recipes-weryai.md](recipes-weryai.md).

Some prompt cookbooks use **`@image1` / `@video1` / `@audio1`** placeholders (JiMeng-style). **WeryAI `video_gen.js` does not parse those tokens.** Always place media in JSON and describe roles in the **`prompt`** string.

---

## 1. Concept → JSON quick map

| Planning slot (concept) | Typical WeryAI JSON | In the `prompt`, say explicitly |
|-------------------------|---------------------|----------------------------------|
| First frame / identity still | `image` **or** `images[0]` **or** `first_frame` | “Match identity, outfit, and composition from the reference still.” |
| Second / waypoint still | `images[1]` | “Mid-shot matches the second reference for environment / prop.” |
| Third / end still | `images[2]` **or** `last_frame` **or** `last_image` | “End state aligns with the final reference frame.” |
| “Camera / motion from a video” (no video upload) | *(text only)* | Describe lens, speed, and path in prose; or extract **key frames** as `https` stills and map as `images` waypoints. |
| “Extend previous clip” | `image` = **last-frame still URL** (or first key frame of next beat) | “Seamless continuation: same character, wardrobe, lighting, and camera style as the reference frame; no jump cut.” |
| “Beat sync to music” | *(text only)* + `generate_audio: true` often | Describe hit points by **time ranges** (e.g. “on 4–5s accent, punch-in”). **WeryAI JSON has no separate music URL** for Seedance 2.0 in this skill—use timed prose. |

**Hard limits for `SEEDANCE_2_0` (image path):** up to **3** reference images (`upload_image_limit`); **`duration`** integer **5–15**; **`prompt`** max **2000** chars; **no API `negative_prompt`**—put hygiene lines inside the prompt text.

---

## 2. Mode selection

### 2.1 First / last frame

**When:** User supplies opening (and optionally ending) stills plus a bridging idea.

**WeryAI:** `first_frame` + `last_frame` + `prompt`, **or** `image` + `last_image` + `prompt`, **or** ordered `images` (2–3 URLs). See **[WERYAI_VIDEO_API.md](WERYAI_VIDEO_API.md)** for exact field names your bundled script expects.

**Prompt habits:** Declare “bridge action”, preserve identity, lighting, and **one continuous motion arc**.

### 2.2 Text-only

**When:** No reference URLs. User wants pure imagination or **IP-safe originals**.

**WeryAI:** `submit-text` JSON only.

**Prompt habits:** Lead with **`aspect_ratio`**, **`duration`**, style; original **nicknames** for characters; **timecoded beats** for the full duration.

### 2.3 Single reference image

**When:** One still anchors identity, product, or composition.

**WeryAI:** `image` + `prompt`.

**Prompt habits:** “Preserve … from reference” + motion that respects silhouette and palette.

### 2.4 Multi-image waypoints (storyboard / one-take path)

**When:** Ordered stills define a path or beats.

**WeryAI:** `images` array (length ≤ **3**) + `prompt` describing **order** and **camera path** through waypoints.

**Prompt habits:** Explicit “first reference … second reference … third reference …”; add **`no cuts, single continuous shot`** only when you truly want one take (works best at **10–15s**).

### 2.5 “All-reference” JiMeng recipes (video + audio refs)

**Reality on this skill:** WeryAI submission here is **text + up to three still URLs**. Translate:

- **`@video1` rhythm** → describe cuts, tempo, and camera in **`prompt`**; optionally add 2–3 **frame grabs** as `images` if the user can supply URLs.
- **`@audio1` beats** → timecoded visual accents in **`prompt`**; enable **`generate_audio`** if you want model-generated ambience/SFX (no copyrighted track names).

---

## 3. Control strengths to exploit (Seedance 2.0)

- **Motion and camera** — describe path, lens feel, and pacing in **specific** terms (see [camera-and-styles.md](camera-and-styles.md)).
- **Identity / style lock** — use **`image`** or ordered **`images`**.
- **Smooth start→end** — **`first_frame` / `last_frame`** or two ordered stills + bridge language.
- **Product reads** — hero light, **360° spin**, **exploded view**, **reassembly** (see recipe H in [recipes-weryai.md](recipes-weryai.md)).
- **Dialogue shorts** — layered **Dialogue** / **Sound** lines under time ranges (keep lines short).
- **Long stories** — **segment** into multiple **5–15s** jobs; each segment ends on a **handoff** description; next job uses **continuation** still + prompt (see recipe K).

---

## 4. Dialogue and sound design

Keep **visual action** and **audio intent** readable as separate lines **inside the same `prompt` string**:

```text
0-5s: [visual + camera]
Dialogue (CharacterName, emotion): "line"
Sound: [ambient / FX / score hint — generic, no copyrighted music titles]
```

**Best practices**

- At most **one dialogue line per ~3–5s** segment.
- Tag emotion: `cold`, `desperate`, `whispering`, `warm`.
- End segments with audio resolution: `score fades`, `silence`, `wind ambience only`.

---

## 5. Multi-segment workflow (>15s total)

1. State **total duration** and **number of segments** (each ≤ **15s**).
2. **Segment 1** — normal `submit-text` or `submit-image` / `submit-multi-image`.
3. End segment 1 prompt on a **stable, describable last frame** (**Handoff frame** paragraph in your plan).
4. **Segment 2+** — use an **`https`** **continuation still** (last frame of prior output, exported by user/pipeline) as `image` or as `first_frame`; prompt: “Continue seamlessly from the reference …”
5. Carry forward in text: **identity, wardrobe, lighting, lens feel**.

---

## 6. One-take / continuous shot

- Assign **`images[0]`** to opening composition; further **`images[n]`** to **waypoints** along the path.
- In **`prompt`**: single camera trajectory, **`no cuts, one-take`**, physically plausible motion.
- Prefer **10–15s**; avoid more waypoints than you can describe clearly within **2000** chars.

---

## 7. Product showcase (e-commerce)

- Bind product still to **`image`** (or first `images[]`).
- In **`prompt`**: **360° rotation**, **exploded layers**, **reassembly snap**, **hero / rim light**, materials (**glass**, **metal**, **matte**).
- Background: **clean studio**, **gradient**, or subtle lifestyle context—**no competitor logos**.

---

## 8. Common pitfalls

| Pitfall | Fix |
|---------|-----|
| Using `@image1` in JSON | URLs in **`image` / `images` / `first_frame` / `last_frame`** only; roles explained in **`prompt`**. |
| Too many references | Max **3** stills for `SEEDANCE_2_0`; merge roles or split segments. |
| Vague motion | Add **timecoded beats** + one **payoff** at the end. |
| IP / moderation rejects | Remove franchise and brand language; **invent** names and generic iconic substitutes; add **in-prompt** hygiene lines (still **no** API `negative_prompt`). |
| Realistic **face** policy risk | Prefer stylized / non-photo references when policy is strict; avoid celebrity likeness. |
| Confusing extension length | Each API call has its own **`duration`**; “extend 15s” = **new** 15s generation with continuation still, not “add to old file” inside one API field. |

---

## 9. Pre-flight checklist (executor)

- [ ] **`model`** is `SEEDANCE_2_0`; **`duration`** ∈ **5…15** (integer); **`aspect_ratio`** and **`resolution`** allowed for this model.
- [ ] **`prompt`** ≤ **2000** chars; **no** API **`negative_prompt`** field.
- [ ] Every **`https`** still has a **named role** in the **`prompt`**.
- [ ] **Timecoded beats** cover the full **`duration`**; one **clear climax or landing frame**.
- [ ] **IP-safe** wording; **no** franchise/brand names; toys **de-branded** in text.
- [ ] Dialogue / SFX **layered** and **sparse** if used.
- [ ] Multi-segment plans include **handoff frame** notes for the next task.
- [ ] User **explicitly confirmed** full **`prompt`** + params (**Pre-submit gate** in [SKILL.md](../SKILL.md)).
