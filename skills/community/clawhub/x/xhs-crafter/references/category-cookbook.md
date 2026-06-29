# Category Cookbook

Per-category cheat sheet for common content types. Each entry maps a category to style mode, theme, recipes, and image source strategy.

When the user names a category, find the row here and start from the listed recipes instead of building from a blank file.

---

## 商业/科技分析 · Business & Tech Analysis

**Strongest fit for our skill.**

- **Recipes**: M01 (text-led cover) or M16 (image-led cover when hero image available), M04 (pull quote), M08 (pipeline), M12 (data cards), M07 (closing note)
- **Style mode**: Editorial × Indigo Porcelain (tech/AI) or × Ink Classic (general business). Swiss × IKB Blue for pure data posts
- **Theme**: Indigo Porcelain for tech/AI topics; Ink Classic for general business; IKB Blue for data-heavy analysis
- **Text scheme**: Text-beside-image for feature pages. Text-on-image only for cover with qualified photo. Body pages use serif text + data cards + pull quotes
- **Image source**: AI generated (editorial documentary style) > Unsplash (tech/office scenes) > Pexels (Chinese keyword search). Avoid stock handshake/laptop photos
- **Content shape**: 5-7 pages. Cover (hook + 1-line deck) → opening thesis + data → 2-3 evidence pages (pipeline/ledger/quote) → closing
- **Pitfalls**:
  1. Generic "industry analysis" voice without specific numbers. Cure: every claim needs a data point
  2. Too many data cards without narrative. Cure: alternate data pages with essay/quote pages
  3. Cover with vague hype instead of concrete hook

---

## 职场/干货 · Workplace & How-to

**Strong fit.** This is what Swiss-International was made for.

- **Recipes**: S01 (cover), S02 (comparison), S05 (warning rows), S06 (pipeline), S07 (takeaway ledger), S09 (KPI tower), S11 (stacked ledger)
- **Style mode**: Swiss × IKB Blue or × Safety Orange. Avoid lemon-yellow/lemon-green for serious content
- **Theme**: IKB Blue (default), Safety Orange (warning/urgent content)
- **Text scheme**: Text-only or text-with-diagram. Almost never text-on-photo (workplace photos read as stock)
- **Image source**: Avoid stock business photos. Prefer diagrams, screenshots of real artifacts (Notion, Linear, Figma), or omit. Generated images rarely add value
- **Content shape**: 5-9 pages. Cover question/claim → context KPI → 3-5 numbered insights as ledger → one comparison or pipeline diagram → takeaway
- **Pitfalls**:
  1. Listicle voice ("8 个让你..."). Cure: rewrite as numbered argument, not tips
  2. Cheap "advice" energy ("一定要", "千万别"). Cure: replace with observed action verbs + a number
  3. Stock-photo seasoning (handshake, laptop-with-coffee). Cure: omit, or use a small icon glyph

---

## 旅行/生活方式 · Travel & Lifestyle

**Strongest fit.**

- **Recipes**: M16 (image-led cover when user has great photos), M01 (text-led cover), M02 (field-note photo), M11 (marginalia essay), S11 (itinerary ledger), M07 (closing note)
- **Style mode**: Editorial × Kraft Paper (warm-tone destinations) or × Dune (art/creative destinations) or × Forest Ink (mountain/wilderness)
- **Theme**: Kraft Paper for warm/cultural trips; Dune for art/design destinations; Forest Ink for outdoor/nature
- **Text scheme**: Text beside image is default. Cover can use text-on-image only when photo has quiet zone. Body pages use photo + caption pairs (field-note style)
- **Image source**: User photos > Pexels (Chinese keyword search for domestic destinations) > Unsplash (overseas/English keywords) > Flickr CC (documentary feel)
- **Content shape**: 5-7 pages. Cover (destination + dates) → atmosphere photo + lead → itinerary ledger → 2-3 field notes → closing quote
- **Pitfalls**: Generic "best places in X city" listicle voice. Cure: keep one specific date/weather/mileage detail per page

---

## 教程/工具 · Tutorial & Tools

**Strong fit.** Screenshot treatment is the key differentiator.

