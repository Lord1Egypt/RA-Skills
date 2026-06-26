---
name: wechat-article-formatter
description: 生成、规范化、主题化和预览 HTML 优先的微信公众号文章，让正文可复制到微信后台。适用于把主题、简报、笔记、提纲、Markdown 或已有 HTML 转成微信友好的文章正文，创建本地预览页，应用可复用排版主题，或准备可复制的 `article#wechatArticle`。
---

# 微信文章排版预览

## 用途

为微信公众号编辑流程生成并规范化 HTML 优先的文章内容。
输出应聚焦文章正文，方便复制到微信后台。
允许使用可选主题预设，让文章在排版时匹配指定的微信文章视觉风格。
被 `wechat-article-pipeline` 调用时，直接生成第一版 HTML 主稿，并以 `wechat-article-writer` 的写作质量标准作为参考；后续修订都以这份经过审核的 HTML 为唯一正文主稿。

## 执行清单

开始后用这张清单跟踪进度：

- [ ] 判断来源类型：主题或简报、笔记、提纲、Markdown、已有 HTML。
- [ ] 选择交付模式：默认本地预览页；正文片段或后台复制场景使用 `article#wechatArticle`。
- [ ] 生成或规范化 HTML 草稿，同时保留来源事实和原有表达。
- [ ] 应用用户指定的主题预设；未指定时使用 `warm-editorial`。
- [ ] 执行样式审核，并直接修复 HTML 问题。
- [ ] 对于含有本地图片资源的排版，运行 [inline_images.py](scripts/inline_images.py) 将相对路径图片内联为 base64 Data URL。
- [ ] 若需要将封面图转为 Base64 Data URL 形式，运行 [convert_cover_to_base64.py](scripts/convert_cover_to_base64.py)。
- [ ] 需要完整预览页时，用 [generate_preview.py](scripts/generate_preview.py) 生成预览，可选择使用 `--open` 参数或 [open_preview.py](scripts/open_preview.py) 交互式地提醒用户并在用户同意后通过浏览器打开 HTML 预览。
- [ ] 按 `references/completeness-checklist.md` 检查最终结果。

## 默认策略

- 默认把 HTML 作为唯一正文主稿格式。
- 普通起草、排版和预览请求默认生成本地完整 HTML 预览页。
- 只有后台复制、API 交接或明确要求正文片段时，才默认交付 `article#wechatArticle`。
- 没有可用主题预设时，默认使用 `warm-editorial`。
- 默认把主标题放在可复制正文外，除非用户要求正文内包含标题。
- 默认把生成的预览文件放在 `dist/`。

## 工作流程

1. 判断来源类型：主题或简报、笔记、提纲、Markdown、已有 HTML。
2. 来源是主题、简报或笔记时，直接生成第一版微信公众号 HTML 草稿。
3. 来源是已经审核过的语义化 HTML 时，把它作为正文主稿，只规范化结构问题。
4. 只有来源是 Markdown 或纯文本，且没有语义化 HTML 草稿时，才转换为 HTML。
5. 把文章整理成微信友好的 HTML 正文结构，保留事实和用户给出的措辞，并使用合适的 `data-role` 属性。
6. 生成最终预览前执行样式审核。
7. 用户指定主题时应用对应主题预设；未指定时使用默认暖色编辑主题。
8. 选择交付模式：
   - 任务涉及后台复制、下游交接、API 交接或只要正文片段时，返回或写入可复制结果，正文主体包在 `article#wechatArticle` 中。
   - 任务未涉及发布或交接时，默认写入本地完整 HTML 预览页。
9. 对于包含本地图片资源的文章，在组装生成预览前，必须运行 [inline_images.py](scripts/inline_images.py) 脚本（如 `python skills/wechat-article-formatter/scripts/inline_images.py --html dist/temp_content.html`）将相对路径图片一键内联为 Base64 Data URL。若有封面图片，可运行 [convert_cover_to_base64.py](scripts/convert_cover_to_base64.py) 进行 Base64 转换。
10. 写完整 HTML 预览页时，按照 [preview-implementation.md](references/preview-implementation.md) 的要求，用 [generate_preview.py](scripts/generate_preview.py) 组装输出，并在完成后提醒并可用浏览器打开预览（例如使用 `--open` 参数或独立脚本 [open_preview.py](scripts/open_preview.py)）。
11. 最终交付前，严格按 `references/completeness-checklist.md` 检查结果。

