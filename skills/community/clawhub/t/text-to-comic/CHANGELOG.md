# Changelog

## 3.0.0

本地版本，未发布。**新增交付出口：单文件 HTML 绘本**。此前 skill 只交 PNG 分格，用户拿到图还得自己拼；现在可以一步装订成「能翻着看、能发给别人」的一个文件。

### Added

- `scripts/assemble_book.py`：panel plan + 已生成的 PNG → **一份单文件 HTML 绘本**。
  - 图片 base64 内嵌、CSS/JS 全内联，**断网可看、可直接转发、无需服务器**。
  - 纯标准库零依赖；不重新出图、不调用图像模型、不改动原图。
  - **不加水印、不埋统计、不发请求**；页脚只写作者与格数（`--no-footer` 可关）。
  - 手机竖版优先（默认内容宽 750px）；CSS scroll-snap 原生分页，**关掉 JS 也能上下滑动读完**（渐进增强，不硬依赖脚本）。
  - 图片命名自动匹配 `panel_01` / `panel-1` / `01` 等多形态；**缺图留带标注的占位框**（写明第几格 + 场景），补图重跑即可。
  - `--cleaning` 出**文本校对版**（不嵌图），先确认台词再出正式版；`--check` 只体检（缺图 / 超长对白），不产文件。
  - 三套主题：`paper` 暖纸（默认）/ `ink` 深色 / `clean` 纯白。
  - 打印样式就位：`@media print` 关掉浮动提示、按格分页不断裂。
- 中文快速指令：`装订成绘本` / `出成一本能翻的`。

### Changed

- SKILL.md 第 8 步拆成两种出口：**静态拼版（PNG）** 与 **单文件 HTML 绘本**，按用户要「一张图」还是「能翻的东西」选。

## 2.8.0

Released 2026-10-27. 语气维度（tone）上线 + 4 组中文场景预设。画风决定长相，语气决定口吻与情绪，两者正交组合。

### Added

- `presets/tones.json`：6 档语气（warm-healing 温暖治愈 / playful-snark 幽默吐槽 / calm-documentary 冷静纪实 / deadpan 冷幽默 / lyrical 诗意抒情 / energetic 元气热血）。每档含 `prompt_fragment`（拼进画面 prompt）、`negative_additions`（并入 negative）、`dialogue_rules`（对白写法）。
- `presets/bundles.json`：4 组中文场景预设——`diary-strip` 日记条漫、`knowledge-picturebook` 知识绘本、`family-quad` 亲子四格、`poetry-strip` 诗词条漫。每组配好画风 + 语气 + 版式 + 中文对白字数纪律（如单气泡 ≤16 字）。
- `scripts/compile_prompt.py` 新增 `--tone` / `--tones` / `--bundle` / `--bundles`；输出增加 `tone_id` 与 `bundle_id` 字段。

### Changed

- 优先级明确为：命令行 `--tone` > panel plan 的 `tone_id`/`style_id` > bundle 默认值——bundle 只给默认，不锁死。
- 角色锚点仍紧跟画风模板，语气片段插在锚点之前，避免稀释角色一致性。

## 2.7.2

Released 2026-10-27. 内容 = 2.7.1 + 互挂段（与 `style-card` 互相引用：风格卡反推画风 → 本 skill 按卡出图）。功能零变化。

## 2.7.1

Released 2026-10-27. 重发版：内容与 2.7.0 完全一致（角色卡工程 + 锚点 + 逐角色校验），仅版本号换为 2.7.1——2.7.0 于 10-12 提交后卡在 ClawHub 安全扫描队列未上线且占住版本号，换号重发以绕开。

## 2.7.0

Released 2026-10-26. 自定义角色也走结构化模板。默认主角与自定义角色从此共用一套锚点规则。

### Added

- `scripts/character_anchors.py`：锚点逻辑的共享模块。负责归一化角色卡（兼容包裹式与扁平式两种写法）、推导硬锚点、补齐 `must_keep`。compile 与 validate 不再各写一份。
- `scripts/character_card.py`：角色卡工具。`init` 从命令行字段生成卡片；`from-bible` 把已有分镜里的角色迁成卡片；`check` 校验卡片结构与锚点自洽性（含重复 `character_id` 提示）；`list` 列出卡片与锚点。
- `presets/character-card.template.json`：自定义角色卡模板。
- `schemas/character-card.schema.json`：角色卡 schema，兼容包裹式（默认卡）与扁平式（用户手写）两种结构。
- `characters/cards/`：自定义角色卡目录，`README.md` 说明用法。目录下所有 `*.json` 自动加载。

### Changed

