---
name: steam-capsule-art
displayName: "Steam Capsule Art (Steam 胶囊图/商店图)"
slug: steam-capsule-art
category: game-asset
description: "Design and audit Steam store capsule images (胶囊图/商店图): the exact 2024-08 asset sizes, Valve's 2022 content rules, the arithmetic that proves one illustration cannot be cropped into every capsule, percentile thresholds measured from 20 top-selling capsules, and a CLI audit. Use when: 'Steam capsule', 'store capsule', 'capsule art', 'header capsule', 'small capsule', 'library hero', 'library logo', 'Steam store images', '胶囊图', '商店图', '上架美术', '主胶囊', '小胶囊', '竖版胶囊'. Ships scripts/capsule_audit.py which checks exact pixel size, saturation, edge density, dead negative space, and exports a 120x45 thumbnail for the only test that matters."
agent_created: true
description_zh: "做 Steam 胶囊图（商店图）的规格、红线、构图算法与验收脚本。含 2024-08 新版全部像素尺寸、2022-09 内容红线（禁评分/奖项/折扣/行动号召）、「不能从一张图裁出所有尺寸」的算术证明与证据、20 张头部胶囊实测的分位数阈值、以及一条最常翻车的规则：留白区超过画面一半时不能写「空」，必须给它具体内容。附 scripts/capsule_audit.py：精确尺寸校验、饱和度、边缘密度、死白区检测、120×45 缩略图导出。触发：胶囊图、商店图、Steam 上架美术、主胶囊、小胶囊、竖版胶囊、Library Hero。"
---

# Steam Capsule Art

## What this solves

Steam capsule images decide click-through, and Valve rejects or de-ranks non-compliant ones. Two failure modes account for almost every bad capsule:

1. **Sizes treated as crops.** One nice illustration, resized into six assets. The small capsule then has an unreadable logo and Valve's own docs use that exact result as the "Poor Execution" example.
2. **Negative space treated as empty.** Prompt or brief says "leave the left side clean for the logo", the generator produces a flat colour field, and the capsule reads as a character pasted on a background.

This skill gives the exact specs, the arithmetic that kills the crop chain, benchmark-derived thresholds instead of invented absolutes, and a script that measures the result.

## Hard specs (Valve, August 2024 — old sizes are rejected)

| Asset | Pixels | Content |
|---|---|---|
| Main Capsule | **1232 × 706** | artwork + title only |
| Small Capsule | **462 × 174** | artwork + title, **logo nearly fills it** |
| Header Capsule | **920 × 430** | artwork + title |
| Vertical Capsule | **748 × 896** | artwork + title |
| Library Capsule | **600 × 900** | must include logo, subtitle allowed |
| Library Hero | **3840 × 1240** | **artwork only, zero words** |
| Library Logo | 1280 wide / 720 tall, PNG | logotype only, transparent |
| App Icon | **184 × 184** | |
| Shortcut Icon | **256 × 256** | |
| Screenshots | ≥1920 × 1080, 16:9 | gameplay only |
| Page Background | 1438 × 810 | ambient, must not compete |

Safe zone: keep critical content inside **8%** of each edge (5% on the small capsule). Values are reverse-engineered from shipped assets — verify against Valve's official templates before final export.

## Platform red lines (effective 2022-09-01)

Base capsules may contain **only**: artwork, the game name, an official subtitle.

Forbidden — these cost visibility and eligibility for official sales, not just a rejection:

1. Any review score (Steam or press)
2. Award names, symbols, logos
3. Discount copy ("On Sale Now", "-90%")
4. Calls to action ("Wishlist now", "Pre-purchase")
5. Promotion of another product, including sequels
6. **Any other text at all**

Temporary Artwork Overrides are the only exception, and they must be localised, time-limited, and describe currently-available content.

## The three arithmetic facts

### 1. Aspect ratios differ by 3.7×

Main 1.745, Small 2.655, Vertical 0.835, Library Hero 3.097. Cropping a 1232×706 master to 0.835 keeps only **589px of width** — 52% of the frame is destroyed, and a logo occupying 62% of the master's width simply leaves the picture.

### 2. Logo widths are mutually exclusive

