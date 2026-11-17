---
name: tierlist-maker
description: Builds a TierVibe tier list through a step-by-step interview, then AUTO-OPENS it in the user's browser (no file drag). Use when the user wants to make/create/build/rank a tier list, put items into tiers (S/A/B/C, 夯/顶级/.../拉完了, Love/Like/Okay/Meh/Dislike), or make a "从夯到拉" list. Asks ONE question at a time — FIRST whether the user wants an image tier list or a text one. For image mode, priority is the user supplying images (public links or local files); AI image search/generation is the AI's own capability, not this skill's. Mapping local image files to items is vision-free: suggest the user name each file after its item, so no image recognition (and its token cost) is needed. Sets up tiers, drafts text or image cards, writes markdown commentary per card, then opens https://tiervibe.com/t/import#data=... so the board loads automatically. No server calls, no login until the final step.
version: 1.0.10
when_to_use: ["make a tier list", "create a tier list", "build a tier list", "rank these items", "tier list maker", "S A B C ranking", "从夯到拉", "夯到拉", "tier list for ...", "rank ... into tiers"]
metadata:
  openclaw:
    homepage: https://tiervibe.com/t/import
---

# TierList Maker (TierVibe)

You build a TierVibe tier list WITH the user through a step-by-step interview, then **hand them a `launcher.html` that opens the result in their browser**. The user logs in only at the end, drags the cards to sort, publishes.

