---
name: text-to-comic
version: 3.0.0
description: 把文字、对话、日记、照片说明或知识内容转成漫画/绘本/信息图，先出分镜再逐格出图，自带默认角色卡保证跨会话主角一致，支持只出分镜、只重出某一格。6 档语气（warm-healing / playful-snark / calm-documentary / deadpan / lyrical / energetic）与 12 画风正交组合，另有 4 组中文场景预设（日记条漫 / 知识绘本 / 亲子四格 / 诗词条漫），含中文对白字数纪律；分出分镜后可装订成单文件 HTML 绘本（图片内嵌、断网可看、可直接转发）。Turn text, dialog, diary entries, photo notes, or knowledge notes into a comic, picture book, infographic, or hybrid comic+diagram — storyboard and panel plan first, then panel-by-panel rendering, with style presets and consistent characters. Ships a default character card (character card / 角色卡) that keeps the protagonist consistent across sessions. Use when 想画故事、对话变漫画、概念变信息图、旅行日记配图、画四格漫画、连环画、条漫、绘本分镜、漫画日记、改某一格而不重画整页、只出分镜、换主角卡。Not for 纯文字写作、模仿在世画家的标志性风格、复制受版权保护的素材。
metadata: { "openclaw": { "os": ["darwin","linux"], "requires": { "bins": ["python3"], "config": ["image_gen.enabled"] } } }
user-invocable: true
disable-model-invocation: false
---

# text-to-comic v2

## Purpose

Turn user-provided text, photo descriptions, dialog, diary entries, poems, or knowledge notes into a visual deliverable that fits the material best:
- multi-panel comic
- picture-book spread
- infographic
- hybrid comic + diagram page

Preserve the strong parts of v1:
- automatic content-type judgment
- visual-form selection
- style recommendation
- character consistency
- scene continuity
- clean-image assembly

Add v2 structure so results are easier to control and revise:
- style presets from `presets/styles.json`
- structured panel plan from `schemas/panel-plan.schema.json`
- per-panel render task and retry record from `schemas/render-task.schema.json`
- panel-by-panel rendering instead of one-shot full-page generation

## When to use

Use this skill when the user wants to:
- draw a story as a comic or picture book
- convert dialog into a 4-panel or short comic
- turn a concept or workflow into a visual infographic
- convert travel notes, diary entries, or photo notes into illustrated output
- iterate on style, storyboard, or single-panel fixes instead of regenerating everything

Do not use this skill when the task is mainly:
- pure text writing with no visual output
- exact imitation of a living artist's distinctive signature style
- direct reproduction of copyrighted third-party material

## How it differs

- **Not a one-shot image generator.** It produces a storyboard and panel plan you can revise before rendering, and supports per-panel retry instead of redrawing the whole page.
- **Not a style-cloning tool.** It recommends from curated presets and refuses to imitate a living artist's signature style.
- **Not a research tool.** It visualizes material you already have; it does not go find or verify the source content for you.

## Decision flow

1. Classify the input as one of:
   - narrative
   - dialog
   - knowledge
   - poetic
   - hybrid
2. Choose a visual form:
   - `comic`
   - `picture-book`
   - `infographic`
   - `hybrid`
3. Pick a default format:
   - `4-panel` for short dialog or punchline-based requests
   - `6-panel` to `8-panel` for short narrative arcs
   - `single` for infographic or single illustration
   - `webtoon` for vertical, dramatic, mobile-first storytelling
4. Pick a style preset from `presets/styles.json`.
5. Build a compact `panel plan`.
6. Render panel by panel.
7. Validate, retry if needed, then assemble the final output.

## Compatibility with v1

Keep the old experience as the default:
- If the user simply says "画成漫画" or gives a short story, still auto-select a reasonable format and style.
- Keep broad support for comics, picture books, and infographics.
- Keep the v1 ideas of storyboard confirmation, character cards, scene labels, clean-image suffixes, and PIL-based assembly.

New in v2:
- Use style IDs instead of only prose style names.
- Store storyboard as structured JSON.
- Track retries and fallbacks per panel.
- Make single-panel regeneration a first-class path.

## Core workflow

### 1. Analyze the request

Identify:
- content type
- likely visual form
- target audience
- tone
- whether the request contains a stable protagonist, multiple scenes, or mainly conceptual information

