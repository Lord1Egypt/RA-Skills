# Seedance 2.0 prompt engineering playbook (hub)

Parent skill: [SKILL.md](../SKILL.md). This file is the **entry point**; deep content lives in sibling docs under **`resources/`** so you can jump straight to what you need.

## Resource library (read in this order for complex jobs)

| File | Purpose |
|------|---------|
| **[modes-and-weryai-mapping.md](modes-and-weryai-mapping.md)** | Mode pick, JiMeng **`@asset` → WeryAI JSON** map, dialogue/sound, multi-segment, pitfalls, **pre-flight checklist** |
| **[recipes-weryai.md](recipes-weryai.md)** | Copy-paste-grade **A–K** scenarios (adventure, extend, IP-safe, toy, product, drama, one-take, 30s two-segment) |
| **[camera-and-styles.md](camera-and-styles.md)** | Shot sizes, moves, angles, lighting, palettes, render styles, lens phrases |
| **[WERYAI_VIDEO_API.md](WERYAI_VIDEO_API.md)** | **After assembly** — exact `submit-*` / `wait` JSON and CLI (sync pipeline copies this file here) |

---

## 60-second workflow (executor)

1. **Classify:** text-only · single `image` · multi `images` · first/last · continuation from prior clip.
2. **Plan (internal or shared):** Mode → **assets mapping** (each URL’s job) → **timecoded beats** for the chosen **`duration`** (5–15 s).
3. **Draft `prompt`:** Use vocabulary from [camera-and-styles.md](camera-and-styles.md); for a matching scenario open [recipes-weryai.md](recipes-weryai.md) and adapt.
4. **Validate:** [modes-and-weryai-mapping.md §9](modes-and-weryai-mapping.md#9-pre-flight-checklist-executor) checklist + **`prompt` ≤ 2000** chars.
5. **Pre-submit gate** in [SKILL.md](../SKILL.md) → **`submit-*`** → user chooses **`status`** vs **`wait`**.

---

## @token → WeryAI (one glance)

| You see in old cookbooks | WeryAI reality |
|--------------------------|----------------|
| `@image1` | `image` **or** `images[0]` **or** `first_frame` + URL in JSON |
| `@image2`, `@image3` | `images[1]`, `images[2]` (max **3** total stills) |
| `@video1` motion | Describe in **`prompt`**; optional **key-frame** stills as `images` |
| `@audio1` beats | **Time ranges** in **`prompt`**; optional **`generate_audio: true`** (no copyrighted track names) |
| `Extend @video1 by Xs` | **`submit-image`** with **last-frame `https`** + continuation **`prompt`**, **`duration` = X** |

---

## Core rules (non-negotiable)

1. **Declare mode** before writing the final **`prompt`**.
2. **Map every still** to a role in prose (identity, waypoint, end state).
3. **One major beat per time slice**; align slices to **5 / 10 / 15** (or any integer **5–15**).
4. **Specific > poetic** — concrete subjects, materials, camera words.
5. **Dialogue / sound** as labeled lines under time ranges when needed.
6. **IP-safe:** invented names, generic iconic substitutes, no franchise/brand strings.
7. **No API `negative_prompt`** for `SEEDANCE_2_0` — put hygiene lines **inside** the **`prompt`**.

---

## Timeline beat templates (compact)

Scale to **`duration`** ∈ **5…15**.

| Approx. length | Pattern |
|----------------|---------|
| **5s** | `0-2s` establish → `2-4s` main → `4-5s` payoff |
| **10s** | `0-3s` setup → `3-7s` core → `7-10s` climax + landing |
| **15s** | `0-4s` world → `4-9s` build → `9-13s` turn → `13-15s` payoff |

---

## JSON field cheat sheet

| Intent | Fields |
|--------|--------|
| Text | `model`, `prompt`, `duration`, `aspect_ratio`, `resolution`, `generate_audio` |
| One still | + `image` |
| Waypoints | + `images` (≤3 URLs) |
| Start/end | `first_frame` + `last_frame` **or** `image` + `last_image` (per [WERYAI_VIDEO_API.md](WERYAI_VIDEO_API.md)) |

---

## When the user only says “make it better”

1. Open [camera-and-styles.md](camera-and-styles.md) and add **one** lighting + **one** camera move term.
2. Tighten beats to **seconds**; add **one payoff** in the last segment.
3. If the topic matches a recipe, merge structure from [recipes-weryai.md](recipes-weryai.md).
4. Re-check length and **pre-flight** in [modes-and-weryai-mapping.md](modes-and-weryai-mapping.md).
