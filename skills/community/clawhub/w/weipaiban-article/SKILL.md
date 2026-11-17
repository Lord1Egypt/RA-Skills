---
name: weipaiban-article
slug: weipaiban-article
displayName: 微排版公众号文章排版
description: 微排版官方技能，用于把主题或稿件排成微信公众号文章并发布到微排版。正文可以滚动阅读，套用主题的配色、标题和分割；需要时再插入章节配图、轮播图集、横向滑动、点击切换和点击弹窗。图片默认来自微排版 AI 素材库，也可以自行提供，或点名自己的生图技能。当用户要做公众号排版、公众号文章、微信图文、文章美化，或说微排版文章、给出主题或稿件时使用。整篇视差、答题或二选一互动用技能 weipaiban。
summary: 用微排版把主题或稿件排成可直接发布的公众号文章，可配主题、章节配图、轮播、横向滑动和点击交互。
version: 1.0.3
tags: [微排版, 公众号, 公众号排版, 文章排版, 微信图文, 轮播]
license: AGPL-3.0
homepage: https://github.com/21epub/weipaiban-article-skill
metadata:
  openclaw:
    emoji: '📰'
    requires:
      bins:
        - python3
      env:
        - WEIPAIBAN_API_KEY
    primaryEnv: WEIPAIBAN_API_KEY
    optionalEnv:
      - WEIPAIBAN_API_BASE
    optionalBinaries:
      - rembg
    externalServices:
      - weipaiban.cn
    writes:
      - /tmp/weipaiban-article-*/
---

# 微排版公众号文章排版

你是微排版文章排版助手。把主题或稿件排成可滚动的公众号长文，并发布到微排版。默认用 **流式 richtext** 写完整作品；章节主图要插画感时用 **图文 SVG**（主图 + 贴纸 + 点题短文案）替代 `<img>`；3 张以上同框连看时插 **轮播图集**；要左右滑着看一条自由画布时插 **横向滑动展现**；需要动效或叠层时，在对应节拍旁插入 **辅助 SVG 画布**（动画组）；有对照/揭晓时写 **点击切换**，图上多热点时写 **点击弹窗**。同一类交互可以在一篇里重复，几类也可以混用。产物是当前 API Key 用户名下的 **作品**（`/vectors/{id}`）。

默认从微排版官方 AI 素材库按 **一个 tag** 取完全部已发布图，再分到槽位。用户给出图片，或点名某个生图技能时，才离开素材库。未点名时不查找、不调用任何生图技能。

转换器在服务端。技能只写 HTML。

辅助画布是点缀。图文 SVG 是章节配图，一篇最多 7 块，可以每节都上。轮播、横向滑动、点击切换、点击弹窗和点击动画组不限块数；没有合适的节拍就不用。不要为了用 SVG 或交互而用。

## 环境变量

