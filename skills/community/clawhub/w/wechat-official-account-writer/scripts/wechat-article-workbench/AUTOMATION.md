# Codex 自动化提示词

在 `/Users/yumingzhi/Documents/Codex/wechat-article-workbench` 中运行微信公众号文章工作台流水线。

重要规则：

- 不要直接发布文章，只创建微信公众号草稿箱条目。
- 不要调用 OpenAI API，也不要要求 `OPENAI_API_KEY`。
- 使用 Codex 自身模型能力完成写作、改写、翻译、总结和文章 JSON 打包。
- 不要在文章正文里出现可见的 `来源：`、`原文链接：`、`参考链接` 或 `个人观点 仅供参考` 字样。
- 不要在生成的文章 JSON 中设置 `author`，草稿脚本会从 `.env` 的 `WECHAT_AUTHOR` 读取。
- 不要设置 `content_source_url`，避免微信公众号后台展示原文链接字段。
- 官方草稿 API 不开放后台的「创作来源」选择器。每次创建草稿后，都要提示用户发布前需要在微信公众号后台手动把「创作来源」设置为 `个人观点，仅供参考`。
- 跳过已经标记为 drafted 的条目。
- 保持内容原创：总结、解释和评论，不要长篇复制来源文本。
- 对中文来源文章，要用明显原创的结构重新组织和改写，不要按原段落顺序逐段改写。
- 对翻译链接，只翻译服务于中文文章所需的部分，并加入上下文和分析，不要生成全文直译。
- 在适合时加入当前大模型、Agent、AI 原生硬件或 AGI 时代背景下的判断，不要只做摘要。
- 封面必须基于标题和正文内容用 image2/imagegen 生成，保存到 `data/images/`，并通过 `coverImagePath` 引用。
- 不要依赖 SVG/模板封面、纯色背景或几个字的渐变图。
- 正文插图在有价值时也应使用 image2/imagegen 生成。技术文章优先使用架构图、流程图、系统图、产品场景、时间线或概念图；非技术文章优先使用能增加意义的编辑插画或象征性场景图。
- 当格式、配图质量或文章排版需要时，可以使用合适的脚本、skill 或 MCP 能力。
- 原创写作使用或创建 `npm run source -- --mode=original` 手动素材。
- 链接翻译或链接改写使用 `npm run source -- --url="..." --mode=translate` 或 `--mode=rewrite`。
- AIHOT 只作为来源适配器。除非文章明确讨论 AIHOT，否则不要在可见正文中提到 AIHOT。
- 所有生成图片保存到 `data/images/`，封面设置 `coverImagePath`，正文图片使用 `inlineImages` 占位符。

步骤：

1. 确认依赖已安装：

   ```bash
   npm install
   ```

2. 收集或添加素材：

   AIHOT 精选选题：

   ```bash
   npm run collect:aihot -- --limit=3
   ```

   自定义链接：

   ```bash
   npm run source -- --url="https://example.com/article" --mode=translate
   ```

   原创/手动选题：

   ```bash
   npm run source -- --title="选题" --mode=original --text="写作要求或素材"
   ```

3. 读取 `data/pending.json`。对每个待处理条目，读取 `data/sources/<sourceId>.json`。

4. 为每个素材写入 `data/generated/<sourceId>.json`：

   ```json
   {
     "sourceId": "与输入素材一致的 sourceId",
     "title": "微信公众号标题，建议28字以内",
     "digest": "80-120字以内摘要",
     "coverTitle": "封面主标题，尽量短",
     "coverSubtitle": "封面副标题，概括文章价值",
     "coverKeywords": ["关键词1", "关键词2", "关键词3"],
     "coverImagePath": "必填，本地PNG/JPG封面路径，必须由 image2/imagegen 基于标题和正文生成，例如 data/images/sourceId-cover.png",
     "inlineImages": [
       {
         "placeholder": "{{inline_image:workflow}}",
         "path": "本地PNG/JPG正文插图路径，由 image2/imagegen 生成，例如 data/images/sourceId-workflow.png",
         "alt": "图片替代文本",
         "caption": "可选图片说明"
       }
     ],
     "contentHtml": "<section>微信公众号正文HTML</section>"
   }
   ```

   正文要求：

   - 中文公众号文章风格，适合微信阅读。
   - 使用干净 HTML，包含必要的行距、段落节奏、分节标题、引用或提示样式。
   - 开头用短导语进入主题，再用清晰小节展开。
   - 包含 3-5 个关键点，用 HTML 段落或样式块表达，不要使用 Markdown。
   - 包含一段简短的分析或判断。
   - 结尾使用简洁提示、收束或观点，不要写来源归因或参考链接列表。
   - 不要使用外部 `<img>` 标签。正文图片应先在 `contentHtml` 中放占位符，再通过 `inlineImages` 映射。
   - 避免直接长篇复制来源内容。
   - 不要在可见正文里提内部来源标签。
   - 在 `coverImagePath` 指向真实存在的本地模型生成 PNG/JPG 前，不要创建草稿。

5. 校验生成文件：

   ```bash
   npm run validate -- --all
   ```

6. 创建微信公众号草稿：

   ```bash
   npm run draft -- --all
   ```

   草稿脚本会为每篇文章上传对应封面图，并在配置了正文图时上传正文图片。

7. 汇报：

   - 素材总数
   - 待处理数
   - 已生成数
   - 已创建草稿数
   - 跳过数
   - 失败条目 ID 和错误信息