- **自定义角色不再被跳过**。2.6.0 里非默认主角会命中 `skipped_reason: custom character detected`，完全不受锚点保护；现在按同一规则处理：有卡片用卡片锚点，没卡片用它自己的 `appearance` 推导。
- `scripts/compile_prompt.py`：`--character-card` 改为可重复；新增 `--character-card-dir`（默认 `characters/cards`）。`character_guard` 新增 `characters[]` 逐角色记录锚点来源与补齐明细，并支持多角色各自的参考图（`reference_images`）。
- 锚点推导字段收敛为 **hair / eyewear / build**（与默认主角卡保持一致，不再自动锚 `face`）：脸型描述对模型的约束力弱于发型/眼镜/体型。三者全空时才退回 face / outfit / accent_color 之一。
- `scripts/validate_panel_plan.py`：改为逐角色检查，报错带角色名；新增「角色没有任何可锚定外观字段」检查。新增 `--character-card` / `--character-card-dir`。
- `schemas/panel-plan.schema.json`：`character_bible[]` 新增可选 `hard_anchors` 与 `reference_image`，自定义角色可以在分镜里直接带锚点，不必额外建卡片。
- 修复：`visual_form=infographic` 时不再注入默认主角（2.6.0 会给信息图塞一个无关角色）。
- `examples/four-panel-demo.json`：小陈的 `must_keep` 补上 `slim`（锚点完整性）。

## 2.6.0

Released 2026-10-26. 角色卡稳定性加固。JSON schemas 不变。

### Added

- `presets/default_character.json`：默认主角卡的结构化版本（appearance 全字段 + must_keep + 三条 hard_anchors + 参考图路径）。人类可读版仍是 `characters/protagonist.md`，两者需同步维护。
- `scripts/compile_prompt.py`：新增 `ensure_character_bible()` 与 `--character-card` / `--no-character-guard`。`character_bible` 缺失时自动注入默认主角卡；主角 `must_keep` 缺硬锚点时自动补齐；自定义主角不套用默认硬锚点；`visual_form=infographic` 不受影响。
- 编译产物新增 `character_guard` 字段：记录本次是否注入、补了哪些锚点、参考图路径，用于定位漂移来源。
- 首格 prompt 增加 `reference image:` 标记，提示宿主带上 `characters/protagonist-ref.png`。

### Changed

- `scripts/compile_prompt.py`：`character bible` 段落从 prompt 第 9 位前移到第 2 位（紧跟画风模板）——prompt 前段权重更高，锚点后置容易被场景描述稀释。
- `scripts/validate_panel_plan.py`：新增 `check_character_anchors()` 与 `--character-card` / `--skip-character-check`。渲染前拦截两类问题：分镜缺 `character_bible`、主角 `must_keep` 缺硬锚点（黑短发 / 圆框眼镜 / 纤细）。信息图模式跳过。
- SKILL.md：新增「硬锚点不会被漏掉（自动兜底）」小节；文件清单补 `presets/default_character.json`。
- 触发词补充：四格漫画、连环画、条漫、绘本分镜、漫画日记。
- SKILL.md frontmatter `version`: 2.5.2 → 2.6.0。

## 2.5.0

Released 2026-10-05. Adds one style preset. JSON schemas are unchanged.

### Added

- `presets/styles.json`: new style preset `naive-crayon-sketch`（红蓝蜡笔稚拙涂鸦 / Naive Red-Blue Crayon Doodle）— loose wobbly crayon outlines alternating red and blue (red for warm parts, blue for cool parts), pure white paper background with a small centered subject and huge margins, only 1-2 key subjects lightly colored, cobalt-blue vs orange-red complementary clash with a tiny yellow accent, waxy crayon + colored pencil grain. Built for travel-photo-to-doodle redraws and childlike memory keeping. Falls back to `doodle-sketch`; stability rank 2. Style presets: 11 → 12.
- SKILL.md frontmatter `version`: 2.4.2 → 2.5.0.

### Changed

- SKILL.md `Style system`: the preset summary list now carries all 12 `style_id` values with bilingual names, plus a usage note and fallback note for `naive-crayon-sketch`.
- `illustration/naga-bawa-crayon-doodle-2K.jpg`: reference render for the new preset.
- `README.md`: rewritten for 2.5.0 — removed the stale "2.0.0 draft" framing, corrected the preset count (11 → 12), and documented the actual repository layout including `characters/`, `illustration/`, and `scripts/assemble_page.py`.
- `skill-card.md`: description and version updated to 2.5.0, added the quick-command and default-character-card coverage.


## 2.4.2

Released 2026-09-29. Release-metadata fix only. No file content, schema, or behavior change.

### Fixed

- Restored the ClawHub display name to `Text-to-Comic · 文字转漫画`. Publishing 2.4.0/2.4.1 without `--name` caused ClawHub to fall back to the raw slug, which drops the Chinese search surface.
- Release note: **always publish with `--name "Text-to-Comic · 文字转漫画"`.** `clawhub publish --name "Text-to-Comic · 文字转漫画" --slug text-to-comic --version <v>`.

## 2.4.1

Released 2026-09-29. Ships the character reference sheet that 2.4.0 listed as planned. No behavior change.

### Added

- `characters/protagonist-ref.png`: actual character reference sheet (front / three-quarter / side full-body views + five-expression row), watermark-free. Used only when the host image tool accepts reference images; text anchors remain the source of truth.
- `characters/protagonist.md`: new 配套参考图 section describing when and how to use the sheet.

## 2.4.0

Released 2026-09-29. Default character asset + panel-level quick commands. JSON schemas are unchanged.

### Added