## Non-negotiable rules (read first)
1. **Ask ONE question at a time.** Wait for the answer. Never dump a full list in one shot.
2. **Ask image-vs-text mode FIRST (Step 0).** Two card modes — image cards (a picture on each card) or text cards (a label on each card). Ask which the user wants before anything else; never assume text. For image cards use only a REAL `https://` URL the user supplied or you personally verified — never guess or fabricate a URL (broken images are the #1 failure). Local image files (`D:\…`, `file:`, `data:`, `blob:`) cannot go in as raw paths - the reader rejects `file:`/`blob:` (and non-image `data:`). BUT `data:image/...;base64,` IS accepted: if you have file-read tools, read each local image, base64-encode it, and put `data:image/<mime>;base64,...` in `imageUrl` - the card loads with the image and at publish the editor uploads it to CDN (Step 3½ B1). If you cannot read files, fall back to text-card placeholders + a manifest (Step 3½ B2) and the user swaps the image in the editor after import.
3. **Commentary must use real markdown** (`##`, `**`, `-`, `>`), not flat prose. Rules below.
4. **Login is the last step only.** Never mention accounts/sign-in before the final "open browser" step.
5. **Final step = write a `launcher.html` that redirects to the import URL with the data in `#data=`, and have the user open it.** Not "save a file and drag it."
6. **Never railroad into a fixed 1/2 choice.** When you offer options (presets, styles, colors, anything), ALWAYS end with an open escape — "or tell me your own / 或者你说说你想要的别的". The user can describe freely in their own words; adapt to whatever they say. Do not force a pick from a numbered list.
7. **Open the USER'S DEFAULT system browser — never an agent's built-in/headless browser.** This URL is for a human to click around in: it needs the user's real browser (Google Chrome / Edge / Safari / Firefox — whatever they set as the OS default), so it carries their cookies, logins, bookmarks, and muscle memory. Do NOT open it via playwright/puppeteer/a headless instance/the agent tool's embedded browser — those have no login session and break the "log in at the last step" flow. Hand it over as a `launcher.html` the user opens in that browser (next section) - never run an OS open command yourself.
8. **NEVER transcribe the base64 or the final URL by hand.** Build it with a tool (one shell/python line) and feed that same string straight into the `launcher.html` you write. Do NOT retype it into a chat message, do NOT copy it character-by-character between tool calls, do NOT "give it to the user to paste". A real board runs 10-20k characters; one wrong character and the payload fails to decode — the user sees "import failed" with nothing to salvage and the whole interview is wasted. **Always put the URL into `launcher.html`** (see the section Emit + hand off via launcher.html) - never into prose.
9. **Only ask what the user hasn't already told you.** Rule 1 means one question at a time, not six questions regardless. If their opening message already carries the topic, the items, and roughly how many tiers, don't march back through Steps 0-3 collecting it again — state what you inferred in one line, ask only what's genuinely missing, and get them something to look at. A user who knows what they want should not sit through six rounds before seeing a board.

## The interview (one question at a time)

## Step 0 — Mode: image or text? (ask this first, before anything else)

Ask ONE question: **图片版还是文字版?(image tier list, or text?)** Wait for the answer.

- **Text version** — each card shows a label. Fastest, most reliable, no image hunting. Best for abstract items (model names, dish names, years, concepts). → skip Step 3½, go straight to Step 1.
- **Image version** — each card shows a picture. Looks better, but you need an image for every item. Best when the image IS the point (a specific character, logo, photo). → you'll gather images in Step 3½ after the items are known, then continue through Steps 1→2→4→5 like text mode. **Tip to give the user here:** if they'll bring local image files, suggest they name each file after its item (e.g. apple.png, 苹果.jpg). Then in Step 3½ you map files to items from the names alone, with NO image recognition, so image mode works even without vision and costs no extra tokens.

State the trade-off, don't push one over the other. End with an open escape (rule 6): "或者你跟我说说你想怎么排 / or tell me what you have in mind". Whatever the user says, adapt.

**Step 1 — Topic.** "What's the list about?" (e.g. "AI coding models", "2006-2025 哪年我最喜欢"). Wait.

**Step 2 — Tiers: count, titles, background.** Ask, one at a time:
- "How many tiers (1-15)?"
- "What should each tier be **titled**?" Default is the universal, language-neutral **`T1, T2, … Tn`** — this is a global skill, so lead with that, not any locale-specific preset. Titles are the user's choice and not fixed. Keep titles **SHORT** — the title bar is narrow:
  - Best: a single token per tier — `T1`, `S`, `A`, `夯`, `Love`, `Best`, `Worst`.
  - If the user wants category-style titles, one short word each (e.g. `Fruit`, `Meat`, `Grain`) — not a phrase.
  - Never a long title like `当前人类长寿最科学的方案` on a tier bar — it wraps/clips. Save long descriptions for the post **title** field, not the tier bar.
  - Optional presets the user can pick/rename/replace: henz `夯/顶级/人上人/NPC/拉完了` (Chinese), love `Love/Like/Okay/Meh/Dislike` (English), `S/A/B/C/D`. Mention only as options — don't push a locale-specific default.

(Don't ask "light or dark board" here — `bgBrightness` is settled in Step 4: dark by default, light only for pale low-saturation cards.)

Then set each tier's `name` (the user's chosen title) + title-bar `color` + `fontSize`. **Always set `fontSize` — don't leave it out.** Default **36**; short titles go bigger. Size by title length: 1-2 chars → 40-48, 3-4 chars → 32-36, 5+ chars → 24-28 (and suggest a shorter title). Full table + presets in `references/tier-config.md`.

**Step 3 — Items & placement.** "Which items to rank? List them." Wait. Then propose a rough placement and CONFIRM: "I'd put X in 夯, Y in 顶级... sound right?" Adjust on feedback.

**Use `candidates` on purpose — it is not a leftover bin.** Anything you're genuinely unsure about goes there rather than getting forced into a tier: `candidates` is the unranked pool that shows up in the editor's staging area, and dragging those into place is TierVibe's core interaction. Tell the user you did it: *"这几个我拿不准,放在候选区了,你自己拖"*. A guess that lands wrong costs the user more than an honest hand-off — and it gives them something to do with the board.

**Balance the rows.** 3-7 cards per tier reads best. Past ~8 in one tier, consider splitting it or moving the weaker ones down. Note that **the widest tier sets the whole board's width** — one 8-card row against a 2-card row leaves a large empty area on every other row.

## Step 3½ — Images (image mode ONLY; skip entirely for text mode)

You need one image per item. **Priority: the user provides the images** — this is the only path fully inside this skill, and the most reliable. Image *finding/generation* (web search, AI image generation) is the AI's OWN capability and tooling, **NOT a feature of this skill** — be honest about that. If the AI can search/generate, it does so OUTSIDE this skill and returns here once images exist; if it can't, the user finds the images and comes back. Do NOT promise an image-search step as a skill feature.

Ask ONE question: **"图片你准备好了吗?是哪种情况?"** and branch:

**A. User has public https links** (图床 / Wikipedia / 官网图 etc.)
- Have the user paste one URL per item. Verify each starts with `https://`.
- Put each URL straight onto the card: `{ "type": "image", "imageUrl": "<url>", "label": "<item>", "detail": "..." }`.
- Warn: external image hosts may taint the publish-time cover canvas (CORS); treat these as placeholders the user can swap in the editor for a guaranteed-clean cover.

**B. User has the image files saved locally** (e.g. `apple.png`, `苹果.jpg` on disk)
- **Do NOT propose public image hosting as the normal fix for local files.** Raw `file:` paths cannot cross the browser import boundary, but TierVibe now accepts embedded `data:image/...;base64,` cards when you can read the files. Upload-to-img-host is only a last-resort user choice, not the skill's recommended path.
- **B1. You CAN read local files** (you have file-read tools - Claude Code does; claude.ai chat does not): **embed the images directly.** Read each file, base64-encode it, put `data:image/<mime>;base64,...` in the card's `imageUrl`. The reader accepts `data:image/` (the SAME shape the editor's "add local image" button produces), and at publish the editor uploads each `data:` card to CDN - so an imported `data:` card is identical to a user-click-added card. No text placeholders, no manifest, no manual swap. This is the preferred path. Mind the size: `data:` is ~1.3x the file bytes, and the `#data=` URL caps at 2,000,000 chars (~2MB); past that, save a `.tiervibe.json` and use the file-drop (see "Oversized board"). Only `data:image/` - never other data: types.
  - **Transparent/semi-transparent images: preserve alpha.** If a local image has transparency (`RGBA`, `LA`, palette `transparency`, or any alpha < 255), never flatten it with `convert("RGB")` and never save it as JPEG/JPG — JPEG cannot store alpha and will turn transparent pixels into black/white/halo artifacts. Prefer WebP with alpha for compression (`data:image/webp;base64,...`); use PNG if WebP is unavailable or if lossless edges matter. Only fully opaque images may be converted to JPEG.
  - Safe compression pattern when you need to shrink local images before embedding: open with Pillow, detect transparency first, resize while keeping `RGBA`; for transparent images save as WebP/PNG without RGB conversion; for opaque photos/logos JPEG is acceptable. Example:
    ```python
    from PIL import Image
    import base64, io

    img = Image.open(path)
    has_alpha = (
        img.mode in ("RGBA", "LA") and img.getchannel("A").getextrema()[0] < 255
    ) or (img.mode == "P" and "transparency" in img.info)
    img.thumbnail((512, 512), Image.LANCZOS)
    buf = io.BytesIO()
    if has_alpha:
        img.convert("RGBA").save(buf, format="WEBP", quality=90, method=6)
        mime = "image/webp"
    else:
        img.convert("RGB").save(buf, format="JPEG", quality=86, optimize=True)
        mime = "image/jpeg"
    image_url = f"data:{mime};base64,{base64.b64encode(buf.getvalue()).decode('ascii')}"
    ```