If the task is obvious, present a compact plan and continue.
Ask the user to confirm before rendering when any of the following is true:
- the content could reasonably become more than one visual form
- the style choice materially changes tone
- the story needs more than 8 panels
- the request contains private or sensitive photo material
- the user supplied copyrighted third-party source text that may need summarization first

### 2. Create the story/panel plan

Represent the visual plan with the schema in `schemas/panel-plan.schema.json`.

Requirements:
- one key beat per panel
- panel count should match narrative complexity
- the last panel should carry payoff, twist, conclusion, or CTA
- keep dialog short enough to remain readable after layout
- if scenes change, make transitions legible

For infographic mode:
- use `visual_form = infographic`
- use `format = single`
- still produce a `panels` array, usually with one major page and multiple structured sections inside the scene/action/must_include fields

### 3. Load or create the character bible

Two paths:

**a. Default protagonist asset（默认路径）**

If the user does not name or describe a protagonist, load the shipped character card before storyboarding:

- read `characters/protagonist.md` (default: black short hair, round glasses, slim young woman)
- inject its visual anchors into every panel prompt (see step 4), so the protagonist stays consistent across panels *and across sessions*
- never modify the default card; it is a shipped asset
- `characters/protagonist-ref.png` is an optional reference sheet; use it only when the host image tool accepts reference images, otherwise rely on the text anchors alone

**b. Custom protagonist（用户指定主角）**

If the user names or describes a protagonist, **build a structured character card** instead of a loose bible entry — the card is what keeps that character from drifting across panels and sessions.

- generate one: `python3 scripts/character_card.py init --name 小陈 --hair "short black hair" --eyewear "round glasses" --build slim --out characters/cards/xiaochen.json`
- or migrate an existing bible entry: `python3 scripts/character_card.py from-bible <plan.json> --name 小陈 --out characters/cards/xiaochen.json`
- `characters/cards/*.json` is auto-loaded; matching is by `character_id` or `name`
- inspect / verify: `python3 scripts/character_card.py list` and `python3 scripts/character_card.py check`
- do not modify `characters/protagonist.md` or `presets/default_character.json`; they are shipped assets
- template: `presets/character-card.template.json`, schema: `schemas/character-card.schema.json`

Minimum character anchors:
- age/gender presentation when relevant
- hair
- face shape
- eyewear if any
- outfit
- accent color
- body build or silhouette
- vibe/expression

Keep these anchors stable across all panels. Note which fields are anchor-eligible below — outfit and accent color are meant to change per scene.

**c. 锚点规则对默认主角和自定义角色完全一致（自动兜底）**

`scripts/compile_prompt.py` 逐角色保证锚点进 prompt，不依赖模型每次现场记得填写。规则只有一套，区别只在锚点来源：

| 情况 | 行为 |
|---|---|
| 角色有卡片 | 用卡片的 `hard_anchors`；卡片没写则从卡片 `appearance` 推导 |
| 角色没有卡片 | 从分镜里该角色自己的 `appearance` 推导（分镜字段本身就是结构化模板） |
| `character_bible` 缺失/为空 | 注入默认主角卡（`character_guard.injected = true`） |
| 信息图 `visual_form = infographic` | 不注入、不检查（无角色一致性需求） |

- 推导用的锚点字段：**hair / eyewear / build**；三者都没填才退回 face / outfit / accent_color 之一
- `outfit` 与 `accent_color` 默认不做锚点——服装和配色要能按场景换
- 补齐项记录在 `character_guard.patched_anchors`；逐角色的锚点来源与补齐明细在 `character_guard.characters[]`
- 完全关闭：`--no-character-guard`
- 卡片目录可换：`--character-card-dir <dir>`；额外卡片：`--character-card <path>`（可重复）

默认主角的硬锚点是**黑色短发 / 圆框眼镜 / 纤细体型**三项，任何画风、任何一格都不允许改变。自定义角色的锚点由它自己的卡片或 appearance 决定，同样不允许帧间漂移。

`scripts/validate_panel_plan.py` 在渲染前**逐角色**拦截三类问题：分镜缺 `character_bible`、某个角色 `must_keep` 缺锚点、角色没有任何可锚定的外观字段。它只做提醒，不做修改——补齐交给 compile 阶段。

### 4. Select and compile style preset

Use `presets/styles.json` as the source of truth for supported styles.

Each render prompt should combine:
- style positive template
- character-bible summary
- panel scene
- panel action
- shot type
- emotion
- must-include list
- avoid list
- global clean-image suffix