## 来源规则

- 优先使用 HTML 作为工作格式。
- 必要时接受 Markdown、提纲文本或笔记作为上游输入。
- 用户要求从零生成微信公众号文章时，可以接受主题或简报作为上游输入，并直接用 HTML 写作和组织正文。
- 输入是语义化 HTML 草稿时，不要转回 Markdown；后续内容和结构修复都直接在 HTML 中完成。
- 输入是 Markdown 时，先转换成文章 HTML，再把这份 HTML 作为工作草稿。
- 用户已经提供 HTML 时，不要要求用户再提供 Markdown。
- 保留来源语种。中文来源的标题、标签和正文都应保持中文。
- 不要重复包裹 `article#wechatArticle`。使用 [generate_preview.py](scripts/generate_preview.py) 时，只传入文章内部内容，因为预览模板会提供外层容器。

## 样式审核

生成最终预览或可复制正文前，先审核 HTML 草稿：

- 正文是干净的语义化 HTML，没有预览工具栏、脚本、外部 CSS、调试文字或重复的 `article#wechatArticle` 包裹。
- 可复制正文通常不包含 `h1`；文章标题用于预览页标题和最终回复说明。除非用户明确要求保留、来源本身必须保留，或交付物就是带读者可见标题的独立正文，否则删除正文层面的重复 `h1` 或大型标题。
- 文章有清晰章节顺序时，主要 H2 上方使用短 `moduleLabel` 序号标签。
- 可调整措辞时，主要 H2 使用自然中文的两段式编辑标题。
- 段落适合移动端阅读，不产生连续大段文本。
- `quote`、`callout`、`summary`、列表、图片和图片说明只在支持内容时使用。
- 不留下未闭合标签、不安全嵌套、过长未换行 URL 或容易造成横向滚动的结构。

样式审核发现问题时，先直接修复 HTML 草稿，再运行预览生成器。若修复会改变事实含义或文章立场，先回到写作或修订步骤。

## 首稿生成

根据主题、简报、提纲或笔记生成第一版文章时：

- 直接产出面向微信的 HTML 首稿，不先写 Markdown。
- 内容取舍、篇幅、信息密度和中文表达以 `wechat-article-writer` 定义的写作标准为准；本技能只负责把已确定的内容组织成微信友好的 HTML。
- 以 `wechat-article-writer` 作为写作质量参考，覆盖目标读者、文章承诺、标题策略、结构、中文节奏、具体细节、作者判断、精简约束和反模板化语气。
- 先让文章读起来自然，再用 HTML 结构支撑节奏，不为满足固定标签清单牺牲阅读。
- 默认把主标题放在 `article#wechatArticle` 外：作为 `--title` 传给预览生成器，并在最终交付说明中提及。除非用户明确要求复制正文内包含标题，否则可复制正文从导语、摘要或第一个 `h2` 开始。
- 只有在提升扫描效率或澄清论证时，才使用 `moduleLabel`、两段式 H2、引用、提示块、摘要和列表。
- 来源备注、事实不确定处、链接、配图建议和发布提醒应作为内部复核或最终交付说明记录。除非用户明确要求、来源已有，或文章本身需要向读者展示引用，不要在 `article#wechatArticle` 中添加读者可见的“来源”“参考资料”“引用和备注”或发布提醒章节。
- 第一版 HTML 草稿生成后，所有内容和样式修订都直接在这份 HTML 草稿中完成。

## 主题预设

