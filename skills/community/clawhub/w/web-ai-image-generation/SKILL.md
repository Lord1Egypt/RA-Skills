# Web AI 生图

当用户需要通过 Gemini、ChatGPT 等网页端 AI 服务生成图片时，使用这个 skill。

## 能力说明

这个 skill 通过浏览器自动化打开真实的 Gemini / ChatGPT 网页，复用浏览器 profile 中的登录态，提交生图提示词，等待图片生成，并把图片保存到本地目录。

适合以下场景：

- 不直接调用 Gemini / OpenAI 图片 API，而是复用网页端账号能力。
- 自动生成 AI 封面图、营销图、短视频封面或其他提示词图片。
- 需要复用网页登录状态，减少重复登录。
- 需要处理 `blob:` 图片、Google 托管图片或 ChatGPT `estuary/content` 图片下载。

## 文件结构

```text
web-ai-image-generation/
├── SKILL.md
├── DEPENDENCIES.md
├── requirements.txt
└── scripts/
    └── ai_image_playwright.py
```

说明：

- `scripts/ai_image_playwright.py`：命令行脚本，包含 Gemini / ChatGPT 生图、等待、下载逻辑。
- `requirements.txt`：Python 包依赖。
- `DEPENDENCIES.md`：Python、Playwright、浏览器和系统环境安装说明。

## 默认目录

默认输出到当前 skill 目录下的运行时目录。默认 profile 和输出目录为：

```text
skills/web-ai-image-generation/.runtime/profile
skills/web-ai-image-generation/.runtime/output
```

## 重要说明

浏览器通过 Playwright 的 `launch_persistent_context()` 启动 persistent context，并复用指定用户数据目录中的登录态。

首次使用全新 profile 时，需要在弹出的浏览器里手动登录 Gemini 和/或 ChatGPT。后续运行会自动复用该 profile 中保存的登录状态。

## 安装依赖

详见 `DEPENDENCIES.md`。

快速安装：

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

## 命令行用法

### Gemini 生图

```bash
python scripts/ai_image_playwright.py \
  --platform gemini \
  --prompt "一张竖屏 3:4 的短视频封面，主题是 AI 自动剪辑" \
  --output-dir ./output
```

### ChatGPT 生图

```bash
python scripts/ai_image_playwright.py \
  --platform chatgpt \
  --prompt "一张电影海报风格的 AI 短视频封面" \
  --output-dir ./output
```

### 使用内置封面提示词构造

如果不传 `--prompt`，可以传 `--title` 和 `--description`，脚本会自动构造短视频封面提示词：

```bash
python scripts/ai_image_playwright.py \
  --platform gemini \
  --title "AI 自动剪辑教程" \
  --description "如何用 AI 自动生成短视频" \
  --output-dir ./output
```

### 指定独立登录态目录

```bash
python scripts/ai_image_playwright.py \
  --platform chatgpt \
  --prompt "一张科技感产品海报" \
  --profile-dir ~/.ai-image-playwright/chatgpt-profile \
  --output-dir ./output
```

## 工作流概览

### 1. 启动浏览器

- 使用 `playwright.async_api.async_playwright()`。
- 通过 `launch_persistent_context()` 启动 Chromium persistent context。
- 当前实现使用 `headless=False`，需要桌面环境。
- 默认优先尝试 `/usr/bin/google-chrome`，不存在则回退到 Playwright Chromium。
- 启动后根据平台打开 Gemini 或 ChatGPT。
- 如果跳转到登录页，会等待用户在浏览器中手动登录。

### 2. Gemini 生图流程

- 打开 `https://gemini.google.com/app`。
- 尝试点击生图入口，支持 `制作图片`、`生成图片`、`Create image`、`Generate image` 等文本。
- 将提示词输入到 Gemini 的富文本输入框。
- 点击发送按钮或按 `Enter`。
- 轮询页面中的大尺寸图片，判断图片是否生成完成。
- 下载图片时优先处理：
  - `blob:` 图片：通过页面内 Canvas 提取。
  - `googleusercontent.com` / `gstatic.com` 图片：通过 Playwright request 下载。

### 3. ChatGPT 生图流程

- 打开 `https://chatgpt.com/`。
- 尝试点击生图入口，支持 `生成图片`、`Create image`、`Generate image` 等文本。
- 将提示词输入到 ChatGPT composer。
- 点击发送按钮或按 `Enter`。
- 轮询页面中的图片候选，识别生成图。
- ChatGPT 生成图常见特征：
  - URL 包含 `chatgpt.com/backend-api/estuary/content`。
  - `alt` 包含 `已生成图片`。
  - CSS class 包含特定图片布局特征。
  - ChatGPT 域名下的大尺寸图片。