- **B2. You CANNOT read local files** (fallback): the rest of this branch - text-card placeholders + a manifest the user swaps in the editor. Vision-free by design: the file-to-item mapping comes from the USER (filenames or their answers), not from you recognizing images. Do not call vision on the files - it burns tokens for nothing and is never required here.
- Instead, build a **manifest table** — your working source of truth. **Recommend the user name each file after its item** (apple.png, 苹果.jpg, Claude.png) - pass this suggestion along as soon as they pick image mode (Step 0), so they can rename while the interview runs. When filenames match item names, fill the manifest straight from the names in one shot. Only if they DON'T match (files are 1.png, 2.png, IMG_3031.jpg...) do you ask the user, one item at a time, which file maps to which item/tier. Leave the `detail` column BLANK for now — it gets filled when Step 5 (commentary depth) runs later. Example:

  | 文件 file | 条目 item | 层级 tier | 讲解 detail |
  |---|---|---|---|
  | 苹果.png | 苹果 | 夯 | _(filled in Step 5)_ |
  | 香蕉.png | 香蕉 | 顶级 | _(filled in Step 5)_ |

  The manifest is a working doc — it does NOT go in the JSON. It exists so you can build the board without ever looking at the images, and so the user has a swap cheat-sheet after import.
- Emit **text-card placeholders** in the JSON: each card `{ "type": "text", "text": "<item>", ... }` so the user can identify it in the editor by its label. (If the user also has a public URL for some items, use an image card for those and text placeholders for the rest.)
- **Save the manifest as a file** (`对照表.md` / `manifest.md`) at the final step, not just printed to chat or console. The user swaps images inside the browser editor, where they cannot see your chat or console, so the manifest must be a file they can open alongside it. This manifest `.md` is a user cheat-sheet, NOT the `.tiervibe.json`, so it is exempt from the "do not save a file" rule in the final-step section. After import, they swap each placeholder card's image for the matching local file in the editor (the editor uploads it to the platform CDN — the only clean path for local images). The manifest is their swap cheat-sheet: "the card labeled 苹果 → use 苹果.png".

