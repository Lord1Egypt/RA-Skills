---
name: song-translation-expert
description: |
  专业歌曲歌词翻译专家skill，将任意语种歌曲歌词翻译为中文（或反向），兼顾语义准确、押韵节奏、文化背景、流派特征与人设语气。
  涵盖 Pop / Rock / Hip-Hop / R&B / Country / Folk / Jazz / EDM / Musical / Vocaloid / 动漫 OP-ED / J-Pop / K-Pop / Latin / 法语香颂 / 德语 / 俄语 / 世界音乐等 20+ 流派。
  适用于：用户给出歌词要翻译、用户给歌曲名要找翻译、用户要求翻译时保留押韵/可唱性、用户要求逐行对照、用户要求加文化注释、二次元/动漫歌词翻译、K-Pop 翻译、欧美流行翻译、古典/民谣翻译。
  触发场景包括但不限于："帮我把这首歌翻译成中文"、"翻译歌词"、"这首歌什么意思"、"X歌曲中文版"、"翻唱歌词翻译"、"动漫 OP 翻译"、"V家曲翻译"、"歌词押韵翻译"、"双语对照歌词"、"song translation"、"lyrics translation"。
  涉及歌曲相关翻译、对照、注释、改写、本地化时都应优先使用此 skill。
---

# Song Translation Expert

## 1. 这个 skill 是什么

这是一个面向**歌词翻译**的专业 skill，沉淀自 44 首覆盖 8 种源语言、20+ 流派的真实翻译样本分析（详见 `assets/sample_corpus.json`）。它解决的核心问题是：**通用翻译模型处理歌词时常见的失败模式** —— 直译生硬、押韵丢失、文化典故错译、人设语气崩坏、流派特征消失。

歌词翻译与散文翻译的根本区别在于：歌词是**声音艺术 + 文学文本 + 文化载体**三者的复合。译文不仅要"意思对"，还要考虑：

- **可唱性**（节奏、音节数、停顿点是否与旋律匹配）
- **押韵**（原词押韵位置在译文中是否能再现）
- **声音质感**（开口音/闭口音、爆破音/鼻音的选择是否贴合情绪）
- **文化语境**（典故、俚语、历史背景是否需要保留或注释）
- **人设语气**（偶像曲的甜腻、说唱的硬核、民谣的疏淡是否传达）
- **流派惯例**（每种流派的翻译惯例不同，如 K-Pop 中"오빠"常音译为 oppa）

## 2. 何时使用

**强制触发**：用户提到"歌词翻译"、"歌曲翻译"、"X 歌中文版"、"动漫 OP 翻译"、"V家曲翻译"、"K-Pop 翻译"、"歌词中文意思"、"翻唱填词"、"双语歌词"等。

**推荐触发**：用户给出大段外文且明显是歌词（带 [Verse]/[Chorus]/段落反复结构），或用户讨论某首歌的"意思"、"故事"、"隐喻"，需要解释+翻译时。

**可不触发**：用户只是问歌曲的发行信息、艺人资料、专辑榜单等元数据（这种用 web-search 即可）。

## 3. 工作流程（核心）

### Step 1 — 识别输入类型

判断用户提供的输入是哪一种：

| 类型 | 识别特征 | 处理方式 |
|------|---------|---------|
| **完整歌词原文** | 用户直接粘贴多行外文 | 直接进入 Step 3 翻译流程 |
| **歌曲名 + 艺人** | 用户只给了曲名，需查找 | 用 web-search 找原文+参考译文，再 Step 3 |
| **歌曲 URL** | 用户给了音乐平台链接 | 用 web-reader 抓取，再 Step 3 |
| **音频/视频识别请求** | 用户要求识别歌曲 | 用 ASR/shazam 类工具，超出本 skill 范围 |

### Step 2 — 识别歌曲元信息

如果用户没给元信息，先尝试识别：

- **曲名 / 艺人 / 专辑 / 发行年**
- **语言**（关键！影响后续所有处理）
- **流派**（Pop / Rock / Hip-Hop / Vocaloid / K-Pop / 动漫 OP / 民谣 / 古典 / EDM / Musical / 拉丁 / 法语香颂...）
- **创作背景**（动漫主题曲？电影配乐？角色曲？社会运动歌曲？）
- **是否含多语种混合**（如 Despacito Remix 西语+英语、Waka Waka 西语+英语+斯瓦希里语）

### Step 3 — 翻译核心流程