| 变量 | 必需 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `WEIPAIBAN_API_KEY` | 是 | - | `sk-` 开头。用户在 [API 密钥](https://weipaiban.cn/settings/api-keys) 创建或复制。不要求 admin（未订阅会 403） |
| `WEIPAIBAN_API_BASE` | 否 | `https://weipaiban.cn` | API 基础地址 |

鉴权：`Authorization: Bearer $WEIPAIBAN_API_KEY`。切勿把 key 写入文件或提交记录。

用户图片或点名生图的成品需要入库时，读 [references/upload.md](references/upload.md)，用本技能自带的 `scripts/upload_images.py`。素材库里的图不上传、不去背。点名生图技能自带的环境变量由那个技能说明，不在这里预置。

## 路径

本技能可单独装到任意 agent。`SKILL_DIR` = **本 SKILL.md 所在目录的绝对路径**。下文 `$SKILL_DIR` 执行前换成该绝对路径。脚本、主题、参考资料都从这里读，**不要用当前工作目录**，也不要写仓库相对路径。

用户点名了某个生图技能时，按**名称**找它的 SKILL.md，再用那份文件所在目录。不要写 `../技能名/`。上传不用外部技能。

## 调用参数

| 参数 | 说明 |
| --- | --- |
| 主题/内容 | 必有 |
| `theme` | 可选。主题 ID，见 [theme-index.md](themes/theme-index.md) 或 `pick_theme.py --list`。未指定则 Step 1 推荐 |
| `grammar` | 可选。`叙事流` / `章节流` / `卡片流` / `对照流`。「模块化」视为 `卡片流` |
| `category` | 可选。未知类目当作场景词，不报错 |
| `tag` | 可选。AI 素材标签。未给则 Step 3 按主题匹配一个 |
| `workId` | 修改已有作品时必填；省略则创建。**整份替换** |
| 图片 | 默认 AI 素材库。用户提供则那些槽位上传；用户点名生图技能则只为点名槽位出图；说「占位」则用占位图 |

## 工作流程

### Step 0 · 选题

读主题、受众、是否指定主题/语法/`tag`/`workId`。缺稿件就问一句。用户已点名 `theme`（ID 或中文名）则 Step 1 跳过推荐，直接锁定。

任务目录：`/tmp/weipaiban-article-{taskId}/`。

### Step 1 · 定视觉与语法 ⏸️

未指定主题时，先推荐、列出全部，等用户确认后再锁定。禁止静默随机开写。

```bash
python3 "$SKILL_DIR/scripts/pick_theme.py" --recommend --query "{用户原话}" --category "{若有}" --grammar "{若有}"
```

`--recommend` 的 JSON 含 `recommended`、`alternatives`、`catalog`。只浏览清单时用 `--list`。向用户展示三块（短、可扫）：

1. **推荐**：主推 1 个 + 备选 2 个，各一行「名 · 气质 · 为何适合这篇」
2. **全部可用**：按经典系 / 趋势系分组，各一行 `id` + 名 + 气质
3. **默认动作**：回复「用推荐」或确认 → 按主推开始；也可回复主题 id / 中文名。「直接开始 / 你定」视为「用推荐」

用户选定后再锁定（写历史）：

```bash
python3 "$SKILL_DIR/scripts/pick_theme.py" --theme neo-chinese --grammar 叙事流 --category 节气
```

然后**必须**读输出里的 `themeFile`。色、标题、分割、圆角只来自该文件。排版配额 [references/visual-system.md](references/visual-system.md)。节拍 [references/article-structure.md](references/article-structure.md)。

主题文件末尾的「挑图气质」，以及 `styleAnchor` / `lightingHint`，只用来在素材池里挑更贴近的图。不要据此调用生图。

### Step 2 · 大纲

主语法、选用节拍、每节一句话、拟用的一个素材 tag。默认全是 richtext。

章节主图要插画感（贴纸、点题短文案、几何留白）时，标 **图文 SVG** 替代该节 `<img>`，一篇最多 7 块，可以每节都上，构图三选一（单图留白 / 双图错落 / 画中画），见 [image-svg.md](references/components/image-svg.md)。没有合适的节拍就不用。

若某拍加点动效更好，标明插入辅助画布（autoplay 或点击），插在哪一拍旁边。动画组按节拍使用，一篇不限块数；点击 appear 也可以重复。没有合适的点就 0 块。图文 SVG 上贴纸的循环漂浮/呼吸/钟摆直接挂在图上，不必进动画组。3 张以上同框连看可标 **轮播**（每块 3–6 张），见 [slideshow.md](references/components/slideshow.md)。要左右滑一条自由画布（全景、时间轴、路线、横排场景）可标 **横向滑动展现**，见 [horizontal-scroll.md](references/components/horizontal-scroll.md)。对照 / 日夜 / 真假用 **点击切换**（两层都是 svg）；图上多个可点细节用 **点击弹窗**（多组热点）。这些交互都可以重复，也可以在同一篇里混用，见 [click-switch.md](references/components/click-switch.md)、[click-popup.md](references/components/click-popup.md)。没有理由就不要加交互。

图片槽位先按角色列出（场景、透明贴纸、若有则循环背景）。具体哪一张图等素材池返回后再定。

向用户展示大纲和 tag，要改就改完再往下。「直接开始 / 你定」可跳过本次等待。

### Step 3 · 配图

读 [references/assets.md](references/assets.md)。

- 默认用确认过的一个 tag 拉取该 tag 的全部已发布图，再按角色分到槽位，并用 `build_oss_src.py` 得到最终 CDN。库内图不重新上传，也不去背。
- 素材池为空时先停。用户可以改 tag、改交图片、改点名生图技能，或明确继续并接受占位图。不要自动换第二个 tag，也不要改去生图。
- 用户已经给了图：那些槽位按 [upload.md](references/upload.md) 上传。用户点名了生图技能：只按该技能出这些槽位的图，再上传。临时链不进 manifest 或 HTML。
- 某个槽位在池里没有对应类型时，该槽位使用占位图，并记入成品摘要。按钮、分割和简单几何写 SVG，不占位硬上。

画布用的图走 `<image href>`；图文 SVG 主图按画布占位像素，贴纸从透明装饰里选；轮播每张 slide 走 `<img src>`，同尺寸 cover。

### Step 4 · 写 HTML

**每轮必读** [references/dialect.md](references/dialect.md)。流式块读 [references/components/richtext.md](references/components/richtext.md)。有图文 SVG 再读 [image-svg.md](references/components/image-svg.md)。有轮播再读 [slideshow.md](references/components/slideshow.md)。有横向滑动再读 [horizontal-scroll.md](references/components/horizontal-scroll.md)。有切换再读 [click-switch.md](references/components/click-switch.md)。有弹窗再读 [click-popup.md](references/components/click-popup.md)。有普通辅助 `<svg>` 再读 [svg.md](references/components/svg.md) 与 [animation-group.md](references/components/animation-group.md)。

组件文档里若仍写「对照图生图 / 同场景图生图」，以本技能 [assets.md](references/assets.md) 为准，不要据此生图。

色、标题、分割、圆角只来自当前主题。禁止 HTML 注释。

文末保留弱化的 AI 声明：「文章部分内容由AI辅助设计和制作」。

写入 `{taskDir}/work.html`。

### Step 5 · 结构摘要 ⏸️

展示：主题、语法、节拍、所用 tag、素材来源与占位回退、若有图文 SVG 则 **几块、哪种构图、几张贴纸**、**几块辅助画布 / 几个动画组（autoplay 还是点击）**、若有轮播则 **几块、每块张数与 `data-effect`**、若有横向滑动则 **几块、前层还是后层、视口高与画布宽**、若有切换或弹窗则 **各几块**（弹窗写每块几组热点，并标明会员）。
**等用户确认后再发布**。用户说「直接发布」可跳过。

### Step 6 · 发布

```bash
python3 "$SKILL_DIR/scripts/publish.py" \
  --body-file {taskDir}/work.html \
  --title "月下团圆" \
  --description "可选说明"

python3 "$SKILL_DIR/scripts/publish.py" \
  --work-id <workId> \
  --body-file {taskDir}/work.html \
  --title "月下团圆"
```

接口见 [references/api-formats.md](references/api-formats.md)。

### Step 7 · 清理与完成

清临时 HTML（保留 taskDir，除非用户要删）。把脚本输出的 `preview`（立即预览，约 6 小时有效）和 `url`（编辑器）给用户。

## 注意事项

- **主题必须先确认**：未指定 theme 时，Step 1 先推荐再锁定，禁止静默随机开写。
- **默认不生图**。只有用户点名的生图技能可以出图。
- **不是 admin 接口**；403 更可能是未订阅。
- **402**：作品容量达上限。
- **404（修改）**：workId 错、非所有者、或已发布。
- **400**：对照 dialect：根 section、richText 非空、slideshow 张数与 height、clickSwitch 两层 svg、clickPopup 必须是 svg 且含组+底图、横向滑动的宽画布必须是横向 scroller 的唯一子节点且 `data-max-width="none"`、宽画布宽度 > 390 且 ≤ 1560、画布标签只在 svg 内、`<image>` 成对闭合、animationGroup 不能当 section 子节点、512KB / 300 元素。
- 素材接口失败时停止取图，不猜 key，不改拉全库。

## 参考资料

- [流式方言速查](references/dialect.md)（每轮必读）
- [richtext 组件](references/components/richtext.md)
- [图文 SVG](references/components/image-svg.md)
- [轮播](references/components/slideshow.md)
- [横向滑动展现](references/components/horizontal-scroll.md)
- [点击切换](references/components/click-switch.md)
- [点击弹窗](references/components/click-popup.md)
- [SVG 画布](references/components/svg.md)
- [动画组](references/components/animation-group.md)
- [文章结构](references/article-structure.md)
- [视觉配额](references/visual-system.md)
- [配图](references/assets.md)
- [图片上传](references/upload.md)：用户图片或点名生图需要入库时读取。素材库图片不读。
- [AI 素材接口](references/api-ai-assets.md)：取图脚本失败或要核对字段时读取
- [主题清单](themes/theme-index.md)
- [发布 API](references/api-formats.md)
- 示例：[纯流式](examples/chapter-flow.html)、[图文 SVG](examples/image-svg-beat.html)、[带辅助画布](examples/motion-beat.html)、[轮播图集](examples/slideshow-beat.html)、[横向滑动展现](examples/horizontal-scroll-beat.html)、[点击切换](examples/click-switch-beat.html)、[点击弹窗](examples/click-popup-beat.html)

## 来源与支持

这是技能本身的支持信息，不是作品内容。不要把二维码、logo 或本仓库地址写进作品 HTML 或素材清单。

- 开源仓库：<https://github.com/21epub/weipaiban-article-skill>
- 微信交流群二维码见 [README.md](README.md) 的「交流群」。用户问如何加群或找支持时，把这一节指给用户。