- 下载 `estuary/content` 图片时使用 `page.request.get()`，这样可以携带当前 Playwright context 的登录 cookie。
- 如果 HTTP 下载失败，则尝试 Canvas 提取。

## 提示词规则

脚本支持两种提示词来源。

### 1. 直接传入完整提示词

如果传入 `--prompt`，脚本会原样发送该提示词，不做改写：

```bash
python scripts/ai_image_playwright.py \
  --platform gemini \
  --prompt "生成一张 3:4 竖屏封面，主题是 AI 自动剪辑，科技感，标题清晰"
```

### 2. 使用标题和描述自动构造封面提示词

如果不传 `--prompt`，脚本会使用 `--title` 和 `--description` 调用内置 `build_prompt()` 构造提示词。

当前模板含义是：

- 要求生成短视频竖屏封面图。
- 比例为 3:4。
- 主题来自 `--title`。
- 如果有 `--description`，会补充视频内容说明。
- 要求标题文字必须清晰醒目，并包含原始标题。
- 要求适合手机信息流。
- 要求构图自然、有设计感、高清高质量。
- 明确禁止生成 APP 界面、手机边框、点赞评论按钮、状态栏或导航栏。

模板生成的提示词大致如下：

```text
请为短视频生成一张竖屏封面图片（3:4比例），主题是：{title}。{desc_part}

要求：标题文字必须清晰醒目并包含：'{title}'；画面适合手机信息流；构图自然、有设计感、高清高质量；不要包含 APP 界面、手机边框、点赞评论按钮、状态栏或导航栏。
```

## 图片下载与保存

默认输出目录在当前 skill 文件夹下：

```text
skills/web-ai-image-generation/.runtime/output
```

也可以通过 `--output-dir` 指定其他目录。

保存流程：

1. 生图完成后，脚本扫描页面中的所有 `img`。
2. 根据平台筛选生成图片候选：
   - Gemini：优先选择尺寸大于约 `400x400` 的大图。
   - ChatGPT：优先识别 `chatgpt.com/backend-api/estuary/content`、`已生成图片`、大尺寸 ChatGPT 图片等候选。
3. 最多取最新 4 张候选图。
4. 按平台和序号保存为 JPEG 文件。

文件名示例：

- `gemini_image_1.jpg`
- `gemini_image_2.jpg`
- `chatgpt_image_1.jpg`
- `chatgpt_image_2.jpg`

下载策略：

- ChatGPT 的 `chatgpt.com/backend-api/estuary/content` 图片使用 `page.request.get()` 下载，可以携带当前登录 cookie。
- Gemini 的 `googleusercontent.com` / `gstatic.com` 图片也使用 `page.request.get()` 下载。
- 如果图片是 `blob:`，或 HTTP 下载失败，会尝试在页面内用 Canvas `drawImage()` 提取，再通过 `toDataURL('image/jpeg', 0.95)` 转为 JPEG base64，最后在 Python 端解码写入文件。
- 文件小于约 `10KB` 会被认为无效并删除。

脚本运行成功后会在标准输出打印保存的图片路径。

## 调用建议

如果要在其他流程里调用这个 skill：

1. 传入平台、提示词、输出目录、profile 目录。
2. 由外部流程决定如何使用生成后的图片。
3. 不要把 API Key 或账号凭据写入脚本。
4. 对 `platform` 做严格校验，只允许 `gemini` 和 `chatgpt`。

## 常见问题

### 找不到“制作图片”或“生成图片”

可能原因：

- 网页语言与选择器不匹配。
- Gemini / ChatGPT UI 更新。
- 当前账号没有生图入口。

处理建议：

- 增加更多语言的选择器。
- 截图确认页面状态。
- 检查账号是否具备生图能力。

### 页面生成了图片但下载失败

可能原因：

- 图片跨域导致 Canvas 读取失败。
- 图片 URL 需要登录 cookie。
- 图片 URL 规则发生变化。

处理建议：

- ChatGPT 图片优先使用 `page.request.get()`。
- Gemini 增加更多图片域名白名单。
- 必要时使用页面截图作为兜底方案。

### 一直等待直到超时

可能原因：

- 没有成功切换到生图模式。
- 提示词触发安全策略。
- 页面出现错误提示，但代码没有识别。

处理建议：

- 检查页面错误文案。
- 增加对“生成失败”“无法生成”等状态的检测。
- 调整等待策略，不只依赖图片数量稳定。

## 后续优化建议

- 增加截图和 HTML dump，便于排查 UI 变化。
- 把等待逻辑改成“生成中状态消失 + 图片出现”。
- 对无桌面服务器支持 `xvfb` 或验证 headless 模式。
- 将平台识别、图片识别、下载逻辑拆成更小的可测试函数。
