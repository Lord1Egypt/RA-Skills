# Showmeai

**[English](README.md) | [中文](README.zh-CN.md)**

通过 Showmeai API，让你的 AI 助手学会画图和生成视频。图像生成使用 OpenAI 兼容的 Images API。视频生成使用 Seedance (Doubao) API。快速、灵活，配置好后即可使用。

---

## 前置条件

- Python 3
- 一个 [Showmeai API 密钥](https://api.showmeai.art) (`Showmeai_API_KEY`)

---

## 配置

在 `.env` 或 `~/.openclaw/openclaw.json` 中设置：
- `Showmeai_API_KEY` — 你的 Showmeai API 密钥 **（必需）**
- `Showmeai_BASE_URL` — 带有 /v1 后缀的基础 URL **（必需）**；如未设置则默认为 `https://api.showmeai.art/v1`

---

## 示例提示词

配置好后，直接用自然语言告诉 AI 你想要什么。

### 图像生成 - 基础

| 提示词 |
|---|
| 画一张海上日落的风景 |
| 生成一张赛博朋克风格的城市夜景 |
| 画一只可爱的卡通猫咪插画 |

### 图像生成 - 指定比例

| 提示词 |
|---|
| 生成一张 16:9 的星空壁纸 |
| 画一张 2:3 竖版奇幻战士肖像 |
| 画一个穿西装的狐狸头像，1:1 方形 |

### 图像生成 - 保存到本地

| 提示词 |
|---|
| 生成一张森林场景的图片，保存到本地 |
| 画 3 张山景图，保存到本地 |

### 图像生成 - 高清生图

| 提示词 |
|---|
| 用高清 4K 模型画一条龙的插画 |
| 生成一张 2K 高清城市地图插画 |

---

## 视频生成

### 文生视频

| 提示词 |
|---|
| 生成一段侦探进入昏暗房间的视频 |
| 生成一段猫咪玩毛线球的视频 |
| 制作一段 10 秒的日落延时视频 |

### 图生视频

| 提示词 |
|---|
| 让这张图片里的女孩睁开眼睛动起来 |
| 用这张照片生成视频，镜头缓慢拉出 |

### 视频参数

| 提示词 |
|---|
| 生成 16:9 宽屏视频 |
| 生成 5 秒 720p 分辨率的视频 |
| 生成无声视频以节省费用 |

---

## 图像转 3D 模型

将 2D 图像转换为 3D 模型（推荐使用 PNG 透明背景图片）。

### 基础转换

| 提示词 |
|---|
| 将这个角色图片转换为 3D 模型 |
| 用纹理从这个精灵图创建 3D 模型 |
| 生成更高质量的 3D 模型 |

### 3D 参数

| 提示词 |
|---|
| 转换为带纹理的 GLB 格式 |
| 用更多步骤生成更高质量 |
| 创建用于 3D 打印的 STL 文件 |

---

## 支持的模型

### 图像模型

| 模型 | 质量 | 输出 |
|---|---|---|
| `nano-banana` | 标准 | URL |
| `nano-banana-pro` | 更好 — **默认** | URL |
| `nano-banana-2` | 第二代 | URL |
| `nano-banana-pro-2k` | 高清 2K | URL |
| `nano-banana-pro-4k` | 超清 4K | URL |
| `gpt-image-1` | 高质量 | 保存的文件 |
| `gpt-image-1.5` | 更高质量 | 保存的文件 |

### 视频模型

| 模型 | 特性 |
|---|---|
| `doubao-seedance-1-5-pro-251215` | **默认**。文生视频、图生视频、首尾帧视频。支持音频生成、草稿模式。24 FPS，5s/10s 时长，480P/720P 分辨率。 |

### 3D 模型

| 模型 | 特性 |
|---|---|
| `Hunyuan3D-2` | **默认**。快速转换（秒级）。支持 glb/stl 输出。 |
| `Hi3DGen` | 图像转 3D。支持 glb/stl 输出。 |
| `Step1X-3D` | 图像转 3D。支持 glb/stl 输出。 |

---

## 图片保存说明

| 参数 | 行为 |
|---|---|
| *(默认)* | 仅返回图片 URL，不保存本地文件 |
| `--save` | 保存到 `~/.openclaw/media/` |
| `--oss` | 保存到 `~/.openclaw/oss/` |
| `gpt-image` 模型 | 始终保存（API 仅返回 base64） |

---

## 链接

- Showmeai API: [api.showmeai.art](https://api.showmeai.art)
- OpenClaw: [openclaw.ai](https://openclaw.ai)
- ClawHub: [clawhub.ai](https://clawhub.ai)