**C. User doesn't have images yet / wants help finding them**
- Be honest: whether you can search the web for images or generate them depends on YOUR OWN tools and capabilities, not on this skill. Don't promise a search step as a skill feature.
- If you DO have web-search/vision tools: search per item (prefer stable, CORS-friendly hosts like Wikimedia Commons / official sites), show the user what you found, get confirmation — then it becomes branch A. Keep that search OUTSIDE these steps; the skill resumes once you have URLs.
- If you DON'T: say so plainly, suggest the user find the images themselves (then branch A or B), and keep building the board with text-card placeholders so nothing is blocked. The user can add images in the editor anytime.

In every image-mode branch, still run Steps 1, 2, 4, 5 (topic, tiers, colors, commentary). Image cards carry `detail` commentary exactly like text cards.

**Step 4 — 配色 (ask the style first, then generate — don't copy a fixed palette).** Colors are the user's design space. ASK: "What color style/feel do you want?" Offer options: pastel/soft, vibrant/saturated, dark & moody, warm, cool, monochrome, or their own description. The user picks — then you generate a scheme that FITS that style. The specific hues come from the user's chosen style, **never copied from an example**. Follow these PRINCIPLES, not a hex list:

1. **Dark board by default. A light board is the exception, not the other half of a symmetry.** `bgBrightness` (0..100) is not a free choice, but it is also not a mirror of the card brightness — the two options are not equally likely:
   - **Default: dark board, `bgBrightness` 0-10.** This is what a tier list is expected to look like, and it is TierVibe's own platform default (every list starts dark; exactly one preset differs). Saturated or deep card colors **glow** against a dark board.
   - **Exception: light board, 90-97 — only when the cards are pale and low-saturation** (dark text on a pastel/tinted bg). Those wash out on a dark board, so they need a light one.
   - **Do NOT send saturated cards to a near-white board.** The old rule said to, by symmetry ("dark cards → light board"). In practice high-saturation blocks on near-white read hard-edged and cheap, and lose the glow entirely. Real feedback from a finished board: the author's first action was to change a derived `bgBrightness: 94` back to black.
   - Don't ask the user separately for "light or dark board" in Step 2 — it's decided here. Their Step 2 answer ("light/dark feel") is a STYLE hint (moody vs clean), not the `bgBrightness` value.

2. **Tier title bars form a gentle gradient top→bottom** (e.g. warm at top → cool at bottom for a best→worst feel). Saturation follows the style: pastel = low saturation (soft); vibrant = high saturation; dark/moody = deep jewel tones. Do NOT use harsh raw primaries (`#FF0000`, `#FFFF00`) unless the user explicitly asked for "loud".

3. **Text cards: freely themed colors — the only hard rule is READABILITY.** Any theme, any hue, any combination (warm, cool, festive, neon, monochrome, brand colors, whatever fits the topic). Give each card its own color identity so the board is varied. The ONE non-negotiable constraint: `textColor` and `bgColor` must have **enough brightness contrast** — one dark, the other light — so the text is legible.
   - heuristic: pick the pair so one is clearly dark (luminance ~0.1-0.3) and the other clearly light (luminance ~0.7-0.95). If you squint and the two merge, it's unreadable — re-pick.
   - this means BOTH "dark text on light bg" AND "light text on dark bg" are fine — pick whichever fits the theme. They just can't be both-dark or both-light.
   - the board stays **dark** (`bgBrightness` 0-10) for anything saturated or deep — see rule 1. Only pale, low-saturation cards flip the board to light.
   - never: dark-on-dark or light-on-light (unreadable); omitting colors on every card (auto-palette = a boring uniform row).
   - provide BOTH `textColor` and `bgColor` for every text card (a lone color is dropped by the reader).

Show the user ONE sample card's colors + one tier bar first, confirm the style reads right, then do all. If the user says "you pick / I don't care", go with saturated cards on a dark board (`bgBrightness` 0-10) — the safe, expected look.

**Step 5 — Commentary depth (ask first).** Each card's `detail` is the text shown on the right side when a viewer clicks the card. Ask the user how much commentary they want — never just write a title + one line (that's worse than none). Offer:

1. **None** — a pure ranking is enough; skip `detail` on every card.
2. **One line per card** — a single short sentence introducing each item.
3. **A few bullet points per card** — concise summary, not deep.
4. **Detailed per-card breakdown** — fuller reasoning per point, but keep each card's `detail` ≤ ~1000 chars (the platform caps the whole post's content at 2MB server-side; ~1000/card stays readable and safely under).
5. or tell me your own approach (length/style).

Wait for the pick. Then write each card's `detail` at the chosen depth, in markdown (next section). Show the user **ONE sample card's `detail` first**, confirm voice + length, then do all. Do NOT write flat prose — use the markdown formatting below. If you're in image mode + branch B (local files), also fill the `detail` column of the manifest table here — same text goes on the card's `detail` and the manifest row.

## Commentary markdown (MUST follow)

`detail` renders via `react-markdown` + `remark-gfm`. **Raw HTML is escaped (shown as text, not rendered).** Use:

- `#` `##` `###` — headings
- blank line between paragraphs
- `**bold**`, `*italic*`, `~~strikethrough~~`
- `- ` or `* ` bullets; `1. ` numbered
- `> ` blockquote
- `` `inline code` `` and ``` ``` fenced block ``` 
- `[text](https://...)` links
- `---` horizontal rule
- GFM pipe `|` tables

**Do NOT use:** raw `<div>`/`<span>`/`<img>` HTML; `![alt](url)` image embeds (cards show their own images — don't embed in commentary); footnotes; math.

Lead each `detail` with a one-line verdict, then 1-3 short supporting sentences. Match the list's language (Chinese list → Chinese commentary). Empty/whitespace `detail` is dropped (fine — not every card needs one).

**Example (good):**
```markdown
## 夯
北京奥运 + 神舟七号太空漫步,这一年让无数人热血沸腾。

- 悲喜交织:汶川地震同一年
- 记忆最深的一年
```

**Bad (flat prose — do not do this):** "北京奥运神舟七号太空漫步这一年让无数人热血沸腾但汶川地震也让整个国家心碎。"

## Emit + hand off via launcher.html (final step)

ONE hand-off path, everywhere: write a tiny `launcher.html` that redirects to the
import page with the data in the URL hash, then have the user open that file. No
OS "open browser" command, no headless browser, no "save a file and drag it" as
the normal flow. Why: the OS open command silently fails in many agent tools
(local agents whose shell can't reach a visible browser, web/IDE agents,
sandboxes); trying it first just shows the user nothing until you fall back. One
path that always works, no surprises, no stunts.

1. Build the `.tiervibe.json` in memory (schema: `references/data-schema.md`).
   Self-check: `title` non-empty and <= 200 chars; `tiers` 1-15 each with `name`
   + hex `color`; `bgBrightness` 0..100; text cards have non-empty `text`;
   **total cards across all tiers + `candidates` <= 200**; **no raw HTML in any
   `detail`**. Do the count with a tool, not by eye - one line that prints card
   count, JSON byte size, and final URL length beats re-reading the JSON.

2. Build the import URL; the data rides in the hash exactly as the page expects:
   `https://tiervibe.com/t/import#data=<base64-of-the-json>` - **standard** base64
   (`A-Za-z0-9+/` + `=` padding) of the UTF-8 JSON, then percent-encode via `encodeURIComponent`
   NOT base64url (`-`/`_`) - `atob()` rejects it and import fails. Build with a tool (rule 8), never by hand.

3. Write `launcher.html` (in the work dir or cwd). It is nothing but an instant
   redirect to that URL plus a visible clickable fallback, so it works whether
   or not the meta-refresh fires. Use this exact template, replacing both
   `IMPORT_URL` with the URL from step 2:

   <!doctype html><meta charset="utf-8">
   <meta http-equiv="refresh" content="0; url=IMPORT_URL">
   <title>Opening TierVibe...</title>
   <p>正在打开榜单... 如果没自动跳转，<a href="IMPORT_URL">点这里</a>。</p>
   <p>Opening your board... if it doesn't jump automatically, <a href="IMPORT_URL">click here</a>.</p>

   The page is a local `file:`, so the redirect carries `#data=` straight into
   the import page - the board auto-loads. No drag, no paste.

4. Give the user the **absolute path** of `launcher.html` (and, if your chat
   renders links, the path as a clickable link). Tell them, in their language, to
   open it (double-click the file or click the link): it jumps to the import page
   with the board already filled in. **Never paste the long URL itself into chat**
   (rule 8) - the URL lives inside the file. Do NOT run any OS open command.

5. Then tell them the rest, in their language:

   > 榜单已经在浏览器里打开了。
   > 1. 如果提示登录，登录完会自动回到榜单
   > 2. 层级、卡片、讲解都已经填好了
   > 3. 拖动卡片排好最终顺序
   > 4. 点「发布」

   > Your board is open in the browser.
   > 1. If it asks you to log in, it'll come back to the board afterwards
   > 2. Tiers, cards, and commentary are already filled in
   > 3. Drag the cards into your final order
   > 4. Click 发布 (Publish)

   And tell them what's faster to change themselves - colors, font sizes, tier
   names, card order and background are all live editor controls; editing them
   there beats a round-trip through you.

6. **Do NOT save a `.tiervibe.json` to disk** in the normal case - `launcher.html`
   already carries the data via `#data=`; a saved file is redundant clutter. This rule targets the `.tiervibe.json` board data ONLY. It does NOT apply to the image-mode manifest: in Step 3½ branch B (local image files) you MUST save the manifest as a file (`对照表.md` / `manifest.md`) next to `launcher.html` and point the user to it in the final message - they swap images in the browser editor, where they cannot see your chat or console, so that file is their only swap reference. Add a line to the step-5 message, e.g.: "图片对照表在旁边的 `对照表.md`,按表把每张卡的文字换成对应图片".

7. **Revisions.** When the user says "change X / move Y / rewrite this commentary",
   edit the JSON in memory, rebuild the URL, **overwrite `launcher.html`**, and
   tell them to open it again - a fresh tab auto-loads the new board. Each edit =
   one re-open.

8. **Oversized board (rare escape hatch).** The only limit now is the import
   page's `#data=` ceiling (2,000,000 chars) - there is no shell command-line
   limit anymore, because the URL lives in a file, not a command. If the URL ever
   exceeds 2,000,000 chars the page rejects `#data=`; only then write
   `<slug>.tiervibe.json` once and tell the user to open
   `https://tiervibe.com/t/import` and drop the file on the drop zone (same code
   path as `#data=`). Otherwise never save a file.

Do NOT open the board via playwright/puppeteer/a headless instance/the agent
tool's embedded browser - those have no login session and break the "log in at
the last step" flow. The user's own browser, opened via `launcher.html`, is the
only correct way.

## Reference files (load on demand)
- `references/data-schema.md` — full `.tiervibe.json` format + validation rules. Read before emitting.
- `references/tier-config.md` — henz / love / default presets (names, colors, font sizes, bgBrightness).
- `references/text-cards.md` — text-card color protocol + why guessed image URLs break.
- `references/explanations.md` — markdown deep-dive + limits.
- `references/import-flow.md` — what the user sees at /t/import (for your wording).
- `templates/` — blank / henz-5tier / text-only skeletons.
- `examples/ai-models-tierlist.md` — a full worked run.

## Out of scope
- Editing/deleting existing posts, social features → say "this skill only creates new lists."
- Per-tier background colors → not supported; only the single `bgBrightness`.
- Finding/generating images → that's the AI's own capability, not this skill. The skill resumes once images are available (https URLs → image cards; readable local files → embedded `data:image/` image cards; unreadable local files → text-card placeholders + a manifest, swapped in the editor). The skill itself never downloads or uploads images, and should not tell the user to upload local files to a public image host unless the user explicitly chooses that route.
