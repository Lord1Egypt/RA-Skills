# 模板匹配规则

根据 `output/content.md` 的结构化内容，选择 `templates/manifest.json` 中的模板，生成 `output/slides.json`。

**共 14 个模板**：cover, contents, section-divider, content-left-text-right-image, content-one-columns, content-two-columns, content-three-columns, content-four-columns, data-highlight, quote, timeline, full-image, comparison, thank-you。

## 核心原则：按需选用

- **14 个模板 ≠ 14 页**：AI 根据内容量与结构**按需选用**模板，同一模板可**多次使用**。
- **一个章节可含多页**：若某章节内容较多，可拆成多页，每页选用最合适的模板（如多页 `content-three-columns`、多页 `content-one-columns` 等）。
- **防空防溢**：每块正文需在 content-rules 规定的**最少/最多行数**内，过少显空、过多溢出画板。超出则拆页或删减。

## 模板与用途对照

| templateId | 用途 | 适用场景 |
|------------|------|----------|
| cover | 封面 | 必用，第一页 |
| contents | 目录 | 有 2+ 章节时使用 |
| section-divider | 章节分隔 | 每个章节开头，大标题+配图 |
| content-left-text-right-image | 左文右图 | 1 主标题 + 3 组小标题正文 + 大图 |
| content-one-columns | 双栏卡片 | 1 主标题 + 2 组小标题正文（无图） |
| content-two-columns | 双栏带图标 | 1 主标题 + 2 组图标+小标题+正文 |
| content-three-columns | 三栏带图标 | 1 主标题 + 3 组图标+小标题+正文 |
| content-four-columns | 四栏 2x2 | 1 主标题 + 4 组图标+小标题+正文 |
| data-highlight | 数据展示 | 3 组数字+描述，黑底绿字 |
| quote | 金句页 | 长段引用/金句，4-5 行 |
| timeline | 时间轴/流程 | 3 步骤带编号+标题+正文，展示过程/步骤 |
| full-image | 全图声明 | 全屏背景图 + 大字声明 + 可选标签 |
| comparison | 对比页 | 左右两栏对比（绿底 vs 灰底），各 4 条 |
| thank-you | 致谢 | 必用，最后一页 |

## 匹配逻辑

### 1. 固定顺序
- 第 1 页：`cover`
- 第 2 页：若有目录则 `contents`，否则跳过
- 最后一页：`thank-you`

### 2. 章节循环
对每个章节：
1. 若有章节标题+金句+大图 → 用 `section-divider`
2. 根据内容块类型选内容页（**务必按内容匹配，优先使用多样化模板**）：
   - 1 主标题 + 3 组 + 大图 → `content-left-text-right-image`
   - 1 主标题 + 2 组（无图）→ `content-one-columns`
   - 1 主标题 + 2 组 + 图标 → `content-two-columns`
   - 1 主标题 + 3 组 + 图标 → `content-three-columns`
   - 1 主标题 + 4 组 + 图标 → `content-four-columns`
   - 3 组数字+描述 → `data-highlight`
   - 长金句 4-5 行 → `quote`
   - **3 步骤/流程/时间线/阶段** → **必须用** `timeline`（如：如何开始、实施步骤、路线图阶段）
   - **大图+一句宣言/愿景** → **必须用** `full-image`（如：品牌宣言、愿景页、过渡页）
   - **A vs B / 方案对比 / 前后对比** → **必须用** `comparison`（如：传统 vs 智能、Before vs After）

### 3. 槽位映射

从 content.md 提取字段，填入对应 slot：