- `characters/protagonist.md`: default character card (black short hair, round glasses, slim young woman). Loaded automatically when the user does not name a protagonist; its visual anchors are injected into every panel prompt, keeping the protagonist consistent across panels and across sessions. Custom protagonists write a temporary `characters/custom-<slug>.md` instead of overwriting the shipped card.
- `characters/protagonist-ref.png`: character reference sheet, used only when the host image tool accepts reference images. *(planned in 2.4.0, shipped in 2.4.1)*
- SKILL.md `Quick commands（快速指令）`:
  - `只出分镜` / `storyboard only` — stop after the panel plan, render nothing
  - `重出第 N 格` / `重出 2,5,8` / `regenerate N` — regenerate only the listed panels, reusing the panel plan and prompts
  - `换画风保留分镜` — keep the storyboard, recompile prompts with a new style preset
- SKILL.md artifact naming convention: `prompts/NN.md` + `pages/NN-<slug>.png` mapped 1:1 to the panels array, making single-panel regeneration reliable.

### Changed

- SKILL.md frontmatter `version`: 2.3.1 → 2.4.0.
- SKILL.md `description`: adds default character card coverage (character card / 角色卡) and quick-command triggers (只出分镜 / 只重出某一格 / 换主角卡).
- SKILL.md step 3: renamed to "Load or create the character bible" — default asset path first, custom path second.
- SKILL.md `Example resources`: lists `characters/protagonist.md`.

## 2.3.1

Released 2026-09-13. ClawHub discoverability fix. Skill behavior is unchanged.

### Added

- SKILL.md `How it differs` section: states plainly that this is not a one-shot image generator, not a style-cloning tool, and not a research tool.
- SKILL.md frontmatter `version` field, for repository hygiene. The published registry version is derived by ClawHub itself.

### Changed

- SKILL.md `description`: now leads with an English problem statement plus a `Not for` clause (pure text writing / imitating a living artist's signature style / reproducing copyrighted material). Chinese trigger coverage retained.
- ClawHub catalog metadata: categories set from `other` to `creative`; topics set to `comic, storyboard, infographic, visual-storytelling, picture-book`.

## 2.3.0

Released 2026-09-04. Document-level Chinese typography and layout hardening plus a zh-CN example. JSON schemas are unchanged.

### Added

- `examples/chinese-webtoon-demo.json`: a zh-CN diary / slice-of-life webtoon example (black short hair + round glasses + slim female protagonist), following the same field structure as `examples/four-panel-demo.json`

### Changed

- SKILL.md `Hard constraints`: new "Chinese dialogue and layout (中文对白与排版约束)" subsection with concrete readability limits:
  - per speech bubble ≤ 16 characters, per-panel dialogue ≤ 40 characters, per-panel caption ≤ 25 characters
  - full-width Chinese punctuation requirements
  - short-line / split-gutter layout advice for bubbles
  - vertical-text handling guidance (assembly-layer only)
  - Chinese title-area suggestion during assembly (≤ 12 characters, matching CJK font family)
- SKILL.md `Example resources`: added pointer to `examples/chinese-webtoon-demo.json`

### Compatibility notes

- Slug remains `text-to-comic`
- `schemas/panel-plan.schema.json` and `schemas/render-task.schema.json` are unchanged; the new rules live at the document/planning level only
- Existing v1/v2 outputs remain valid

## 2.2.0

Released 2026-09-01. 新增 topics 与中英双语 description（含触发词），修复 README 版本/目录树问题。

## 2.0.0

This release upgrades the installed ClawHub release `1.0.0` into a publish-ready, structured v2 package.

### Added

- Structured `style preset` registry in `presets/styles.json`
- Structured `panel plan` schema in `schemas/panel-plan.schema.json`
- Structured `render task` schema in `schemas/render-task.schema.json`
- Example payloads in:
  - `examples/four-panel-demo.json`
  - `examples/infographic-demo.json`
- GitHub/ClawHub-oriented bilingual `README.md`
- Updated publishable `skill-card.md`
- `RELEASE_NOTES_2.0.0.md`
- `.gitignore` for local install artifacts
- Helper scripts:
  - `scripts/compile_prompt.py`
  - `scripts/validate_panel_plan.py`

### Changed

- Reframed the skill from a mainly prose-driven visual-director prompt into a staged workflow:
  - analyze
  - plan
  - style compile
  - render
  - validate
  - retry
  - assemble
- Preserved the original broad scope across comics, picture books, infographics, and hybrid outputs
- Preserved the original emphasis on:
  - content-type judgment
  - storyboarding
  - character consistency
  - scene continuity
  - clean-image composition
- Converted legacy style names into stable `style_id` values for repeatable behavior

### Compatibility notes

- Slug remains `text-to-comic`
- Frontmatter remains compatible with the current OpenClaw metadata expectations
- Simple natural-language requests still work without requiring users to provide JSON
- Structured JSON artifacts are additive, not mandatory for end users

### Expected benefits

- More stable output across retries
- Easier single-panel regeneration
- Better publishing review because intermediate artifacts are inspectable
- Less style drift because presets are explicit and reusable
- Easier future split into multiple specialized skills