- 用户需要特定文章配色时，支持可选的 `themePreset` 输入。
- 使用 `references/theme-presets.md` 中定义的预设 id、展示名、固定颜色标记、固定排版标记和视觉方向。
- 没有有效预设时，兜底使用 `warm-editorial`。
- 支持的预设 id：
  - `warm-editorial`
  - `light-simple`
  - `tech-blue`
  - `indigo-card`
  - `swiss-grid`
  - `purple-highlight`
  - `warm-nature`
  - `vitality-orange`
  - `wechat-pure-glass`
  - `modern-cobalt`
  - `deep-space`
- 用户提到“科技蓝”“自然森系”等主题名时，映射到对应预设 id。
- 未指定预设时，保持内容优先，并以 `warm-editorial` 作为本地兜底预设。
- 完整预览页必须在主题切换器中暴露所有支持的预设；除非用户指定其他主题，否则初始化为 `warm-editorial`。
- 预览外壳可以用 JavaScript 切换主题，但复制出去的正文必须把所选主题写成 `article#wechatArticle` 内的行内样式。
- 主题颜色由 `references/theme-presets.md` 固定。不要根据预设名臆造新的主色、正文色、表面色、边框色、引用色、代码色或表格色。
- 需要的组件未被语义标记表覆盖时，先从同一预设的完整色板中选择，再考虑新增颜色。
- 主题排版由 `references/theme-presets.md` 固定。不要根据预设名臆造新的基础字号、标题字号、列表字号、引用字号、代码字号、表格字号、说明字号或备注字号。
- 主题未列出专用尺寸时，使用 `references/theme-presets.md` 中的通用排版标记。

## 纯样式边界

- 应用样式时，不强行套用固定文章架构。只处理来源中已有的元素，或来源转换后自然产生的元素。
- 不要添加编号章节、作者块、结尾块、推荐模块或特定媒体模板，除非来源已有等价内容。
- 从草稿、提纲或新写文章生成正文时，默认在主要 H2 上方使用紧凑的 `moduleLabel`，例如 `01 / 开头`、`02 / 关键判断`、`06 / 最后一句话`。标签要短、贴合来源，并放在 H2 文本外。
- 来源允许编辑塑形时，主要章节优先使用两段式 H2：前半段说明主题或场景，后半段给出具体判断或收益。能写得更清楚时，避免只写 `背景`、`分析`、`总结` 这类空泛标题。
- 任务是严格排版既有终稿时，不要为了制造两段式标题而改写 H2；只有现有章节顺序明确或用户要求这种编辑风格时，才添加 `moduleLabel`。
- 默认输出应通过字体、间距、克制的表面层和语义强调形成温暖编辑感，不通过编造内容实现风格。

## 输出约定

- HTML 输出目录：生成的本地预览 HTML 默认写入 `dist/`。这与仓库 `.gitignore` 匹配，也能避免生成预览进入版本控制。
- 只有用户明确指定其他目录时，才使用其他输出目录。
- 除非用户明确要求只输出文章正文，或任务属于交接流程，否则默认生成本地完整 HTML 预览页。
- 普通写作、排版或起草任务以预览页作为交付物。最终回复提供本地文件路径，不粘贴完整 HTML 源码。
- 主体文章正文包裹为：

```html
<article id="wechatArticle">...</article>
```

- 结果聚焦文章正文。最终正文中不要包含测试页外壳、应用导航、调试面板或无关控件。
- 内容必须自包含。文章可读性不要依赖外部 CSS、外部 JavaScript、外部字体、旁路 JSON 文件或运行时渲染。
- 不要依赖 JavaScript 在运行时生成最终文字或图片 URL。
- 用户要求完整预览页时，也要隔离可复制目标，确保实际文章正文仍可干净抽取。

## 交付规则

