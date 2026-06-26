---
name: "toutiao-publish"
description: "用 Cookie 或已保存会话在头条号后台发布文章，支持标题/正文/图片与固定目录 docx 导入。当用户要自动发头条文章、传入 cookie_header 或要求按 docx 流程发布时调用。"
---

# Toutiao Publish

## 目标

把用户给的标题、正文、图片（可选）或 docx 文档发布到头条号后台。优先使用 `cookie_header` 参数登录；未提供 cookie 时使用已保存的会话文件。

## 适用场景（触发条件）

- 用户说“发头条文章/发文到头条/自动发布头条”
- 用户提供 `title` + `content`（或 `content_file`）+ 可选 `images`
- 用户要求从固定目录 docx 自动导入并发布
- 用户提供 `cookie_header`，希望无交互登录并发文

## 输入（建议 OpenClaw 传参）

- `title`：字符串，必填
- `content`：字符串，必填（纯文本）
- `images`：字符串数组，可选（服务器上的图片绝对路径）
- `docx`：可选；如使用固定目录投放，可不传，由脚本自动取第一个 `.docx`
- `docx_wait_seconds`：可选，整数；docx 导入后的等待秒数，默认 `60`，可设为 `90`、`120`
- `cookie_header`：字符串，可选（形如 `a=b; c=d; ...`，来自浏览器对 `mp.toutiao.com` 的 Cookie）
- `publish`：布尔值，可选；默认 `false`（只填充不发布，避免误发）

## 执行方式

在腾讯云 Ubuntu 上执行（项目固定路径）：

```bash
cd /home/ubuntu/projects/toutiao_poster
```

### 1) 使用 cookie_header 发文（推荐，最稳）

只填充不发布：

```bash
TOUTIAO_COOKIE='<cookie_header>' \
./.venv/bin/python -m toutiao_poster post \
  --title '<title>' \
  --content-text '<content>' \
  --headless
```

发布：

```bash
TOUTIAO_COOKIE='<cookie_header>' \
./.venv/bin/python -m toutiao_poster post \
  --title '<title>' \
  --content-text '<content>' \
  --docx-wait-seconds 60 \
  --headless \
  --publish
```

带图片（多张图重复传 `--image`）：

```bash
TOUTIAO_COOKIE='<cookie_header>' \
./.venv/bin/python -m toutiao_poster post \
  --title '<title>' \
  --content-text '<content>' \
  --image '/abs/path/1.png' \
  --image '/abs/path/2.jpg' \
  --docx-wait-seconds 60 \
  --headless \
  --publish
```

### 2) 不提供 cookie_header（使用已保存会话）

```bash
./.venv/bin/python -m toutiao_poster post \
  --title '<title>' \
  --content-text '<content>' \
  --docx-wait-seconds 60 \
  --headless \
  --publish
```

### 3) OpenClaw 固定图片目录（无需传 images）

当 OpenClaw 把图片保存到固定目录时，不需要传 `--image`，脚本会自动读取并上传：

- 默认目录优先级：
  - `/home/ubuntu/projects/artifacts/toutiaopic`
  - `./artifacts/toutiaopic`（以运行时 cwd 为准）
  - `/home/ubuntu/projects/toutiao_poster/artifacts/toutiaopic`
  - `/home/ubuntu/projects/toutiao_poster/.toutiao_poster/artifacts/toutiaopic`
- 发文成功后自动移动到：
  - `<图片目录>/done/`
- 也可通过环境变量覆盖目录：
  - `TOUTIAO_IMAGE_DIR=/abs/path/to/toutiaopic`

示例（无需传 `--image`）：

```bash
TOUTIAO_COOKIE='<cookie_header>' \
./.venv/bin/python -m toutiao_poster post \
  --title '<title>' \
  --content-text '<content>' \
  --headless \
  --publish
```

### 4) OpenClaw 固定 docx 目录（推荐，有文档时优先走文档导入）

当 OpenClaw 把 docx 保存到固定目录时，不需要额外传文档路径，脚本会自动读取目录中的第一个 `.docx`：

- 固定目录：
  - `/home/ubuntu/projects/toutiao_poster/.toutiao_poster/artifacts/toutiaodoc/`
- 发文成功后自动移动到：
  - `/home/ubuntu/projects/toutiao_poster/.toutiao_poster/artifacts/toutiaodoc/done/`
- docx 模式下会严格执行以下步骤：
  - 点击“文档导入”
  - 点击“选择文档”，并把完整路径写入文件输入框
  - 按 `docx_wait_seconds` 等待文档解析，默认 60 秒
  - 点击“预览并发布”
  - 点击“确认发布”

示例（只要目录里有 docx，就会优先导入该 docx）：

```bash
TOUTIAO_COOKIE='<cookie_header>' \
./.venv/bin/python -m toutiao_poster post \
  --title '<title>' \
  --content-text '<content>' \
  --docx-wait-seconds 90 \
  --headless \
  --publish
```

说明：

- 如果固定 docx 目录里存在文档，脚本优先走 docx 导入流程
- 如果文档较大、图片较多或头条解析较慢，可把 `--docx-wait-seconds` 调大到 `90` 或 `120`
- 成功发布后，已处理的 docx 会自动归档到 `done/`
- 如果 docx 导入失败，脚本会直接停止，避免误点其他按钮

## 产物与排障

- 每一步都会在以下目录保存截图，便于无界面环境核对：
  - `/home/ubuntu/projects/toutiao_poster/.toutiao_poster/artifacts/`
- 常见失败原因：
  - 会话失效/未登录：改用 cookie_header 或重新登录保存会话
  - 风控/滑块/验证码：不尝试绕过；改用 cookie_header（来自已通过验证的浏览器会话）
  - 固定 docx 目录为空：不会走文档导入流程，请先把 `.docx` 放入 `toutiaodoc/`
  - 页面结构变化导致控件找不到：查看 artifacts 的最新截图，按截图更新选择器
