# Content Planning

## Compression Ladder

Start from the user's original text and compress in layers:

1. **Core claim**: one sentence — what is this article really saying?
2. **Viewer promise**: what the reader gets from swiping through the image set
3. **Section map**: 4-8 ideas that become pages
4. **Page hooks**: short, concrete, not abstract
5. **Body fragments**: only the words needed to explain the visual

**Do not put the full article on images.** The image set is a visual outline that makes the user want to read the caption/body.

## Page Plan Template

Before writing any HTML, fill out this plan:

```text
Title:
Category:          (→ see category-cookbook.md)
Style:             Editorial / Swiss
Theme:             (→ see theme-presets.md)
Image assets:      (user photos / search / AI generate / none)

01 Cover
- Hook:            (1-second hook line)
- Visual:          (cover image strategy)
- Layout:          M01 / M16 / S01

02 Page
- Point:           (core argument)
- Copy:            (body text fragment)
- Visual:          (data / quote / image / screenshot)
- Layout:          M04 / M08 / S06 / ...

...
```

## Page Roles — Use Variety

Use varied roles instead of repeating the same card page type. A 7-page set should have at least 5 distinct shapes:

| Role | Description | Typical Layout |
|------|-------------|---------------|
| Hook cover | 1-second stopper | M01 / M16 / S01 |
| Problem scene | Set up the tension | M03 / S02 |
| Misconception vs reality | Two-column contrast | S02 / M15 |
| Checklist | Numbered items | M04 / S05 |
| Data evidence | KPI / stats / ledger | M12 / S09 / S11 |
| Pull quote | One big quote | M04 / M05 |
| Step-by-step flow | Pipeline / process | M08 / M14 / S06 |
| Screenshot evidence | Tool UI proof | S08 / frame-shot |
| Summary / closing | "Remember these three" | M07 / M16 |

**Avoid repeating "title + lead + 3 rows" more than twice in one set.**

## Cover Hook Patterns

Use one of these proven patterns:

- "终于有 Mac 版了"
- "新手别急着买"
- "这个功能真的改变用法"
- "我替你踩过坑了"
- "先看这 5 个点"
- "不要被装备带着走"
- "从此不用手动..."

**Avoid:**
- Overlong complete article titles as cover text
- Vague hype without a concrete object ("重磅！" "速看！")
- Multiple unrelated claims on one cover

## Copy Rules

- Titles should be plain and sharp
- Avoid abstract labels like "背景介绍" unless the page is actually context
- Use verbs and consequences: "高帮鞋会让脚更闷" is better than "鞋子选择"
- For product updates, lead with the user-facing change, then add the feature name
- For AI/tool posts, lead with workflow change: faster capture, less manual work, cross-app automation

## Image-Led Sequence

When the user has multiple good lifestyle photos (旅行/户外/自家成菜/家居), front-load the strongest photo on page 1 and let pages 2-3 carry the text/data.

Pattern:
```
P1      M16 Image-Led Cover    ← best photo, full bleed, restrained title
P2      S11 / M05 / M10        ← text-heavy: ledger / checklist / mini-data
P3      M02 Field-Note Photo   ← second-best photo, in a frame, with caption
P4-N    M02 / M11              ← more field notes or marginalia essays
P_last  M07 / M04              ← closing note or pull quote
```

**Hard rule: never two M16 in a row.** After a full-bleed cover the eye needs to settle on text before another big image.

## Page Count Guidance

| Source length | Recommended pages |
|--------------|-------------------|
| 600-1000 Chinese characters | 5-7 images |
| 1000-1800 Chinese characters | 7-9 images |
| Very long source | Compress to 8-10 images, rest in caption/body |

If several pages have large empty lower areas, **merge adjacent ideas**.

## Matching Visuals To Content

Use visuals only when they support the point:

| Visual type | When to use |
|------------|-------------|
| Screenshot | Proof of a product feature or UI |
| Photo | Scene, object, person, outdoor atmosphere |
| Generated image | Missing scene, conceptual hero, stylized illustration |
| Diagram | Flow, cross-app chain, checklist, system relation |

Generated image prompts should be short and role-specific:
```text
Editorial documentary photo for a hiking gear guide, summer mountain trail,
lightweight long-sleeve outfit, natural sunlight, clean composition, no text, no logo, 3:4.
```

## Captions And Metadata

Small recurring elements help the set feel designed:

- Category row: `AI TOOL / UPDATE / 2026`
- Issue row: `SUMMER HIKING / BEGINNER GUIDE`
- Page number: `03 / 08`
- Compact labels: `DO`, `DON'T`, `WHY`, `NOTE`

Keep these consistent. They should support orientation, not become decoration.
