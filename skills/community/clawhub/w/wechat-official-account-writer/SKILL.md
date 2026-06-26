---
name: wechat-official-account-writer
description: "微信公众号写作发布助手 / WeChat Official Account Writer. 用于写公众号文章、微信公众号推文、技术长文、AI 热点解读、个人观点文、产品文章、教程文章和商业内容；支持选题策划、爆款标题、文章大纲、正文成稿、润色改写、链接翻译/链接改写、AI 资讯整理、Markdown/微信 HTML 排版、image2/imagegen 生成封面图、正文贴图/插图、技术架构图/流程图配图、底部关注引导、发布前检查、生成上传 JSON，并通过内置 wechat-article-workbench 上传到微信公众号平台草稿箱。English triggers: WeChat Official Account article writing, translation/rewrite, AI news rewriting, image generation, WeChat HTML, draft-box upload."
---

# 微信公众号写作发布助手 / WeChat Official Account Writer

## 概览 / Overview

这个 skill 用于把一个主题、一段素材、一个链接或一组 AI 热点整理成可发布的微信公众号草稿，并在需要时生成封面图、正文插图、微信安全 HTML、上传 JSON，最后通过内置 `wechat-article-workbench` 创建微信公众号草稿箱条目。

English summary: use this skill for end-to-end WeChat Official Account writing, link translation/rewrite, AI-news rewriting, image generation, validation, and draft-box upload.

## 能完成什么 / Capabilities

- 从一句话主题生成公众号标题、大纲、正文和结尾。
- 把英文/中文链接翻译、消化、重组为原创中文公众号文章。
- 把 AI 新闻、AI HOT 条目、产品发布、技术资料改写成适合公众号阅读的内容。
- 为技术文章规划或生成架构图、流程图、系统图、产品场景图等正文插图。
- 使用 image2/imagegen 生成封面图、文章内贴图和正文插图，而不是静态 SVG 模板。
- 在正文适当位置插入有信息增量的图片，并在底部加入自然的关注引导。
- 输出微信安全 HTML 和上传 JSON，并调用内置上传器创建草稿箱条目。
- 做发布前检查，识别标题夸张、事实缺口、敏感表述、排版问题和读者理解断点。

## 工作原则 / Principles

- 默认使用中文，除非用户明确要求其他语言。
- 产出可发布的公众号草稿，不写泛泛的普通作文。
- 优先保证读者承诺清晰、开头有抓力、结构适合扫读、例子具体、结论克制、配图有信息价值。
- 保留用户提供的事实、名称、产品细节、引用和约束。
- 不编造数据、背书、客户案例、政策结论、来源链接或竞品结论。
- 文章正文避免过度营销感；底部关注引导要像自然编辑署名，不要像广告横幅。

## 工作流程 / Workflow

1. 先判断任务类型：
   - 原创写作：把主题或粗略想法扩展成标题、大纲和正文。
   - 素材改写：把笔记、报告、转录稿、网页或要点改写成文章。
   - 链接翻译/改写：提炼来源观点，翻译必要部分，再重组为带有分析的原创中文文章。
   - 润色：提升现有草稿的清晰度、节奏、标题强度和微信可读性。
   - 配图：规划或生成封面图和正文图片。
   - 上传准备：生成 `wechat-article-workbench` 需要的 JSON，并在需要时运行校验和草稿命令。
   - 审稿：发现逻辑薄弱、风险表述、证据不足、语气问题和发布阻力。

2. 只在关键信息缺失时最多问两个问题。优先确认目标读者、文章角度、篇幅、品牌/人设语气、必须使用的事实或素材。如果用户希望快速推进，或上下文已经足够，就做合理假设并简短说明。

3. 写作前先定型：
   - 用一句话定义读者承诺。
   - 选择一个主角度，不堆砌多个松散观点。
   - 需要标题创意时，给出 8-12 个标题选项。
   - 建立分节大纲，每节回答一个读者问题。