If the user gives a reference style image or a very specific style direction:
- preserve the selected `style_id`
- add a short reference-derived modifier instead of replacing the whole preset
- do not promise exact style cloning

### 5. Render panel by panel

Do not render the full page in one shot unless the request is explicitly a single illustration or infographic.

For comics or picture books:
- generate each panel independently
- keep output paths and retry records separate
- prefer clean images without embedded panel numbering
- if in-image text is unavoidable, keep it short and in English for image generation reliability
- add Chinese captions, narration, or labels during assembly when possible

### 6. Validate each panel

Validate against these priorities:
- character consistency
- scene continuity
- clean image without watermark/signature/panel numbering
- readable composition
- dialog within `text_budget`
- no obviously broken face or limb rendering

If a panel fails validation, retry with a bounded mutation ladder.

### 7. Retry policy

Use `schemas/render-task.schema.json` for retry bookkeeping.

Retry ladder:
1. shorten dialog or move text out of the image
2. simplify background and reduce secondary props
3. switch to a more stable shot such as `medium`
4. reduce side characters
5. fall back to a more stable style preset when appropriate

Stop conditions:
- default maximum 2 retries per panel unless the user explicitly wants more
- if the panel still fails after fallback, return the best valid storyboard plus the strongest attempt rather than silently looping

### 8. Assemble final output

Assembly defaults:
- `4-panel`: 2x2 grid
- `6-panel` or `8-panel`: balanced grid with consistent gutters
- `webtoon`: vertical stack
- `single`: single page or single image

Assembly rules preserved from v1:
- crop to target ratio before final resize
- avoid panel numbering inside generated images
- keep a clean margin and readable caption area
- use warm off-white backgrounds for comic boards unless the chosen style clearly calls for another background

#### 交付形态：静态拼版 或 单文件 HTML 绘本

两种出口，按用户要「一张图」还是「能翻着看的东西」来选：

- **静态拼版**（上面那些 grid 规则）：输出 PNG，适合发朋友圈、做封面、贴进图文。
- **单文件 HTML 绘本**：`scripts/assemble_book.py`，把每格 PNG + 旁白 + 对白气泡装订成**一个 .html**。
  - 图片走 base64 内嵌，CSS/JS 全内联，**断网可看、可直接发给别人、无需服务器**。
  - 纯 Python 标准库，零依赖；不重新出图、不调用图像模型、不改动原图。
  - 不加水印、不埋统计、不发任何请求；页脚只写作者与格数。
  - 手机竖版优先（默认内容宽 750px），CSS scroll-snap 做原生分页，关掉 JS 也能上下滑动读完。

```bash
# 先体检：哪格缺图、哪句对白太长
python3 scripts/assemble_book.py --check --plan plan.json --images ./renders

# 出成品
python3 scripts/assemble_book.py --plan plan.json --images ./renders \
  --out book.html --title "我的漫画日记" --author "巴扎嘿" --theme paper

# 先出文本校对版（不嵌图），确认台词再出正式版
python3 scripts/assemble_book.py --plan plan.json --images ./renders \
  --out draft.html --cleaning
```

图片命名默认按 `panel_01.png` / `panel-1.png` / `01.png` 自动匹配；缺图时留**带标注的占位框**（写明第几格 + 场景描述），补完图重跑即可，不会留一个看不出问题的空白洞。

主题：`paper`（默认暖纸）/ `ink`（深色）/ `clean`（纯白）。

## Hard constraints

### Character consistency

If the story has a main character, every panel should clearly look like the same person.
Reuse the same core descriptors and avoid drifting outfit, hair, face shape, or accent color.

### Language separation

Prefer:
- English for minimal in-image text if generation quality depends on it
- Chinese for captions, narration, or post-assembly overlay

If the user explicitly wants all-Chinese bubbles, try it, but still favor readability and brevity.

### Chinese dialogue and layout (中文对白与排版约束)

When the target language is Chinese (zh-CN), enforce these extra readability rules on top of `text_budget`. These are document-level guidance for planning and assembly; the JSON schemas are unchanged.

**对白与旁白的字数上限（基于中文排版可读性）：**
- 单个对话气泡：建议 ≤ 16 字（含中文标点占位，超出则拆句，不放第二行硬塞）
- 整格内所有对白合计：建议 ≤ 40 字（含标点）
- caption / 旁白单格：建议 ≤ 25 字（含标点）
- 上述字数按"每个全角字符占 1 字"计数（含标点）；若必须放入英文、数字或拼音，按 1 个半角字符 ≈ 0.6 字折算占用，避免超限