按以下顺序处理：

#### 3.1 段落标记识别

歌词中的结构标记**不翻译**，原样保留：

- `[Intro]`, `[Verse 1]`, `[Verse 2]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`, `[Hook]`, `[Refrain]`
- `[Intro: Justin Bieber]`, `[Verse 1: Luis Fonsi & Daddy Yankee]` 这种带演唱者标记的也保留
- `[Drop]`, `[Beat drop]`, `[Solo]`, `[Instrumental]` 等电子/摇滚标记保留

#### 3.2 逐行翻译（不是整段翻译！）

**关键原则**：歌词翻译必须**逐行对照**，不能整段意译。原因：

1. 译文需要与原词行号一一对应，方便用户跟读
2. 演唱时每行的音节长度有上限，整段翻译会破坏节奏
3. 双语对照学习要求行级对齐

**翻译单位**：以一行为单位翻译。如果原行较长（如说唱中的快嘴段），可拆为两行译文，但要在两行间保留空行。

#### 3.3 应用六大翻译原则

详见 `references/translation_principles.md`，简述如下：

1. **可唱性优先** —— 音节数尽量贴近原文（±2 音节内）
2. **押韵再现** —— 副歌部分至少要做到 AABB / ABAB 押韵
3. **文化典故处理** —— 优先直译+脚注；高频典故可意译+加注释
4. **人设语气保留** —— 偶像曲的甜腻、说唱的硬核、民谣的疏淡必须传达
5. **流派惯例遵守** —— K-Pop 中"오빠"音译 oppa，V家曲中拟声词保留等
6. **多语种混合处理** —— 混入的英文短句在日语/韩语歌词中通常保留不译

#### 3.4 特殊元素处理

详见 `references/special_elements.md`：

| 元素 | 处理方式 | 示例 |
|------|---------|------|
| 拟声词 / Adlib | 保留原文或音译 | "Na na na" → "那那那" 或保留 "Na na na" |
| 罗马音 / 注音 | 删除（如果原文是日韩文，只保留汉字/谚文） | "残酷な天使" (ざんこくなてんし) → "残酷な天使" |
| 歌手名 / 角色名 | 保留原文 + 中文括注首次出现 | "初音ミク" → "初音ミク（初音未来）" |
| 地点 / 历史典故 | 直译 + 脚注 | "黄泉" → "黄泉"（脚注：日本神话中的死者世界） |
| 俚语 / 黑话 | 意译为主 + 脚注 | "drop bombs" → "炸翻全场" |
| Section markers | 原样保留 | `[Chorus]` 保留 |
| 跨语言嵌套 | 区分对待 | 西语歌中英文段保留+翻译 |

#### 3.5 输出格式

默认输出为**逐行对照**格式，每行原词后跟译文：

```
残酷な天使のように 少年よ 神話になれ
就像残酷的天使那样 少年啊 成为神话吧

蒼い風がいま 胸のドアを叩いても
纵然蓝色的微风在此刻 敲打着心门
```

如用户要求其他格式，可调整为：

- **整段对照**：原文段在前，译文段在后
- **表格对照**：Markdown 表格，左原右译
- **JSON 结构化**：`{"original": "...", "translation": "...", "notes": "..."}`

### Step 4 — 文化注释（可选但推荐）

对涉及文化典故、历史背景、双关语的歌词，应在译文后追加"译注"小节。每条译注：

- 标号清晰（注1、注2...）
- 简洁说明（一般 1-3 句）
- 关联到译文的具体位置

示例（来自 Hallelujah 翻译）：

> 哈利路亚，赞美主
> 煎熬中的国王编奏赞美我主 (注一)
> ...
>
> **译注**：
> 注一：指《圣经·撒母耳记下》中的大卫王，他为取悦上帝而奏琴。"baffled king" 既指大卫在道德困境中的挣扎，也暗指创作者在灵感枯竭时的状态。

### Step 5 — 输出文件

如果用户要求"下载"、"保存"、"生成文件"，按需生成：

- **Word 文档**：用 docx skill 生成，每首歌一节，原词译文并列
- **Excel 表格**：用 xlsx skill 生成，每首歌一行，列含曲名/艺人/流派/语种/原词/译文
- **PDF**：用 pdf skill 生成精美排版
- **JSON**：结构化数据，便于程序处理
- **Markdown**：默认聊天输出格式

详见 `references/output_formats.md`。

