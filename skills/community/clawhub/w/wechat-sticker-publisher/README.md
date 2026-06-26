# WeChat Sticker Publisher / 微信公众号贴图发布器

## English

A small skill/project for creating **WeChat Official Account image-first sticker drafts** (图片消息 / 发贴图) via the official API.

- Repository: `git@github.com:hzlawliet/wechat-sticker-publisher-skill.git`

### What it does
- Uploads one or more local images as permanent WeChat materials
- Creates a `newspic` draft in the WeChat draft box
- Keeps the workflow **draft-only**
- Leaves final publication to a human operator in the WeChat backend

### What it does not do
- It does **not** change the existing daily article publishing workflow
- It does **not** auto-publish
- It does **not** require browser automation

### Why this exists
The WeChat backend has an image-first posting tab parallel to "Write Article". This project packages that capability into a reusable draft-box workflow.

### Usage
```bash
python3 scripts/publish_sticker.py \
  --image /abs/path/to/image.jpg \
  --title "Title" \
  --text "Short caption"
```

Multi-image example:
```bash
python3 scripts/publish_sticker.py \
  --image /abs/1.jpg \
  --image /abs/2.jpg \
  --title "Poster draft" \
  --text "A short image-first post"
```

### Requirements
- Python 3.10+
- `requests`
- Or install from `requirements.txt`
- Required environment variables for actual API calls:
  - `WECHAT_APP_ID`
  - `WECHAT_APP_SECRET`
- Main secret:
  - `WECHAT_APP_SECRET`
- Optional helper file:
  - `wechat.env.example` is included as a template; copy it to `wechat.env` locally and fill in your real credentials

### Important note
Chinese text should be sent as explicit UTF-8 JSON request bodies. Otherwise the title/caption may become garbled.

---

## 中文

一个用于创建**微信公众号“发贴图 / 图片消息”草稿**的小型 skill / 项目，走官方 API，不走浏览器自动化。

- 仓库地址：`git@github.com:hzlawliet/wechat-sticker-publisher-skill.git`

### 它能做什么
- 把一张或多张本地图片上传为微信永久素材
- 在公众号草稿箱中创建 `newspic` 类型草稿
- 整个流程保持为**仅写入草稿箱**
- 最终发布由人手动在公众号后台完成

### 它不做什么
- **不**修改现有每日日报“发文章”逻辑
- **不**自动发布
- **不**依赖浏览器自动化

### 为什么做这个
公众号后台有一个和“写文章”并列的“发贴图”入口。这个项目把这条能力整理成一个可复用的草稿箱工作流。

### 用法
```bash
python3 scripts/publish_sticker.py \
  --image /abs/path/to/image.jpg \
  --title "标题" \
  --text "配文"
```

多图示例：
```bash
python3 scripts/publish_sticker.py \
  --image /abs/1.jpg \
  --image /abs/2.jpg \
  --title "贴图草稿测试" \
  --text "这是一个以图片为主、文字为辅的草稿。"
```

### 依赖
- Python 3.10+
- `requests`
- 或使用 `requirements.txt` 安装
- 实际调用 API 时需要的环境变量：
  - `WECHAT_APP_ID`
  - `WECHAT_APP_SECRET`
- 主要敏感凭证：
  - `WECHAT_APP_SECRET`
- 可选模板文件：
  - 已附带 `wechat.env.example`，本地可复制为 `wechat.env` 后再填写真实凭证

### 重要说明
中文标题/配文必须显式按 UTF-8 JSON 请求体发送，否则可能出现乱码。
