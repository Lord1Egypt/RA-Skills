---
name: xiaohongshu-note
description: Generate Xiaohongshu (Little Red Book) style image notes. Use when the user wants to create vertical 3:4 image posts for Xiaohongshu — knowledge cards, infographic-style notes, 干货图文, or multi-image posts with matching caption text. Produces: a set of 3:4 high-res PNG images (1080×1440 @2x) + a ready-to-post caption (title / body / hashtags). Trigger words: 小红书, xiaohongshu, 图文笔记, 干货图文, 种草图文, 知识卡片, 图文卡片. NOT for: PPT decks, course materials, or 讲师版 slides — those are separate workflows.
---

# Xiaohongshu 图文笔记生成

把任意知识内容做成**小红书风格的 3:4 竖版图文笔记**（一套可直接发布的精美图片 + 配套发布文案）。

## 输出物
1. `export/图01.png … 图NN.png` — 3:4 竖版高清图（1080×1440，2x = 2160×2880），一张一张可直接上传小红书
2. 小红书发布文案（标题 2-3 个备选 + 正文 + 话题标签）

## 核心原则（重要，先读）
小红书图文 ≠ 课件/PPT。必须遵守：

- **去掉所有机构感字样**：不出现「课程」「讲师」「学员」「品牌名」「xxx学习」「xxx课」等。用户可能只是知识博主，不是卖课机构。
- **定位是「干货分享」**：像私人知识博主发的笔记，单张即可传播、可被收藏。
- **封面抓眼球**：大字扎心金句（如「你缺的不是时间，是精力」）+ 强对比/高颜值背景，让人想点进来。
- **一页一个知识点**：短句、少字、有条理，方便截图收藏。不要把一页塞满。
- **结尾有钩子**：收藏/点赞引导 + 行动号召（如「建议收藏」「从今晚睡个好觉开始」）。

## 视觉风格（随机多套 + 可指定）
风格不是固定一种，而是**内置 7 套主题，每次渲染默认随机抽取**（同一内容可发多篇不同配色的笔记，避免审美疲劳/限流，也可测试哪种风格数据好）。

预设主题（见 `scripts/themes.js`）：
- `cream` 奶油系（默认风） · `matcha` 抹茶清新 · `peach` 蜜桃少女 · `mono` 极简黑白
- `caramel` 焦糖暖棕 · `mistyblue` 雾霾蓝 · `lilac` 紫调梦幻

选择方式：
```bash
node render.js            # 随机一套
node render.js matcha     # 指定风格（可用名见上）
node render.js list       # 列出所有风格
```
配色通过 CSS 变量注入（模板 `assets/template/slides.html` 内有 `<!-- THEME -->` 占位符，render.js 自动替换）。若用户指定风格或想新增一套，改 `scripts/themes.js` 即可。

元素通用：圆角卡片、可爱 emoji 图标、点状/圆形装饰。若用户要完全自定义风格，直接改 CSS。

## 工作流

### 1. 确认需求（如不确定先问，别猜）
- 内容主题 / 素材来源（是否有读书笔记、文章、大纲）
- 想拆成几张图（默认 6-9 张：封面 + 若干知识点 + 结尾）
- 视觉风格（默认奶油系；可换）
- 是否有具体的爆款金句/标题偏好

### 2. 组织内容（把素材拆成「一页一个知识点」）
参考 `assets/template/slides.html` 的已有结构。常见笔记结构：
- **封面**：大字金句 + 「建议收藏」钩子
- **2-6 张知识点**：每张图一个核心点（可用步骤条 / 卡片列表 / 表格 / 引言）
- **结尾**：行动号召 + 收藏引导

### 3. 写 HTML
把 `assets/template/slides.html` 复制到工作目录（如项目下的 `xiaohongshu/`），按主题改写内容：
- 复用现成的 CSS 类（`.cover` `.card` `.step` `.quote` `table` `.end`），保证风格统一、无需重写样式
- 每个 `.slide` 是一张图；页码手动标在 `.foot .page`（如 `2/8`）
- 保持一页一屏，内容不要溢出 1440 高度（可用浏览器预览检查）

### 4. 渲染成图
把 `scripts/render.js` **和 `scripts/themes.js` 一起**复制到 HTML 同目录（两个文件缺一不可，渲染需要主题库），运行：
```bash
node render.js            # 随机风格
node render.js <theme>    # 指定风格
```
产出 `export/图01.png …`。脚本用 playwright + chromium 渲染，1080×1440 @2x。

> 也可不复制，直接在 skill 目录运行 `node scripts/render.js`（会自动在 `../assets/template/` 找 slides.html）——但产出会写到 skill 的 assets/template/export，交付前注意文件位置。

### 5. 写发布文案
参考 `references/copywriting.md` 的语气与结构，产出：
- **标题**：2-3 个备选（扎心/悬念/痛点型）
- **正文**：短段落 + emoji + 分点，口语化、有共鸣
- **话题标签**：8-12 个，嵌套热门+垂类标签

### 6. 交付
- 图可直接发群/交付（可用 message 工具逐张发送）
- 文案以可复制文本交付

## 环境依赖
- Node.js + playwright + chromium（脚本需要）
- 无需 python-pptx（小红书图文不合成 PPT）

## 提示
- 图片渲染后**务必目检**（或让用户看）是否有溢出/错位，再交付。
- 若用户后续要把同一内容做成 PPT/课程（讲师版/知识点版），那是另一套流程，不要混用本 skill。