## 4. 流派专属指南

不同流派的翻译策略差异很大，处理前请先识别流派，再参考对应的指南：

- 日语歌曲（含 Vocaloid、动漫 OP/ED、J-Pop）：见 `references/japanese_songs.md`
- 英文歌曲（含 Pop、Rock、Hip-Hop、R&B、Country、Folk、Musical）：见 `references/english_songs.md`
- 多语种歌曲（含 K-Pop、Latin、法语香颂、德语、俄语）：见 `references/world_songs.md`

**为何要分流派**：日语歌词中的"古语/和制汉语"与英文 Hip-Hop 的"俚语/内部押韵"是完全不同的处理对象；K-Pop 翻译惯例（如 oppa 音译）与拉丁流行翻译惯例（如保留西语"Despacito"不译）也截然不同。统一指南会让模型在简单情况下过度注释，在复杂情况下又抓不住重点。

## 5. 翻译质量自检

完成翻译后，请按以下清单自检（详见 `references/quality_checklist.md`）：

- [ ] 每行原文都有对应译文（除非是纯音乐段）
- [ ] 段落标记 [Verse]/[Chorus] 原样保留
- [ ] 副歌部分押韵（AABB 或 ABAB）
- [ ] 音节数与原文差距不超过 ±2
- [ ] 文化典故已加注释
- [ ] 人设语气传达（偶像曲甜不甜、说唱硬不硬）
- [ ] 拟声词处理一致（全音译 or 全保留，不混用）
- [ ] 歌手/角色名首次出现有中英文对照
- [ ] 多语种混合段已正确区分处理
- [ ] 译文无直译生硬感（读起来像中文，不是翻译腔）

## 6. 常见陷阱与解决方案

### 陷阱 1：直译导致译文生硬

**反例**："Anyway the wind blows, doesn't really matter to me"
**错译**："反正风怎么吹，对我不太重要"
**正译**："但不论风如何吹拂我，这些都不会影响我"

**原因**：英文的 "anyway" 在这里是过渡副词，中文需要"但不论...都..."的让步结构才自然。

### 陷阱 2：押韵丢失

**反例**：Adele "Someone Like You" 副歌
- "Never mind, I'll find someone like you"
- "Don't forget me, I beg"

**错译**（不押韵）：
- "放心吧！我会找到一个像你一样的人"
- "我求你别忘了我"

**正译**（AABB 押韵）：
- "放心吧！我会找到一个像你一样的人"
- "我求你 别忘了我 也别忘 我们走过的路程"

### 陷阱 3：人设语气崩坏

**反例**：YOASOBI《アイドル》(偶像)
原词使用了大量「だわ」「のよ」「かしら」等女性语尾助词，呈现"甜腻偶像人设"。
**错译**：用普通陈述句翻译，丧失人设感
**正译**：在译文中加入"呀"、"哦"、"啦"等语气词，传达甜腻感

### 陷阱 4：文化典故错译

**反例**：Hallelujah 中 "the baffled king composing Hallelujah"
**错译**："困惑的国王编写哈利路亚"
**正译**："煎熬中的国王编奏赞美我主" + 脚注解释大卫王典故

### 陷阱 5：K-Pop 中"오빠"的处理

**惯例**：在 K-Pop 翻译社区，"오빠"（哥哥，女性对年长男性的爱称）通常音译为 "oppa" 而非意译为"哥哥"，因为：

- "哥哥"在中文语境中亲属感太强，缺乏韩语中的暧昧/亲昵色彩
- "oppa" 已成为 K-Pop 文化符号，目标读者（韩流粉丝）能理解

详见 `references/world_songs.md` 中 K-Pop 章节。

## 7. 工具脚本

skill 内置以下辅助脚本，位于 `scripts/` 目录：

| 脚本 | 用途 | 调用方式 |
|------|------|---------|
| `align_lyrics.py` | 将原文与译文按行对齐（解决行数不匹配问题） | `python align_lyrics.py orig.txt trans.txt` |
| `extract_section_markers.py` | 从歌词中提取段落标记，便于翻译时保留 | `python extract_section_markers.py lyrics.txt` |
| `detect_language.py` | 检测歌词主语言（支持日/英/韩/西/法/德/俄） | `python detect_language.py lyrics.txt` |
| `validate_translation.py` | 检查译文是否符合本 skill 的质量清单 | `python validate_translation.py orig.txt trans.txt` |
| `format_output.py` | 将对照歌词格式化为多种输出形式（Markdown/JSON/Excel） | `python format_output.py orig.txt trans.txt --format md` |