- **cover**: title, subtitle, description, footer。**coverBackground 勿填**，使用模板默认背景；仅当用户明确要求自定义封面图时才填
- **contents**: title, intro, chapter1..chapter5
- **section-divider**: chapterNumber, title, subtitle, statement。**image 尽量勿填**，使用模板默认右侧插图；仅当用户明确要求更换章节配图时才填
- **content-left-text-right-image**: title, subtitle, block1Heading, block1Copy, block2Heading, block2Copy, block3Heading, block3Copy, image
- **content-one-columns**: title, subtitle, block1Heading, block1Copy, block2Heading, block2Copy
- **content-two-columns**: title, subtitle, block1Image, block1Heading, block1Copy, block2Image, block2Heading, block2Copy
- **content-three-columns**: title, subtitle, block1Image..block3Image, block1Heading..block3Heading, block1Copy..block3Copy
- **content-four-columns**: 同上，4 组
- **data-highlight**: title, subtitle, data1Num, data1Desc, data2Num, data2Desc, data3Num, data3Desc, slogan
- **quote**: quote, subtitle
- **timeline**: title, subtitle, step1Number, step1Heading, step1Copy, step2Number, step2Heading, step2Copy, step3Number, step3Heading, step3Copy
- **full-image**: image, statement, subtitle, tag
- **comparison**: title, subtitle, leftLabel, leftItem1..leftItem4, rightLabel, rightItem1..rightItem4
- **thank-you**: description

## slides.json 格式

根为数组，每项 `{ "templateId": "xxx", "slots": { "slotId": "value", ... } }`。槽位名与约束见 `templates/manifest.json`。

**完整示例**（14 种模板各一页，供参考）：见本 skill 目录下 `rules/slides-example.json`。生成时可复制后按 content.md 改写，注意 image 槽位可填：图片 URL、本地路径 `output/images/xxx.png`、或 `lucide:<icon-name>`（图标）。

```json
[
  {
    "templateId": "cover",
    "slots": {
      "title": "Qoder Work 2024",
      "subtitle": "智能开发新纪元"
    }
  },
  {
    "templateId": "contents",
    "slots": {
      "title": "目录",
      "intro": "本次发布涵盖以下内容",
      "chapter1": "01 产品概览",
      "chapter2": "02 核心能力",
      "chapter3": "03 落地案例"
    }
  },
  {
    "templateId": "section-divider",
    "slots": {
      "chapterNumber": "01",
      "title": "产品概览",
      "subtitle": "Product Overview",
      "statement": "重新定义智能开发"
    }
  },
  ...
]
```

## 注意事项

- **封面背景**：cover 的 `coverBackground` **不得**在 slides.json 中填写，否则会覆盖模板默认背景。仅当用户明确要求自定义封面图时才填。
- **章节分隔页插图**：section-divider 的 `image` **尽量勿填**，使用模板默认右侧插图。仅当用户明确要求更换章节配图时才填。
- 槽位值需符合 manifest 中 maxLength、type 等约束
- **字体**：模板统一使用黑体字（苹方 PingFang SC / 微软雅黑 Microsoft YaHei）
- **内容量**：遵守 content-rules 中的最少/最多行数，防空防溢
- 可选槽位可省略，不必在 slots 中写空字符串

### 图片槽位规则（type: image）

所有 `type: image` 的槽位支持三种值，**任选其一**：

| 填写方式 | 示例 | 适用场景 |
|----------|------|----------|
| `lucide:<icon-name>` | `lucide:shield-check` | 图标型配图（06/07/08 栏目卡片的首选） |
| 图片 URL | `https://example.com/photo.jpg` | 网络图片 |
| 本地路径 | `output/images/slide-03.png` | 生图保存到本地后引用 |

**何时必须生图/搜图**：manifest 中标记 `aiGeneratable: true` 且需要**真实配图**（而非图标）的槽位——典型场景是 `content-left-text-right-image` 的 image、以及 `full-image` 的 image（全屏背景）。此时**必须**调用 `generate_image` 或 `web_search` 获取。**例外**：`section-divider` 的 image 尽量勿填，使用模板默认。

**何时可直接用 Lucide**：06/07/08 栏目卡片的 `block*Image` 虽然也标了 `aiGeneratable: true`，但通常填 `lucide:<icon-name>` 即可，**无需生图**。仅当你需要用真实照片/插画替代图标时才调用生图。
