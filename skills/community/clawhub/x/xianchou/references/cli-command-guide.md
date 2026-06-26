# CLI 命令指南

本文档说明 `xianchou` CLI 的安装、认证、环境变量、命令参数和输出格式。

## 安装

```bash
npm install -g @xianchou/cli
```

本地源码开发：

```bash
cd cli
pnpm install
pnpm build
pnpm dev -- --help
```

## 认证

在献丑 Web 登录后，点击头像菜单中的 `Access Key`，在弹窗中点击 `创建新 Access Key`，复制完整 Access Key。

```bash
xianchou auth login --key <ACCESS_KEY> --project-id <PROJECT_ID>
```

凭据默认保存到 `~/.xianchou/config.json`。可通过 `XIANCHOU_CONFIG_DIR` 改变目录。

环境变量优先级高于配置文件：

```bash
export XIANCHOU_ACCESS_KEY=<ACCESS_KEY>
export XIANCHOU_PROJECT_ID=<PROJECT_ID>
export XIANCHOU_API_URL=https://api.xianchou.com
```

## 模型列表

```bash
xianchou models image --project-id <PROJECT_ID>
```

返回 JSON，包含 `models[]` 和 `defaults`。生成图片前必须动态读取模型，不要硬编码模型 ID。

## 单张生图

```bash
xianchou generate image \
  --prompt "现代科技文档封面，抽象 AI 视频创作画布" \
  --project-id <PROJECT_ID> \
  --poll
```

可选参数：

| 参数 | 说明 |
|------|------|
| `--provider-id` | 从 `models image` 返回值中读取 |
| `--model-id` | 从 `models image` 返回值中读取 |
| `--ratio` | 宽高比，如 `16-9` |
| `--resolution` | 分辨率选项 |
| `--output-format` | 输出格式 |
| `--number` | 生成数量 |
| `--image-urls` | 逗号分隔的参考图 URL 或本地路径（传入后自动切换为图生图模式） |
| `--poll` | 轮询到完成并自动 settle |

## 图生图

传入 `--image-urls` 参数时自动切换为图生图模式（`image-to-image`）：

```bash
xianchou generate image \
  --prompt "将参考图转为水彩风格" \
  --image-urls "./reference.png" \
  --project-id <PROJECT_ID> \
  --poll
```

`--image-urls` 支持本地文件路径，CLI 会自动上传到平台。

## 上传文件

将本地文件上传到献丑平台，获取可公开访问的 URL：

```bash
xianchou upload ./01.png
```

输出 JSON：

```json
{"success": true, "url": "https://xianchou.com/users/cli-uploads/..."}
```

支持的文件类型：
- 图片：`.png`, `.jpg`, `.jpeg`, `.webp`, `.gif`（最大 20MB）
- 视频：`.mp4`, `.mov`, `.webm`（最大 100MB）
- 音频：`.mp3`, `.wav`, `.m4a`, `.flac`, `.aac`（最大 50MB）

## 本地文件自动上传

`generate video` 和 `generate image` 的所有 URL 参数都支持传入本地文件路径。CLI 会自动检测非 URL 的值，上传文件后替换为平台 URL：

```bash
# 本地文件路径会自动上传
xianchou generate video --mode first \
  --prompt "让图片动起来" \
  --first-frame-url ./scene01.png \
  --project-id <PROJECT_ID> \
  --poll
```

## Markdown 插图

```bash
xianchou markdown images ./article.md --count 3 --write
```

常用参数：

| 参数 | 说明 |
|------|------|
| `--count` | 正文图片数量 |
| `--cover` | 生成封面并更新 frontmatter |
| `--write` | 写回 Markdown；不传则为 dry-run |
| `--assets-dir` | 图片保存目录 |
| `--public-url-prefix` | Markdown 中写入的 URL 前缀 |

封面图示例：

```bash
xianchou markdown images ./article.md \
  --cover \
  --count 3 \
  --write
```
