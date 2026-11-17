# text-to-comic v2.7.0

中文 | [English](#english)

当前发布版本：**2.7.0**（已发布至 ClawHub，slug `text-to-comic`）

## 中文

把文字、对话、日记、照片说明或知识内容，转成漫画 / 绘本 / 信息图 / 混合视觉页。

核心思路**不是一次性出图**，而是先出可审阅的分镜，再逐格渲染、逐格校验、逐格修复。

### 什么时候用

- 把故事画成漫画或绘本
- 把对话变成四格或短漫画
- 把概念 / 流程做成信息图
- 给旅行日记、照片笔记配图
- 只想改某一格、换个画风，而不想整页重画

### 什么时候不用

- 纯文字写作，没有视觉产出需求
- 精确模仿在世画家的标志性风格
- 直接复制受版权保护的第三方素材

### 它不是什么

- **不是一次性生图工具。** 先产出分镜和 panel plan，确认后再渲染；支持单格重试，而不是整页重画。
- **不是风格克隆工具。** 从精选 preset 中推荐，拒绝模仿在世画家的签名风格。
- **不是研究工具。** 它可视化你已经有的材料，不会替你去找或核实原始资料。

## 工作流

1. **分析请求** — 判断内容类型、视觉形式、目标受众、语气
2. **生成分镜** — 按 `schemas/panel-plan.schema.json` 输出结构化 panel plan
3. **加载角色卡** — 用户没指定主角时用默认角色卡；指定了主角就用 `characters/cards/` 下的自定义卡。两种卡走同一套锚点保护，保证跨会话一致
4. **编译画风** — 从 `presets/styles.json` 选 preset，编译成逐格 prompt
5. **逐格渲染** — 一次一格，不整页一次性生成
6. **校验** — 角色一致性 / 场景连续性 / 无水印无编号 / 可读性 / 字数预算
7. **重试** — 按阶梯式策略局部修复，默认每格最多 2 次
8. **拼版** — 2×2 / 2×3 / 竖版条漫 / 单页，标题与旁白在拼版层叠加

内容复杂时，会在出图前先跟你确认视觉形式和画风选择。

## 自定义角色卡

用户指定主角时，不要只写一段描述——给它一张结构化角色卡，锚点才锁得住。

```bash
# 新建
python3 scripts/character_card.py init --name 小陈 \
  --hair "short black hair" --eyewear "round glasses" --build slim \
  --out characters/cards/xiaochen.json

# 从已有分镜迁移
python3 scripts/character_card.py from-bible examples/four-panel-demo.json \
  --name 小陈 --out characters/cards/xiaochen.json

# 检查 / 列出
python3 scripts/character_card.py check
python3 scripts/character_card.py list
```

`characters/cards/*.json` 会自动加载，按 `character_id` 或 `name` 匹配分镜里的角色。锚点从 `hair` / `eyewear` / `build` 推导（三者全空才退回 face / outfit / accent_color）；`outfit` 与 `accent_color` 默认不锁，服装和配色要能按场景换。渲染前 `validate_panel_plan.py` 会逐角色检查，编译时 `compile_prompt.py` 会兜底补齐。

## 画风库

`presets/styles.json` 收录 **12 种**画风，每种包含 `style_id`、中英文名称、正负向 prompt、`use_cases`、`avoid_cases`、`fallback_style_id`、`stability_rank`。

| style_id | 中文名 |
|---|---|
| `cute-cartoon` | 明亮可爱卡通 |
| `watercolor-picture-book` | 温暖水彩绘本 |
| `shonen-manga` | 日式少年漫画 |
| `slice-of-life-color` | 彩色日常漫画 |
| `gongbi-comic` | 国风工笔漫画 |
| `ink-wash-comic` | 写意水墨漫画 |
| `toon-3d-animation` | 3D 卡通动画 |
| `claymation` | 黏土定格 |
| `sci-fi-future` | 科幻未来漫画 |
| `vintage-watercolor-travelogue` | 复古手绘水彩 |
| `doodle-sketch` | 潦草涂鸦风 |
| `naive-crayon-sketch` | 红蓝蜡笔稚拙涂鸦（2.5.0 新增） |

画风是**推荐而非硬限制**；但同一页内不混用风格。请求模糊时推荐 2–3 种让用户挑。

`naive-crayon-sketch` 适合照片转涂鸦（上方原图、下方插画对照）、旅行记忆、稚拙记录；`fallback` 为 `doodle-sketch`，`stability_rank` 2。

## 快速指令

| 指令 | 作用 |
|---|---|
| `只出分镜` / `storyboard only` | 停在 panel plan，不渲染。省图像调用成本 |
| `重出第 N 格` / `重出 2,5,8` | 只重渲染指定格，复用已有分镜和 prompt |
| `换画风保留分镜` | 保留分镜，换画风重新编译并重渲染 |

## 目录结构

```text
.
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── skill-card.md
├── presets/
│   ├── styles.json                    # 12 种画风
│   ├── default_character.json         # 默认主角卡（结构化）
│   └── character-card.template.json   # 自定义角色卡模板
├── schemas/
│   ├── panel-plan.schema.json         # 分镜计划
│   ├── character-card.schema.json     # 角色卡
│   └── render-task.schema.json        # 渲染任务 / 重试记录
├── characters/
│   ├── protagonist.md                 # 默认角色卡
│   ├── protagonist-ref.png            # 角色参考图（可选）
│   └── cards/                         # 自定义角色卡，自动加载
├── examples/
│   ├── four-panel-demo.json
│   ├── infographic-demo.json
│   └── chinese-webtoon-demo.json
├── illustration/
│   └── naga-bawa-crayon-doodle-2K.jpg # naive-crayon-sketch 效果图
└── scripts/
    ├── compile_prompt.py              # panel plan + preset → 逐格 prompt
    ├── validate_panel_plan.py         # schema 与业务规则校验
    ├── character_anchors.py           # 角色锚点的共享逻辑
    ├── character_card.py              # 角色卡 init / from-bible / check / list
    └── assemble_page.py               # 拼版与中文文字叠加
```

## 工具脚本

```bash
# 校验分镜
python3 scripts/validate_panel_plan.py examples/four-panel-demo.json

# 编译逐格 prompt
python3 scripts/compile_prompt.py examples/four-panel-demo.json

# 拼版（2x2 / 2x3 / webtoon / 长图）
python3 scripts/assemble_page.py --layout 2x2 --out pages/page-01.png pages/*.png
```

`compile_prompt.py` 会输出 `text_budget` 与 `text_budget_warning`，用于在出图前发现对白过长。

## 硬性约束

**角色一致性** — 有主角时每格都应明显是同一个人，复用相同核心描述词，不漂移发型、服装、脸型、点缀色。

**语言分离** — 图内文字需要稳定时用英文简短文字；中文说明、旁白、标签在拼版层叠加。

**中文排版** — 单个气泡 ≤ 16 字，整格对白合计 ≤ 40 字，caption ≤ 25 字；使用中文全角标点；标题 ≤ 12 字；竖排文字只在拼版层处理，不依赖 AI 直出。

**场景连续性** — 规划时用 `INDOOR` / `OUTDOOR` 等明确标记；场景跳跃过大时加过渡格。

**干净出图** — 统一追加：`no border, no panel frame, no watermark, no AI signature, no accidental page numbering, edge-to-edge composition`。

## 依赖

- `python3`
- 图像生成能力需启用（`image_gen.enabled`）
- 运行环境：darwin / linux

---

## English

Current release: **2.7.0** (published on ClawHub, slug `text-to-comic`).

Turn text, dialog, diary entries, photo notes, or knowledge notes into a comic, picture book, infographic, or hybrid comic+diagram page.

The key idea is **not one-shot image generation**. The skill produces a reviewable storyboard and panel plan first, then renders, validates, and repairs panel by panel.

### When to use

- draw a story as a comic or picture book
- turn dialog into a 4-panel or short comic
- turn a concept or workflow into an infographic
- illustrate travel notes, diary entries, or photo notes
- iterate on one panel or swap styles without redrawing the whole page

### When not to use

- pure text writing with no visual output
- exact imitation of a living artist's distinctive signature style
- direct reproduction of copyrighted third-party material

### How it differs

- **Not a one-shot image generator.** You get a storyboard and panel plan you can revise before rendering, plus per-panel retry instead of full-page redraws.
- **Not a style-cloning tool.** It recommends from curated presets and refuses to imitate a living artist's signature style.
- **Not a research tool.** It visualizes material you already have; it does not go find or verify the source content.

## Workflow

1. **Analyze** — content type, visual form, audience, tone
2. **Plan** — structured panel plan per `schemas/panel-plan.schema.json`
3. **Load character cards** — defaults to the shipped card when you do not name a protagonist; a named protagonist gets a structured card from `characters/cards/`. Both go through the same anchor guard.
4. **Compile style** — pick a preset from `presets/styles.json`, compile per-panel prompts
5. **Render panel by panel** — never the whole page in one shot
6. **Validate** — character consistency / scene continuity / no watermark or numbering / readability / text budget
7. **Retry** — bounded mutation ladder, 2 attempts per panel by default
8. **Assemble** — 2×2, 2×3, vertical webtoon, or single page; titles and captions overlaid at assembly

## Custom character cards

When a protagonist is named, give them a structured card instead of a loose description — that is what keeps the anchors locked.

```bash
python3 scripts/character_card.py init --name "Xiao Chen" \
  --hair "short black hair" --eyewear "round glasses" --build slim \
  --out characters/cards/xiaochen.json
python3 scripts/character_card.py from-bible <plan.json> --name "Xiao Chen" --out characters/cards/xiaochen.json
python3 scripts/character_card.py check
```

Cards in `characters/cards/*.json` are auto-loaded and matched by `character_id` or `name`. Anchors come from `hair` / `eyewear` / `build` (falling back to face / outfit / accent_color only when all three are empty). `outfit` and `accent_color` are intentionally left unanchored so costumes and palettes can change per scene.

## Style presets

`presets/styles.json` ships **12** presets, each with `style_id`, bilingual names, positive/negative prompt templates, `use_cases`, `avoid_cases`, `fallback_style_id`, and `stability_rank`.

`cute-cartoon`, `watercolor-picture-book`, `shonen-manga`, `slice-of-life-color`, `gongbi-comic`, `ink-wash-comic`, `toon-3d-animation`, `claymation`, `sci-fi-future`, `vintage-watercolor-travelogue`, `doodle-sketch`, `naive-crayon-sketch` (new in 2.5.0).

Styles are **recommended, not enforced** — but never mix styles within one page. When the request is ambiguous, recommend 2–3 options.

`naive-crayon-sketch` (红蓝蜡笔稚拙涂鸦) targets photo-to-doodle redraws with a top-photo / bottom-doodle contrast layout, travel memory keeping, and childlike records. Falls back to `doodle-sketch`, stability rank 2.

## Quick commands

| Command | Effect |
|---|---|
| `只出分镜` / `storyboard only` | stop after the panel plan, render nothing |
| `重出第 N 格` / `regenerate N` | re-render only the listed panels, reusing plan and prompts |
| `换画风保留分镜` | keep the storyboard, recompile with a different preset |

## Layout

```text
.
├── SKILL.md
├── README.md
├── CHANGELOG.md
├── skill-card.md
├── presets/                           # 12 styles + default_character.json + character-card.template.json
├── schemas/                           # panel-plan + character-card + render-task
├── characters/                        # default character card, reference sheet, cards/ (custom cards)
├── examples/                          # four-panel / infographic / zh-CN webtoon
├── illustration/                      # naive-crayon-sketch sample render
└── scripts/                           # compile_prompt / validate_panel_plan / character_anchors / character_card / assemble_page
```

## Hard constraints

**Character consistency** — every panel should read as the same person; reuse stable core descriptors.

**Language separation** — short English text inside images when generation reliability matters; Chinese captions and narration are overlaid during assembly.

**Chinese typography** — ≤ 16 characters per bubble, ≤ 40 per panel, ≤ 25 per caption; full-width CJK punctuation; vertical text is handled at the assembly layer, never by the image model.

**Scene continuity** — tag `INDOOR` / `OUTDOOR` explicitly; add a transition panel when a scene jump would feel abrupt.

**Clean images** — always append: `no border, no panel frame, no watermark, no AI signature, no accidental page numbering, edge-to-edge composition`.

## Requirements

- `python3`
- image generation must be enabled (`image_gen.enabled`)
- darwin / linux