- Small capsule needs the logo at **≥85%** of its 462px width = 393px
- Scaling from a 1232px master uses a factor of 462/1232 = 0.375
- So the master would need the logo at 393 / 0.375 = **1048px = 85% of the master**
- But the master's logo should occupy **60–75%**

No single logo size satisfies both. Valve states it directly: *"The art in the small capsule does not need to be the same as your other capsules."*

### 3. So the pipeline is derive, not crop

Order: **logotype first → master key art → each capsule composed independently**, inheriting motif and palette but re-laying out. A capsule family is a set, not five copies of one image.

## Negative space must carry content

When a capsule reserves more than half the frame for the logo, "clean empty space" produces a dead flat field. Fill it with **specific, named elements** — street lights, distant windows, particles, architectural edges, a horizon. A dark, structured field reads as depth; a flat gradient reads as unfinished.

Practical rule: specify **at least three distinguishable light or edge events** in the reserved zone. If the brief says "empty", the model will paint one colour.

## Thresholds from measurement, not taste

Twenty top-selling capsules measured with the same normalisation the audit script uses (LANCZOS to 400×229, preserving source aspect ratio):

| Metric | Median | P25 (use as floor) |
|---|---|---|
| Saturation (mean HSV S) | 0.535 | **0.360** |
| Edge density (ΔL > 28) | 11.56% | **4.92%** |

**Do not invent absolute floors.** Measured games below 10% edge density that are commercially successful: Undertale 1.93%, Inscryption 3.65%, Dave the Diver 3.88%, Lethal Company 4.13%, RimWorld 4.92%, Mouthwashing 6.58%, Slay the Spire 7.26%, Animal Well 9.27%, Celeste 9.69%. A "≥10%" rule would fail half the reference set.

Low saturation is likewise not disqualifying: Cult of the Lamb 0.225, Hollow Knight 0.324, RimWorld 0.329.

**Measurement caveat that has already caused a wrong threshold once:** always resize to the source aspect ratio. Resizing a 460×215 header to 200×200 distorts it and inflates edge density from ~10.9% to ~15.2%.

## Workflow

1. **Logotype.** Legible at 120×45. Stroke width must stay ≥1.5px when the logo is 102px wide, i.e. **≥1.5% of logo width**; at a 862px logo that means ~13px strokes.
2. **Master key art.** One 3:2 or 16:9 illustration. Reserve the logo zone as *structured* negative space, not empty.
3. **Per-size composition.** Rebuild layout for each asset. Small capsule and App Icon are always drawn separately.
4. **Audit** with `scripts/capsule_audit.py`.
5. **Thumbnail test.** 120×45 is the real viewing size in Steam search results.

## Script

```bash
python scripts/capsule_audit.py capsule.png --target 1232x706
python scripts/capsule_audit.py small.png    --target 462x174 --logo-zone left
```

Reports exact-size match, saturation, edge density, negative-space liveness, and writes a 120×45 thumbnail next to the source. Exit code 1 on any hard failure.

## Failure modes (each one paid for)

| Symptom | Cause | Fix |
|---|---|---|
| Purple/black flat field on one side | Brief said "empty gradient" | Name 3+ concrete elements for that zone |
| Small capsule title unreadable | Cropped from master | Compose separately; logo ≥85% width |
| Character standing tiny, feet cut by frame edge | Full-body master pasted in | Crop at thigh, character 84–90% of frame height |
| Output 2px short (704 vs 706) | Generator rounds | Re-request exact size or render taller and crop |
| Watermark in the deliverable | Generator stamp | Pad before generating, crop after (see `ai-watermark-margin`) |
| Family looks like five crops | One composition reused | Verify: small-capsule logo width × (462/1232) > 110% of master logo width |

## Acceptance gates

1. Exact pixel dimensions — no scaling to fit
2. Legible at 120×45
3. Saturation ≥ 0.363, edge density ≥ 4.9% (benchmark P25)
4. Reserved zone contains ≥3 distinguishable light/edge events
5. Base capsule carries the game name only — count the words
6. Small capsule logo ≥85% of width
7. Crop-chain check: small-capsule logo, scaled back to master width, is **>110%** of the master's logo width

Gates 1, 3, 6, 7 are mechanical. Gate 4 is the one humans keep skipping.
