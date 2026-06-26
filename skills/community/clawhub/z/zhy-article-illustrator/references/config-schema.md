# .zhy-illustrator.yml 配置说明

用户可在项目根目录放置 `.zhy-illustrator.yml` 文件来持久化偏好设置。
技能在 Step 1 启动时会检查此文件，若存在则读取并合并为默认值。

命令行参数 / skill inputs 的优先级高于配置文件。

---

## 设计原则

新版配置不再只描述“偏好色彩”这种软性信息，而是支持更强的提示词控制、
统一风格控制，以及 Gemini 原生代理 / Xiaomi Gemini 兼容接口生图配置。

推荐思路：

- 用 `prompt_profile` 决定提示词框架
- 用 `visual_consistency` / `information_density` / `finish_level` 决定输出质量基线
- 用 `text_language` / `english_terms_whitelist` 控制图片内文字语言
- 用 `image_provider` / `image_model` / `image_base_url` 控制生图通道

---

## 配置项

```yaml
# .zhy-illustrator.yml

# 默认配图密度
# 可选值: minimal | balanced | rich
density: balanced

# 默认宽高比
aspect_ratio: "16:9"

# 默认是否上传七牛云
upload: false

# 提示词配置档案
# 当前推荐: nano-banana
prompt_profile: nano-banana

# 图片中文字默认语言
# 当前推荐: zh-CN
text_language: zh-CN

# 允许保留英文展示的术语白名单
english_terms_whitelist: []

# 同篇图片风格统一强度
# 可选值: standard | strong
visual_consistency: strong

# 信息密度
# 可选值: medium | high
information_density: high

# 完成度基线
# 可选值: editorial | editorial-premium
finish_level: editorial-premium

# 生图通道
# 推荐值: xiaomi
image_provider: xiaomi

# 模型名称
image_model: gemini-3.1-flash-image-preview

# Gemini 原生代理 / Xiaomi Gemini 兼容接口基础地址
# 默认值使用 Xiaomi Gemini 兼容接口
image_base_url: "https://your-compatible-endpoint.example/v1beta"

# 图片清晰度 / 尺寸标识
# Xiaomi Gemini 兼容接口推荐 1K
image_size: "1K"

# 视觉偏好（作为 visual bible 的补充输入）
visual_preferences:
  color_tendency: ""
  graphic_style: ""
  layout_mood: ""
  watermark: ""

# 图片文件名前缀（默认无前缀，仅序号）
filename_prefix: ""
```

---

## 字段说明

| 字段 | 说明 |
|------|------|
| `prompt_profile` | 当前建议固定为 `nano-banana`，用于启用高完成度编辑视觉提示词模板 |
| `text_language` | 默认图片中文字语言，建议使用 `zh-CN` |
| `english_terms_whitelist` | 允许保留英文展示的术语，如 `Playwright`、`HTTP`、`ROI` |
| `visual_consistency` | 同篇文章图片风格统一强度 |
| `information_density` | 控制图片是偏精简还是偏高信息密度 |
| `finish_level` | 控制画面是否追求更强专题视觉和成片感 |
| `image_provider` | 默认使用 `xiaomi`，也可切回 `gemini` |
| `image_model` | 指定实际调用模型；接口调用默认推荐 `gemini-3.1-flash-image-preview` |
| `image_base_url` | 用于 Gemini 原生代理、中转站或 Xiaomi Gemini 兼容接口接入 |
| `image_size` | 图片清晰度 / 尺寸标识，如 Xiaomi 的 `1K` |
| `visual_preferences` | 作为 visual bible 生成时的补充偏好，不替代统一风格逻辑 |

---

## 示例

### 技术博客 + Nano Banana

```yaml
density: balanced
aspect_ratio: "16:9"
prompt_profile: nano-banana
text_language: zh-CN
english_terms_whitelist:
  - Playwright
  - Chromium
  - Firefox
  - WebKit
visual_consistency: strong
information_density: high
finish_level: editorial-premium
image_provider: xiaomi
image_model: gemini-3.1-flash-image-preview
image_base_url: "https://your-compatible-endpoint.example/v1beta"
image_size: "1K"
visual_preferences:
  color_tendency: "深蓝灰底，蓝青高亮"
  graphic_style: "圆角卡片、细线连接、科技编辑视觉"
  layout_mood: "模块清晰、留白克制、信息密度高"
  watermark: ""
```

### 使用 Gemini 原生代理 / 中转站

```yaml
density: balanced
aspect_ratio: "16:9"
prompt_profile: nano-banana
text_language: zh-CN
visual_consistency: strong
information_density: high
finish_level: editorial-premium
image_provider: gemini
image_model: gemini-3.1-flash-image-preview
image_base_url: "https://your-relay.example.com/v1beta"
```

### 使用 Xiaomi Gemini 兼容接口

```yaml
density: balanced
aspect_ratio: "16:9"
prompt_profile: nano-banana
text_language: zh-CN
visual_consistency: strong
information_density: high
finish_level: editorial-premium
image_provider: xiaomi
image_model: gemini-3.1-flash-image-preview
image_base_url: "https://your-compatible-endpoint.example/v1beta"
image_size: "1K"
```

### 生活类公众号

```yaml
density: rich
aspect_ratio: "4:3"
prompt_profile: nano-banana
text_language: zh-CN
visual_consistency: strong
information_density: medium
finish_level: editorial-premium
image_provider: gemini
image_model: gemini-3.1-flash-image-preview
visual_preferences:
  color_tendency: "暖色系，柔和自然光"
  graphic_style: "叙事型编辑视觉，克制插画感"
  layout_mood: "留白较多，节奏舒缓"
  watermark: ""
```

---

## 环境变量建议

推荐在技能根目录 `.env` 中配置：

```dotenv
IMAGE_PROVIDER=xiaomi
IMAGE_MODEL=gemini-3.1-flash-image-preview
IMAGE_BASE_URL=https://your-compatible-endpoint.example/v1beta
IMAGE_API_KEY=
IMAGE_SIZE=1K

# Xiaomi Gemini 兼容接口
XIAOMI_API_KEY=
XIAOMI_BASE_URL=https://your-compatible-endpoint.example/v1beta
XIAOMI_IMAGE_SIZE=1K

# 兼容官方直连 fallback
GEMINI_API_KEY=
GOOGLE_API_KEY=
```

如果使用 Gemini 原生代理，中转站应尽量兼容 Gemini 原生接口路径与请求格式。
如果使用 Xiaomi 接口，推荐直接设置 `IMAGE_PROVIDER=xiaomi`，并配合 `XIAOMI_API_KEY` 与 `XIAOMI_IMAGE_SIZE`。

配合规划脚本可这样使用：

```bash
bun run scripts/plan-illustrations.ts --article articles/demo/article.md
```

---

## 注意事项

- `visual_preferences` 现在是补充输入，不是唯一风格来源
- 真正的统一风格由文章级 `visual_bible` 决定
- `english_terms_whitelist` 只应用于确实需要保留英文的专有术语
- `image_base_url` 留空时走官方 Gemini 地址；填写后可走 Gemini 原生代理或 Xiaomi Gemini 兼容接口
- Xiaomi 图片接口文档显示其请求风格接近 Gemini 原生，但多模态 `inline_data` 字段命名与 `imageSize` 支持略有差异，脚本已做兼容处理
- 此文件完全可选，不存在时技能仍可使用默认值运行