使用示例：

```bash
# 检测一首歌的语言
python /home/z/my-project/skills/song-translation-expert/scripts/detect_language.py input.txt

# 验证翻译质量
python /home/z/my-project/skills/song-translation-expert/scripts/validate_translation.py orig.txt trans.txt
```

## 8. 示例语料

`assets/sample_corpus.json` 收录了 44 首真实歌曲翻译样本，覆盖：

- 日语 19 首：千本桜、残酷な天使のテーゼ、夜に駆ける、Lemon、うっせぇわ、紅蓮華、廻廻奇譚、アイドル、前前前世、ブルーバード、紅蓮の弓矢、ウィーアー!、メルト、ワールドイズマイン、ローリンガール、青春コンプレックス、ミックスナッツ、新時代、だから僕は音楽を辞めた
- 英文 15 首：Bohemian Rhapsody、Imagine、Shape of You、Someone Like You、Lose Yourself、Smells Like Teen Spirit、Hotel California、Hey Jude、Rolling in the Deep、Bad Guy、Yesterday、Hallelujah、Let It Be、Wonderwall、Despacito Remix
- 多语种 10 首：Despacito (西)、Dynamite (BTS, 英)、La Vie en Rose (法)、99 Luftballons (德)、Alors on danse (法)、Waka Waka (西+英+斯瓦希里)、Con Altura (西)、Gangnam Style (韩)、Ya Soshla S Uma (俄)、DDU-DU DDU-DU (韩)

可参考这些样本了解不同流派、不同语种的翻译惯例。

## 9. 与其他 skill 的协作

- **docx skill**：当用户要 Word 文档输出时，配合生成排版好的歌词对照文档
- **xlsx skill**：当用户要批量歌曲 Excel 表格时
- **pdf skill**：当用户要精美排版的 PDF 歌词本时
- **web-search skill**：当用户只给歌名要找原词+参考译文时
- **web-reader skill**：当用户提供具体 URL 要抓取时

## 10. 限制与边界

- **不处理版权问题**：本 skill 只做翻译，不下载或分发受版权保护的音频/视频
- **不处理实时识别**：用户上传音频识别歌曲超出本 skill 范围，需用 ASR/shazam 类工具
- **机器翻译本质**：本 skill 提供高质量翻译，但仍为 AI 生成；对极致专业的出版级翻译需求，建议人工润色
- **古典/中古语言**：拉丁语、古英语、文言文等极冷门语种翻译质量会下降，应提示用户
- **方言/小语种**：粤语、闽南语、藏语等需特别提示用户期望

## 11. 快速决策树

```
用户提供歌词？
├── 是 → 识别语言+流派 → Step 3 翻译流程
│       ├── 简短（< 30行） → 直接翻译
│       └── 长篇（≥ 30行） → 分段翻译 + 汇总
└── 否 → 用户提供歌曲信息？
        ├── 是 → 用 web-search 找原词 → Step 3
        └── 否 → 询问用户具体想翻译哪首歌
```

输出需求判断：

```
用户要文件输出？
├── Word 文档 → 配合 docx skill
├── Excel 表格 → 配合 xlsx skill
├── PDF 文档 → 配合 pdf skill
└── 仅聊天输出 → Markdown 逐行对照格式
```

## 12. 完成标准

一次成功的歌词翻译应满足：

1. **完整**：每行原文都有译文，无遗漏
2. **准确**：意思忠实于原文，不增删关键信息
3. **流畅**：读起来像中文，无翻译腔
4. **可唱**：节奏感贴近原文，音节数相近
5. **押韵**：副歌部分押韵
6. **有灵魂**：传达原歌的情绪、人设、文化质感
7. **可学习**：文化典故有注释，目标读者能理解

满足以上 7 条即为合格译文。如用户有更高级需求（如要求严格可唱、要求保留原韵脚等），按需进一步打磨。

---

**参考文档**：
- 翻译原则详解：`references/translation_principles.md`
- 特殊元素处理：`references/special_elements.md`
- 输出格式规范：`references/output_formats.md`
- 质量自检清单：`references/quality_checklist.md`
- 日语歌曲专项：`references/japanese_songs.md`
- 英文歌曲专项：`references/english_songs.md`
- 多语种歌曲专项：`references/world_songs.md`