4. 撰写草稿：
   - 用具体场景、对比、近期变化或直接痛点开头。
   - 避免“在当今时代”“随着互联网的发展”这类空泛开场。
   - 使用短段落、清晰小标题和具体例子。
   - 根据内容价值决定正文图片数量，可以是 0、1 或多张，不为了套模板强行配图。
   - 正文图片应承担解释、情绪锚点或分享价值，不做纯装饰。
   - 除非用户明确要求，正文 HTML 避免卡片盒、边框总结框、大色块 callout 和厚重圆角容器；优先使用普通标题、段落、简单序号和留白。
   - 结论力度要和证据匹配。
   - 根据文章类型，用明确 takeaway、问题、清单或行动收尾。
   - 发布态公众号文章默认加入克制自然的底部关注引导，除非用户要求不要。

5. 打包发布材料：
   - 给出最终推荐标题。
   - 必要时给出 3-5 个备选标题。
   - 必要时给出一句话摘要。
   - 默认输出 Markdown 正文；如果用户要求上传准备或草稿箱上传，则输出微信安全 HTML JSON。
   - 草稿箱上传时，按 `scripts/wechat-article-workbench` 的格式写 JSON。
   - 草稿箱上传默认先生成封面图，并把图片保存到本地项目后再创建草稿。
   - 正文图片只在确实提升理解或传播时使用 image2/imagegen；在 `contentHtml` 插入占位符，写入 `inlineImages`，并保存到 `data/images/`。
   - 只有做审稿、涉及事实风险、敏感主张或商业说服时，才加入“发布前检查”。

## 图片生成 / Image Generation

草稿箱上传时，默认先生成模型封面图。使用 `imagegen` skill/tool，并让它走可用的 image2/imagegen 路径。项目内图片保存到内置上传器的 `data/images/` 目录，并在文章 JSON 中引用。

默认素材要求：

- 封面图：一张横向编辑风格图片，基于文章标题、核心论点和情绪/技术主题生成。除非用户明确要求，不要在图里放标题文字，因为图片文字容易渲染不好。
- 正文图/贴图：当图片能帮助理解、提升扫读或增强分享价值时再生成。技术文章优先架构图、流程图、系统图、产品场景、时间线或概念图；非技术文章优先编辑插画、象征场景或能深化观点的氛围图。
- 不要默认使用本地 SVG/模板封面生成器。

创建图片或准备草稿箱上传前，读取 `references/image-and-draft-upload.md`。

## 内置上传器 / Bundled Uploader

内置 Node.js 上传器路径为 `scripts/wechat-article-workbench`。当用户需要真实创建微信公众号草稿箱条目时使用它。

首次安装配置：

1. 在 `scripts/wechat-article-workbench` 中运行 `npm install`。
2. 复制 `config.example.env` 为 `.env`。
3. 填写 `WECHAT_APPID`、`WECHAT_APPSECRET` 和较短的 `WECHAT_AUTHOR`。
4. 第一次校验保持 `DRY_RUN=1`，确认无误后设置 `DRY_RUN=0` 创建真实草稿。

如果缺少凭据，或微信 API/IP 白名单尚未配置好，仍然先产出文章 JSON 和图片文件，然后告诉用户还缺什么设置。

## 参考资料加载 / Reference Loading

只加载当前任务需要的参考文件：

- 写结构、开头、结尾和标题公式时，读取 `references/article-patterns.md`。
- 润色、审稿或最终发布检查时，读取 `references/output-checklist.md`。
- 生成图片、创建微信 HTML JSON、使用内置上传器或把链接/手动选题转成草稿箱条目时，读取 `references/image-and-draft-upload.md`。

## 质量标准 / Quality Bar

最终交付前确认：

- 标题和正文匹配，不夸大承诺。
- 前 200 个中文字符能让读者知道为什么要继续读。
- 每个小节都推进同一个中心承诺。
- 具体例子多于抽象形容词。
- 数据、排名、政策、医疗、法律、金融和竞品判断，要么来自用户提供的材料，要么明确标注为假设。
- Markdown 干净，不包含内部推理笔记。
- 上传前，文章 JSON 必须通过本地 schema 校验。
- 除非用户明确启用静态兜底，否则没有真实 `coverImagePath` 时不得创建草稿。