**中文标点规范：**
- 对话内一律使用中文标点：逗号「，」、句号「。」、问号「？」、感叹号「！」；不用半角 `,` `.` `?` `!`
- 省略号用中文「……」；引号内对话用「」或“”；破折号用「——」
- 不使用连排标点（如 `。。` `！！`）；标点占位会影响字数预算

**气泡内的排版建议：**
- 单气泡内不换行过多：短句优先（一句一个停顿）
- 整格对白超 40 字时，拆到多格 / 多气泡，或用旁白承接，绝不让一格塞满小字
- 心情、环境等"可画出来"的信息不要写进对白，留给画面

**竖排文字场景：**
- 默认对白用横排（现代中文阅读习惯 + 生图可读性）
- 仅在标题、古风 / 竖排叙事、或用户明确要求时使用竖排；竖排时每列 ≤ 12 字，气泡按列排布，拼版时再叠文字
- 生图阶段文字不可控，竖排文字一律在拼版层处理，不在格内依赖 AI 直出

**拼版时中文标题区建议：**
- 若作品有中文标题，拼版时预留独立标题区（顶部标题条或封面区），不在第一格内直接画字
- 中文标题建议 ≤ 12 字；副标题 ≤ 20 字
- 标题区需匹配正文字体族（同一套 CJK 字体），避免系统字体缺字（如宋体 / 黑体未覆盖的生僻字）

### Scene continuity

Use clear indoor/outdoor/street/home/office/etc. tags in planning when scene continuity matters.
Add a transition panel if a major scene jump would feel abrupt.

### Clean image rule

Use a clean-image suffix equivalent to:
- no border
- no panel frame
- no watermark
- no AI signature
- no accidental page numbering
- edge-to-edge composition

### Copyright boundary

Allowed:
- user-owned stories
- user summaries of ideas or experiences
- original educational reframing

Disallowed:
- direct transformation of substantial copyrighted text or art into near-derivative output
- exact imitation of a protected living artist's signature style

## Output contract

Default user-facing output should include:
- a compact explanation of chosen visual form and style
- a short storyboard summary
- final image(s) or assembled page
- concise notes if any panel required retries or fallback

Internally keep these artifacts whenever useful, using the naming convention from `Quick commands`:
- `panel_plan.json`
- `prompts/NN.md` per panel
- `pages/NN-<slug>.png` per panel
- per-panel render task records and retry notes

Do not force raw JSON on the user unless they ask for it or the task benefits from editable intermediate output.

## Style system

Supported style presets live in `presets/styles.json` (12 presets).

`presets/styles.json` is the source of truth; the list below is a human-readable summary:
- `cute-cartoon` — bright cute cartoon / 明亮可爱卡通
- `watercolor-picture-book` — warm watercolor picture book / 温暖水彩绘本
- `shonen-manga` — Japanese shonen manga / 日式少年漫画
- `slice-of-life-color` — colorful slice-of-life manga / 彩色日常漫画
- `gongbi-comic` — Chinese gongbi comic / 国风工笔漫画
- `ink-wash-comic` — ink wash comic / 写意水墨漫画
- `toon-3d-animation` — 3D cartoon animation / 3D 卡通动画
- `claymation` — claymation / 黏土定格
- `sci-fi-future` — sci-fi future comic / 科幻未来漫画
- `vintage-watercolor-travelogue` — vintage watercolor travelogue / 复古手绘水彩
- `doodle-sketch` — doodle sketch comic / 潦草涂鸦风
- `naive-crayon-sketch` — naive red-blue crayon doodle / 红蓝蜡笔稚拙涂鸦

`naive-crayon-sketch` note: use it for photo-to-doodle redraws (often a top-photo / bottom-doodle contrast layout), travel memory keeping, and childlike records. Its `fallback_style_id` is `doodle-sketch` and its `stability_rank` is 2, so it is a reasonable first choice for casual travel material but should fall back quickly if faces turn unreadable.

When a request is ambiguous, recommend 2 to 3 styles instead of forcing a single one.

## Tone system

画风决定「长什么样」，语气决定「怎么说话、什么情绪」——两者正交，可任意组合。语气预设存在 `presets/tones.json`（6 档），默认 `warm-healing`。