- **Recipes**: S01 (cover), S06 (pipeline for steps), S08 (duo compare), S11 (stacked ledger for shortcuts), M04 (pull quote for key insight)
- **Style mode**: Swiss × IKB Blue (default) or × Safety Orange (warning tips). Editorial × Indigo Porcelain for long-form tutorials
- **Theme**: IKB Blue for tool tutorials; Indigo Porcelain for methodology tutorials
- **Text scheme**: Screenshot-heavy. Use `.frame-shot` + `.device-browser` for all screenshots. Text above/below screenshots, not beside
- **Image source**: User screenshots (mandatory for real tutorials). Use `.frame-shot` with device chrome + background texture. Never use stock UI screenshots
- **Content shape**: 5-8 pages. Cover (tool name + what you'll learn) → context → 3-5 step pages (screenshot + 1-2 sentence instruction) → tips/shortcuts ledger → closing
- **Pitfalls**:
  1. Screenshots too small to read. Cure: give screenshots 45-65% page height
  2. Full-screen dumps without focus. Cure: crop to relevant area, preserve readable UI labels
  3. Dark screenshots on dark background. Cure: use `.frame-shot` with paper-2 background

---

## 影视/读书 · Film & Books

**Strong fit** for reviews, scene analysis, quote cards.

- **Recipes**: M01 (cover), M04 (pull quote for memorable lines), M10 (evidence feature for scene analysis), M11 (marginalia essay), S02 (comparison), S12 (matrix for weekly roundups)
- **Style mode**: Editorial × Ink Classic or × Indigo Porcelain. Letterboxd visual vocabulary fits Editorial naturally
- **Theme**: Ink Classic (default for reviews); Indigo Porcelain (sci-fi/tech films); Kraft Paper (literature/classics)
- **Text scheme**: Text-beside-image for review cards (poster on left, take on right). Text-on-image only for atmospheric quote pages
- **Image source**: Official posters/stills. Do not generate fake stills. User photos of book covers acceptable
- **Content shape**: 5-7 pages. Cover (title + year + 1-line take) → 1-2 scene captures → director-quote/theme pullquote → verdict ledger
- **Pitfalls**:
  1. Fake film-festival typography (adding fake awards badges). Don't
  2. Spoiler in title without warning. Mark `剧透` in kicker if needed

---

## 游戏 · Gaming

**Strong fit** for journals, recaps, build lists. **Has image-rights risk.**

- **Recipes**: M01 (cover with full-bleed art), M08 (boss tier ledger), S07 (takeaway ledger), S11 (chapter timeline), M15 (build before/after)
- **Style mode**: Editorial dark (Ink Classic with paper inverted to near-black) for atmospheric games. Swiss for esports/competitive data
- **Theme**: Midnight Ink for atmospheric games; IKB Blue for esports/data
- **Text scheme**: Text-on-image is standard for game covers (game art is the primary draw). Use subject mapping from image-overlay.md
- **Image source**: Wallhaven for keyword pulls, official screenshots. Always disclose copyright risk and log to SOURCES.md
- **Content shape**: 4-6 pages. Cover (game name + playtime) → first impression → chapter ledger → memorable boss/scene → verdict
- **Pitfalls**: Score-card seriousness (8.5/10 in giant block). Keep verdict as one short clause, not a number

---

## 美食 · Food

**Split fit.** Recipes work. Food-photo showcase does not.

- **Recipes**: M16 (image-led cover with finished-dish photo), S11 (ingredient/price ledger), M14 (cooking steps pipeline), M02 (extra dish detail)
- **Style mode**: Editorial × Kraft Paper (cookbook feel). Swiss × Lemon Yellow/Safety Orange for "cost-per-serving" data posts
- **Image source**: User photos of finished dish are best. Pexels for Chinese food scenes. Unsplash food photos read as Western stock
- **Pitfalls**: Excited recipe voice ("超绝!!!"). Editorial doesn't shout — let the dish do the talking

---

## Capability Circle Summary

**End-to-end strong** (text + structure + image all from skill):
- 商业/科技分析 · 旅行 · 职场 · 推荐

**Strong on text/structure, needs user photos for image**:
- 影视/读书 · 游戏 · 美食(食谱) · 彩妆(教程) · 穿搭(精选/胶囊) · 家居 · 健身

**Outside scope** (skill cannot reliably produce — be explicit with user before designing):
- 美食(菜品大片摆盘) — 需要专业食物摄影，AI生图无法达到
- 穿搭(日常OOTD全身照) — 需要真实人物实拍
- 情感(梦核/氛围感装饰风) — 与 Editorial 和 Swiss 均冲突
- Y2K/千禧辣妹/哥特萝莉/kawaii装饰风 — 超出两种风格体系
- 纯摄影展示 — 图片本身就是交付物，排版无意义

Be explicit with the user when their request lands in "outside scope". Do not promise a result the system was not designed to make.

---

## 彩妆 · Makeup

**Split fit.** 教程方向强，大片展示方向弱。

- **Recipes**: S06 (pipeline for steps), S08 (duo compare before/after), M04 (pull quote for key tip), S11 (product ledger)
- **Style mode**: Swiss × Lemon Yellow (年轻活力) or × Safety Orange (大胆对比). Editorial × Dune for 高端品牌
- **Theme**: Lemon Yellow for 教程/入门; Safety Orange for 对比/警示; Dune for 高端品牌
- **Text scheme**: Text-beside-image. 步骤页用截图+简短说明，对比页用左右分栏
- **Image source**: 用户实拍妆容步骤图（必须）. 禁止AI生成人脸
- **Content shape**: 5-7 pages. Cover (妆容名称+效果预期) → 2-3 step pages → product ledger → before/after → tips
- **Pitfalls**:
  1. AI生成人脸做妆容示范 → 禁止，必须用户实拍
  2. 色号标注不清晰 → 每个产品标注品牌+色号

---

## 穿搭 · Outfit

**Split fit.** 胶囊衣橱/穿搭哲学方向强，日常OOTD方向弱。

- **Recipes**: S11 (单品 ledger), S02 (compare 对比搭配), M11 (marginalia essay for 穿搭哲学), M07 (closing note)
- **Style mode**: Editorial × Dune (极简穿搭) or × Kraft Paper (复古穿搭). Swiss × Lemon Yellow (年轻活力)
- **Theme**: Dune for 极简/设计感; Kraft Paper for 复古/手作; Lemon Yellow for 年轻/潮流
- **Text scheme**: Text-beside-image. 单品页用 ledger 列品牌+价格，搭配页用对比图
- **Image source**: 用户实拍穿搭图（推荐）. Pexels for 平铺图/单品图. 禁止AI生成全身照
- **Content shape**: 5-7 pages. Cover (穿搭主题+季节) → 核心理念 → 3-5 单品/搭配 → 购买清单 → closing
- **Pitfalls**:
  1. OOTD全身照用AI生成 → 禁止，必须用户实拍
  2. 纯链接堆砌无搭配逻辑 → 每个单品说明为什么选它

---

## 家居 · Home

**Strong on text/structure, needs user photos.**

- **Recipes**: M02 (field-note photo for 空间展示), S11 (好物 ledger), M11 (marginalia essay for 居住哲学), S06 (pipeline for 改造步骤)
- **Style mode**: Editorial × Kraft Paper (温暖手作) or × Dune (极简设计). Swiss × IKB Blue for 智能家居/数据
- **Theme**: Kraft Paper for 温馨/手作; Dune for 极简/设计; IKB Blue for 智能家居
- **Text scheme**: Text-beside-image. 空间页用大图+短文，好物页用 ledger
- **Image source**: 用户实拍家居图（推荐）. Pexels for 家居场景. Unsplash for 极简空间
- **Content shape**: 5-7 pages. Cover (空间类型+风格) → 理念/改造前 → 2-3 空间展示 → 好物清单 → closing
- **Pitfalls**:
  1. 纯产品堆砌无居住逻辑 → 每个物品说明为什么适合这个空间
  2. 网红风过度装饰 → Editorial克制，让空间说话

---

## 健身 · Fitness

**Strong on text/structure, needs user photos.**

- **Recipes**: S06 (pipeline for 训练计划), S09 (KPI tower for 数据), S11 (动作 ledger), S02 (compare 正确vs错误)
- **Style mode**: Swiss × Safety Orange (力量/警示) or × Lemon Green (健康/增长). Editorial × Forest Ink for 户外健身
- **Theme**: Safety Orange for 力量训练; Lemon Green for 有氧/健康; Forest Ink for 户外
- **Text scheme**: Text-only or text-with-diagram. 动作说明用 pipeline，数据用 KPI tower
- **Image source**: 用户实拍训练图（推荐）. 禁止AI生成肌肉/身材图
- **Content shape**: 5-7 pages. Cover (训练目标+周期) → 数据基线 → 3-4 训练步骤 → 饮食/恢复提示 → closing
- **Pitfalls**:
  1. AI生成身材图 → 禁止，用数据+文字代替
  2. 过度承诺（"7天练出马甲线"） → 用真实数据说话

---

## 情感 · Emotion

**Split fit.** 文字驱动方向强，梦核/氛围感方向弱。

- **Recipes**: M04 (pull quote), M11 (marginalia essay), M07 (closing note), M01 (text-led cover)
- **Style mode**: Editorial × Ink Classic (通用) or × Kraft Paper (温暖回忆). 避免Swiss——情感内容不适合工程感
- **Theme**: Ink Classic for 深度思考; Kraft Paper for 温暖回忆
- **Text scheme**: Text-only为主. 引言页用 pull quote，思考页用 marginalia essay
- **Image source**: 用户实拍生活图（推荐）. Unsplash for 氛围图. 禁止AI生成人物情绪图
- **Content shape**: 5-7 pages. Cover (核心感受) → 2-3 思考/引言 → 1 数据/对比 → closing quote
- **Pitfalls**:
  1. 梦核/氛围感装饰风 → 超出能力范围，明确告知用户
  2. 过度鸡汤 → Editorial克制，用观察代替说教

---

## 推荐 · Recommended

**Strong end-to-end, after specifying a subtype.**

- **Recipes**: S11 (推荐清单 ledger), S02 (compare 对比), M02 (field-note for 实物展示), M07 (closing note)
- **Style mode**: 取决于推荐类型——科技推荐用 Swiss × IKB Blue; 生活推荐用 Editorial × Kraft Paper; 设计推荐用 Editorial × Dune
- **Theme**: 按推荐类型路由——科技→IKB Blue, 生活→Kraft Paper, 设计→Dune, 数据→Lemon Green
- **Text scheme**: Text-beside-image. 清单页用 ledger，对比页用 compare
- **Image source**: 用户实拍产品图（推荐）. Pexels for 产品场景. 截图 for App推荐
- **Content shape**: 5-9 pages. Cover (推荐主题+数量) → 1-2 筛选标准 → 3-5 推荐项 → 对比/总结 → closing
- **Pitfalls**:
  1. 纯链接堆砌无筛选逻辑 → 每个推荐说明为什么选它
  2. 推荐项信息不足 → 每项至少包含：名称、价格/评分、一句话推荐理由