- 请求不涉及后台复制、API 交接或其他下游交接步骤时，默认写入本地完整 HTML 预览页。
- 完整预览交付必须是单个可转移的 `.html` 文件。不要留下主题 JSON 或样式 JSON 作为用户发送、打开或发布时必须携带的配套文件。
- 只有用户明确要求只输出文章正文，或任务明显属于后台复制/交接流程时，才返回原始 `article#wechatArticle` HTML。
- 写完整预览 HTML 文件时，默认使用 [generate_preview.py](scripts/generate_preview.py)，继承其主题切换和复制到微信控件；**必须**在生成完成后使用 `--open` 参数或调用 [open_preview.py](scripts/open_preview.py) 强制交互式提醒用户是否在浏览器中打开预览。用户明确要求只要正文时除外。
- 用户要求 Markdown 加微信可复制结果时，Markdown 只作为可选中间阅读稿，最终交付目标仍是 HTML 正文。
- 在 HTML 优先的文章流程中，不维护 Markdown 和 HTML 两份主稿。以经过审核的语义化 HTML 作为主编辑物。

## 常见误用

- 不要把已审核 HTML 转回 Markdown 再编辑。
- 不要把完整预览页外壳当作可复制正文；正文交接只交 `article#wechatArticle`。
- 使用 [generate_preview.py](scripts/generate_preview.py) 时，不要重复生成 `article#wechatArticle` 包裹。
- 不要根据主题名臆造新的主题颜色或排版尺寸。
- 除非用户或来源要求，不要新增读者可见的来源、审核或发布风险章节。
- 不要让最终文章依赖外部 CSS、JavaScript、字体或旁路文件。
- 生成本地 HTML 预览页后，在未提醒或未尝试用浏览器打开的情况下就直接交付或关闭任务。
- **不要在排版首稿或正文中使用 `div` 标签进行排版装饰或作为文字容器（例如 `moduleLabel` 或提示卡片）**。微信后台粘贴富文本时会过滤或打碎 `div` 标签的行内样式。应使用 `<section>` 作为外层容器（如提示区、摘要卡），使用 `<p>` 标签作为文本或小标题容器。
- **不要在正文 HTML 中使用相对路径来引用本地图片（如 `./image.png`）**。因为本地 `file://` 协议下浏览器的 CORS 跨域策略会阻止在复制时的 Base64 转换与拉取，导致在微信中图片失效。所有的本地图片资源必须在首稿起草或排版前，直接进行 Base64 Data URL 内联编译。


## 验证闭环

最终交付前：

1. 确认交付模式符合用户请求。
2. 交付正文时，确认文章正文只有一个干净的 `article#wechatArticle` 包裹。
3. 交付预览页时，确认预览页可以干净抽取并复制文章正文。
4. 确认主题颜色和排版来自 `references/theme-presets.md`。
5. 确认已经检查 `references/completeness-checklist.md`。
6. **[强制要求]** 确认已通过 [open_preview.py](scripts/open_preview.py) 或 `--open` 参数提醒用户是否打开浏览器，并在用户同意后成功打开了 HTML 预览页面。

## 示例请求

- “把这篇 Markdown 转成可以复制到微信公众号后台的正文”
- “把这段 HTML 调整成微信公众号正文结构”
- “生成可以复制到微信后台的文章 HTML”
- “把这个提纲扩展成公众号排版，并输出 `article#wechatArticle`”
- “用 `tech-blue` 主题把这篇 Markdown 排成微信公众号正文”
- “按自然森系配色输出公众号正文 HTML”

## 参考资料

为保持主说明聚焦，具体技术细节和约束放在参考文件中。执行相关步骤时，必须按需读取这些参考：

- **[主题预设](references/theme-presets.md)**：本地预设目录、颜色/排版标记和兜底行为。
- **[视觉与排版规范](references/visual-guidelines.md)**：编辑化样式、避免大色块、保持稳定 HTML 结构的规则。
- **[预览页实现](references/preview-implementation.md)**：生成预览页的技术要求，包括工具栏、剪贴板复制和图片 base64 内联。
- **[图片规则](references/image-rules.md)**：静态图片来源和 base64 转换策略。
- **[完整性清单](references/completeness-checklist.md)**：交付最终 HTML 前必须验证的 QA 清单。
- **[输出约定](references/output-contract.md)**：微信正文结构和交接约束。