| tone_id | 名称 | 一句话 |
|---|---|---|
| `warm-healing` | 温暖治愈 | 柔光、日常细节、不制造冲突 |
| `playful-snark` | 幽默吐槽 | 夸张反应、自嘲优先、一句一个梗 |
| `calm-documentary` | 冷静纪实 | 观察式构图、先事实后判断 |
| `deadpan` | 冷幽默 | 面瘫对荒诞、不解释笑点 |
| `lyrical` | 诗意抒情 | 留白、季节感、短句分行 |
| `energetic` | 元气热血 | 动态姿势、上升势能、短促有力 |

每档含三样东西：`prompt_fragment`（拼进画面 prompt）、`negative_additions`（并入 negative）、`dialogue_rules`（对白怎么写）。命令行：`--tone deadpan`。

## Chinese scenario bundles

中文场景预设包在 `presets/bundles.json`（4 组），把「画风 + 语气 + 版式 + 中文对白纪律」一次配好：

| bundle_id | 场景 | 画风 / 语气 | 对白纪律 |
|---|---|---|---|
| `diary-strip` | 日记条漫（3-4 格 3:4） | slice-of-life-color / warm-healing | 单气泡 ≤16 字、整格 ≤40 字 |
| `knowledge-picturebook` | 知识绘本（3 格 4:3） | watercolor-picture-book / calm-documentary | 一格一个概念，概念名要出现在画面里 |
| `family-quad` | 亲子四格（2×2 1:1） | naive-crayon-sketch / playful-snark | 至少一格只有表情不说话 |
| `poetry-strip` | 诗词条漫（3 格 3:4） | gongbi-comic / lyrical | 古诗只引用不改写，原句核对通行版 |

优先级：命令行 `--tone` > panel plan 里的 `tone_id` / `style_id` > bundle 默认值。bundle 只提供默认值，不锁死。

```bash
python3 scripts/compile_prompt.py plan.json --bundle poetry-strip            # 全套默认
python3 scripts/compile_prompt.py plan.json --bundle poetry-strip --tone deadpan  # 只换语气
```

## Example resources

If you need a concrete starting point, read:
- `examples/four-panel-demo.json`
- `examples/chinese-webtoon-demo.json` (zh-CN diary/slice-of-life webtoon example)
- `characters/protagonist.md` (default character card)
- `presets/default_character.json` (structured version of the default card — used by compile/validate for anchor guarding)
- `presets/character-card.template.json` (template for custom character cards)
- `characters/cards/` (custom character cards, auto-loaded)
- `scripts/character_card.py` (`init` / `from-bible` / `check` / `list`)
- `scripts/assemble_book.py` (panel images → single-file HTML picture book)
- `presets/styles.json`
- `schemas/panel-plan.schema.json`
- `schemas/character-card.schema.json`
- `schemas/render-task.schema.json`

## Quick commands（快速指令）

These are shortcuts over the core workflow; they reuse the same schemas, retry policy, and character bible.

- `只出分镜` / `storyboard only` — stop after the panel plan; render nothing. Cheapest way to iterate on narrative before spending image calls.
- `重出第 N 格` / `重出 2,5,8` / `regenerate N` — regenerate only the listed panels. Reuse `panel_plan.json` and the compiled prompts, re-render just those panels, keep all other panels untouched, and record the update in the render-task notes.
- `换画风保留分镜` — keep the panel plan, recompile prompts with a different style preset, re-render all panels.
- `装订成绘本` / `出成一本能翻的` — after panels are rendered, run `scripts/assemble_book.py` to produce a single-file HTML picture book (embedded images, offline-viewable, forwardable). Add `--cleaning` first if the user wants to proofread the text before finalizing.

Artifact naming convention (when saving to disk):

- `panel_plan.json` — the storyboard / panel plan
- `prompts/NN.md` — compiled prompt for panel NN
- `pages/NN-<slug>.png` — rendered image for panel NN

`NN` is the 1-based panel index matching the order of the `panels` array. The mapping between `prompts/`, `pages/`, and the panels array is what makes single-panel regeneration reliable.

## Revision behavior

When the user asks for changes:
- prefer single-panel repair when the issue is local
- change style preset only if the issue is stylistic, not compositional
- change the storyboard only if the problem is narrative
- carry forward the validated character bible and successful panels whenever possible

## 相关 skill / Related skills

- 想固定某个画风、而不是一次性生成：先用 `style-card` 从参考图反推风格卡，再回来按卡出图。
